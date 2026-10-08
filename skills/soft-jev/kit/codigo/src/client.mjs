import { execFile, spawn } from 'node:child_process';
import { promisify } from 'node:util';
import {
  ENDPOINT, MAX_RESPONSE_BYTES, MODEL, NETWORK_TIMEOUT_MS, normalizeResponse, validArguments,
} from './contracts.mjs';

/**
 * Optional 1Password reference (`op://vault/item/field`), only used if you keep the credential in
 * 1Password. Configure your own via `JEV_OP_REFERENCE`; when unset this lookup is skipped entirely.
 * The credential that always works, with no extra setup, is the `OPENROUTER_API_KEY` env var
 * (adaptação OpenRouter); `TYPESAFE_API_KEY` segue aceito como alternativa.
 */
export const KEY_REFERENCE = process.env.JEV_OP_REFERENCE || '';
/** macOS Keychain cache (optional): each hook is a new process, and `op read` costs about 2-3 s on the Mac. */
export const KEYCHAIN_SERVICE = 'jev-auto';
const KEYCHAIN_ACCOUNT = 'typesafe';
const SECURITY = '/usr/bin/security';
const execute = promisify(execFile);
/** @type {'environment'|'memory'|'keychain'|'1password'|'none'} */
let lastSource = 'none';
/** Where the last resolved key came from (for telemetry; never the key itself). */
export const keySource = () => lastSource;
const keychainEnabled = () => process.platform === 'darwin' && process.env.JEV_KEYCHAIN !== '0';

/** @param {unknown} value @returns {value is string} */
const validKey = (value) => typeof value === 'string' && value.trim().length > 0 && value.length <= 8_192
  && !['\r', '\n', '\u0000'].some((character) => value.includes(character));

/** @returns {Promise<string | null>} */
async function readOnePassword() {
  if (!KEY_REFERENCE) return null; // No reference configured: this optional shortcut is a no-op.
  try {
    const { stdout } = await execute('op', ['read', KEY_REFERENCE], {
      encoding: 'utf8', timeout: 3_000, maxBuffer: 16_384, windowsHide: true,
    });
    const value = stdout.trim();
    return validKey(value) ? value : null;
  } catch {
    // execFile errors may contain stdout/stderr (including secrets); never log them.
    return null;
  }
}

/** @returns {Promise<{key: string | null, missing: boolean}>} `missing` only when the Keychain answered "not found". */
async function readKeychain() {
  try {
    const { stdout } = await execute(SECURITY, ['find-generic-password', '-s', KEYCHAIN_SERVICE, '-a', KEYCHAIN_ACCOUNT, '-w'], {
      encoding: 'utf8', timeout: 1_500, maxBuffer: 16_384,
    });
    const value = stdout.trim();
    return { key: validKey(value) ? value : null, missing: false };
  } catch (error) {
    // Exit 44 = item not found. A locked Keychain (e.g. SSH session) is not "missing": never write then.
    return { key: null, missing: /** @type {{code?: unknown}} */ (error)?.code === 44 };
  }
}

/** The key goes through stdin of `security -i`, never through argv, a file or a log.
 * @param {string} key @param {string} command */
function keychainCommand(key, command) {
  return new Promise((resolveCommand) => {
    // Only plain token characters: anything else could break the interactive parser's quoting.
    if (!/^[A-Za-z0-9._~+/=-]+$/.test(key)) return resolveCommand(false);
    const child = spawn(SECURITY, ['-i'], { stdio: ['pipe', 'ignore', 'ignore'] });
    const timer = setTimeout(() => { child.kill('SIGKILL'); resolveCommand(false); }, 1_500);
    child.on('error', () => { clearTimeout(timer); resolveCommand(false); });
    child.on('close', (code) => { clearTimeout(timer); resolveCommand(code === 0); });
    child.stdin.on('error', () => {});
    child.stdin.end(`${command} -w "${key}"\n`);
  });
}

/** @returns {Promise<string | null>} */
async function readKey() {
  const keychain = keychainEnabled() ? await readKeychain() : { key: null, missing: false };
  if (keychain.key) { lastSource = 'keychain'; return keychain.key; }
  const value = await readOnePassword();
  if (value) {
    lastSource = '1password';
    // Filled once from 1Password; later hooks read the Keychain (about 20 ms) instead of `op read`.
    if (keychain.missing) await keychainCommand(value, `add-generic-password -U -s ${KEYCHAIN_SERVICE} -a ${KEYCHAIN_ACCOUNT}`);
  }
  return value;
}

/** Remove the cached Keychain item (after the API rejects the key), so the next read goes to 1Password. */
async function forgetKeychain() {
  if (!keychainEnabled()) return;
  try {
    await execute(SECURITY, ['delete-generic-password', '-s', KEYCHAIN_SERVICE, '-a', KEYCHAIN_ACCOUNT], { timeout: 1_500 });
  } catch { /* absent or locked */ }
}

/** In-memory only: a long-lived process (MCP server) reads 1Password once. Never written to disk.
 * @type {Promise<string | null> | null} */
let cachedKey = null;

/** Drop the cached key, e.g. after the API rejects it, so the next call reads 1Password again. */
export async function forgetKey() { cachedKey = null; await forgetKeychain(); }

/** @returns {Promise<string | null>} */
export async function resolveKey() {
  if (validKey(process.env.OPENROUTER_API_KEY)) { lastSource = 'environment'; return process.env.OPENROUTER_API_KEY.trim(); }
  if (validKey(process.env.TYPESAFE_API_KEY)) { lastSource = 'environment'; return process.env.TYPESAFE_API_KEY.trim(); }
  if (cachedKey) lastSource = 'memory';
  if (!cachedKey) cachedKey = readKey();
  const key = await cachedKey;
  if (!key) { cachedKey = null; lastSource = 'none'; }
  return key;
}

export function checkConfiguration() {
  const fromEnvironment = validKey(process.env.OPENROUTER_API_KEY) || validKey(process.env.TYPESAFE_API_KEY);
  return {
    model: MODEL,
    endpoint: ENDPOINT,
    advisory_only: true,
    network_called: false,
    key_present: fromEnvironment ? true : null,
    key_source: fromEnvironment ? 'environment' : '1password_not_checked_offline',
    key_reference: KEY_REFERENCE || null,
    ...(process.platform === 'darwin' ? { keychain_service: KEYCHAIN_SERVICE, keychain_enabled: keychainEnabled() } : {}),
    network_timeout_ms: NETWORK_TIMEOUT_MS,
  };
}

/** @param {string} reason @param {number} [started] @returns {import('./types.js').Result} */
export const fallback = (reason, started = performance.now()) => ({
  available: false, reason, answers: {}, advisory_only: true, ms: Math.round(performance.now() - started),
});

/** @param {Response} response @returns {Promise<unknown>} */
async function readResponse(response) {
  if (!response.body || Number(response.headers.get('content-length')) > MAX_RESPONSE_BYTES) throw new Error('schema');
  const reader = response.body.getReader();
  const chunks = [];
  let bytes = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      if (bytes > MAX_RESPONSE_BYTES) throw new Error('schema');
      chunks.push(value);
    }
    return JSON.parse(Buffer.concat(chunks).toString('utf8'));
  } finally {
    // Cancellation is cleanup only; do not let it extend the request deadline.
    void reader.cancel().catch(() => {});
    reader.releaseLock();
  }
}

/**
 * Dependency injection is for offline tests. Runtime URL/model/deadline are fixed.
 * @param {{fetchImpl?: typeof fetch, keyProvider?: () => Promise<string | null>, onAuthFailure?: () => void | Promise<void>}} [dependencies]
 */
export function createClient({ fetchImpl = fetch, keyProvider = resolveKey, onAuthFailure = forgetKey } = {}) {
  /** @param {unknown} args @returns {Promise<import('./types.js').Result>} */
  return async function decide(args) {
    const started = performance.now();
    if (!validArguments(args)) return fallback('invalid_arguments', started);
    let key;
    try { key = await keyProvider(); } catch { key = null; }
    if (!validKey(key)) return fallback('missing_key', started);
    const controller = new AbortController();
    /** @type {ReturnType<typeof setTimeout> | undefined} */
    let timer;
    let timedOut = false;
    let stage = 'upstream_network';
    const deadline = new Promise((_, reject) => {
      timer = setTimeout(() => {
        timedOut = true;
        controller.abort();
        reject(new Error('timeout'));
      }, NETWORK_TIMEOUT_MS);
    });
    try {
      const operation = (async () => {
        const response = await fetchImpl(ENDPOINT, {
          method: 'POST', redirect: 'error', signal: controller.signal,
          headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ model: MODEL, ...args }),
        });
        if (!response.ok) {
          void response.body?.cancel().catch(() => {});
          stage = [401, 403].includes(response.status) ? 'upstream_auth' : 'upstream_http';
          if (stage === 'upstream_auth') await onAuthFailure();
          throw new Error('http');
        }
        stage = 'upstream_schema';
        const result = normalizeResponse(await readResponse(response), args);
        return { available: true, ...result, advisory_only: /** @type {const} */ (true), ms: Math.round(performance.now() - started) };
      })();
      return /** @type {import('./types.js').Result} */ (await Promise.race([operation, deadline]));
    } catch {
      return fallback(timedOut ? 'upstream_timeout' : stage, started);
    } finally {
      clearTimeout(timer);
    }
  };
}

export const decide = createClient();
