import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readFile, writeFile, rename, unlink, stat, open, chmod, readdir } from 'node:fs/promises';
import { homedir } from 'node:os';
import { join } from 'node:path';

/** @param {unknown} value */
export const digest = (value) => createHash('sha256').update(JSON.stringify(value)).digest('hex');
export const stateDirectory = () => process.env.JEV_AUTOMATION_STATE_DIR || join(homedir(), '.local/state/jev-auto');

/** @param {number} now @returns {import('./automation-types.js').SessionState} */
export function freshState(now) {
  return { version: 1, day: new Date(now).toISOString().slice(0, 10), calls: 0, failures: 0,
    circuit_until: 0, circuit_trips: 0, turn_id: '', turn_calls: 0, prepare_fingerprint: '', prepare_at: 0,
    guidance: null, guidance_consumed: false, evidence: { success: 0, failure: 0, unknown: 0, writes: 0 }, seen: {}, cache: {} };
}

/** Serialized per session; concurrent independent sessions do not block one another.
 * @param {string} directory @param {string} scope @param {number} now
 */
export async function acquireState(directory, scope, now) {
  await mkdir(directory, { recursive: true, mode: 0o700 });
  await chmod(directory, 0o700);
  const path = join(directory, `${scope}.json`);
  const lockPath = `${path}.lock`;
  // A killed hook must not permanently disable the session. No retry of API calls.
  try { if (now - (await stat(lockPath)).mtimeMs > 30_000) await unlink(lockPath); } catch { /* no lock */ }
  /** @type {import('node:fs/promises').FileHandle} */
  let lock;
  try { lock = await open(lockPath, 'wx', 0o600); } catch { return null; }
  let state = freshState(now);
  try {
    if ((await stat(path)).size <= 512_000) {
      const saved = JSON.parse(await readFile(path, 'utf8'));
      if (saved.version === 1 && saved.day === state.day && typeof saved.calls === 'number'
        && saved.evidence && saved.cache && saved.seen) state = saved;
    }
  } catch { /* new, expired or invalid local state */ }
  /** @param {import('./automation-types.js').SessionState} value */
  async function save(value) {
    const temporary = `${path}.${randomUUID()}.tmp`;
    try {
      await writeFile(temporary, JSON.stringify(value), { mode: 0o600 });
      await rename(temporary, path);
    } finally { await unlink(temporary).catch(() => {}); }
  }
  async function release() { await lock.close(); await unlink(lockPath).catch(() => {}); }
  return { state, save, release };
}

/** Bounded metadata only; prompts, identities, arguments and tool outputs are forbidden.
 * @param {string} directory @param {Record<string, unknown>} entry @param {number} now
 */
export async function telemetry(directory, entry, now) {
  const path = join(directory, `events.${new Date(now).toISOString().slice(0, 10)}.jsonl`);
  try {
    if ((await stat(path)).size > 1_048_576) await rename(path, `${path}.previous`);
  } catch { /* first record */ }
  await writeFile(path, `${JSON.stringify(entry)}\n`, { flag: 'a', mode: 0o600 });
  // Retention is seven days. Cleanup only our hash-named metadata, at most 256 entries/run.
  for (const name of (await readdir(directory)).filter((name) => /^(?:[a-f0-9]{64}\.json|events\.\d{4}-\d{2}-\d{2}\.jsonl(?:\.previous)?)$/.test(name)).slice(0, 256)) {
    const candidate = join(directory, name);
    try { if (now - (await stat(candidate)).mtimeMs > 7 * 86_400_000) await unlink(candidate); } catch { /* concurrent cleanup */ }
  }
}
