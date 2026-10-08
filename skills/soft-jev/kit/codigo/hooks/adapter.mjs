#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { HARNESS_NAMES, MAX_HOOK_BYTES, hookOutput, normalizeHook, record } from './normalize.mjs';
import { hasExplicitInvocation, loadCatalog } from './catalog.mjs';

export const CORE_TIMEOUT_MS = 7000;
const MAX_OUTPUT_BYTES = 32 * 1024;
const DEFAULT_CORE = fileURLToPath(new URL('../src/automation-cli.mjs', import.meta.url));

/** @param {unknown} input @param {{corePath?:string,nodePath?:string,timeoutMs?:number}} [options] */
export async function callCore(input, { corePath = DEFAULT_CORE, nodePath = process.execPath, timeoutMs = CORE_TIMEOUT_MS } = {}) {
  return new Promise((resolveResult) => {
    let settled = false;
    let size = 0;
    const chunks = [];
    const child = spawn(nodePath, [corePath], { stdio: ['pipe', 'pipe', 'ignore'], windowsHide: true });
    const finish = (result = {}) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (child.exitCode === null) child.kill('SIGKILL');
      resolveResult(result);
    };
    const timer = setTimeout(() => finish(), timeoutMs);
    child.on('error', () => finish());
    child.stdin.on('error', () => finish());
    child.stdout.on('data', (chunk) => {
      size += chunk.length;
      if (size > MAX_OUTPUT_BYTES) return finish();
      chunks.push(chunk);
    });
    child.on('close', (code) => {
      if (code !== 0) return finish();
      try { finish(JSON.parse(Buffer.concat(chunks).toString('utf8'))); } catch { finish(); }
    });
    child.stdin.end(JSON.stringify(input));
  });
}

/** @param {unknown} raw @param {{harness:string,profile?:string,env?:Record<string,string|undefined>}} options
 * @param {(input: unknown) => Promise<unknown>} [invoke]
 * @param {(event: unknown, options: unknown) => Promise<object>} [catalog] */
export async function runHook(raw, options, invoke = callCore, catalog = loadCatalog) {
  const hook = normalizeHook(raw, options);
  if (!hook) return {};
  try {
    if (['prepare', 'delegate'].includes(hook.input.event) && !hook.input.skip_reason) {
      const available = await catalog(hook.input, { cwd: raw.cwd, env: options.env });
      if (hasExplicitInvocation(hook.input.text, available.personas)) {
        if (hook.input.event === 'delegate') hook.input.explicit_choice = true;
        delete available.personas;
        // Persona activation skills must not reintroduce an alternative role.
        if (available.skills) available.skills = available.skills.filter(({ id }) => !id.startsWith('role-'));
      }
      if (hasExplicitInvocation(hook.input.text, available.skills)) delete available.skills;
      Object.assign(hook.input, available);
    }
    return hookOutput(hook, await invoke(hook.input));
  } catch { return {}; }
}

/** @param {AsyncIterable<Buffer|string>} stream */
export async function readPayload(stream) {
  let bytes = 0;
  const chunks = [];
  for await (const value of stream) {
    const chunk = Buffer.isBuffer(value) ? value : Buffer.from(value);
    bytes += chunk.length;
    if (bytes > MAX_HOOK_BYTES) throw new Error('hook_payload_too_large');
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}

async function main() {
  const args = process.argv.slice(2);
  const options = {};
  for (let index = 0; index < args.length; index += 2) {
    const flag = args[index];
    if (!['--harness', '--profile'].includes(flag) || !args[index + 1]) throw new Error('invalid_arguments');
    options[flag.slice(2)] = args[index + 1];
  }
  if (!HARNESS_NAMES.includes(options.harness)) throw new Error('invalid_arguments');
  const raw = await readPayload(process.stdin);
  if (!record(raw)) throw new Error('invalid_payload');
  const result = await runHook(raw, { ...options, env: process.env });
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  // A consultative hook must fail open without exposing payloads or raw errors.
  main().catch(() => { process.stdout.write('{}\n'); });
}
