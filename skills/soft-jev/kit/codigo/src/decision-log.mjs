import { mkdir } from 'node:fs/promises';
import { decide as defaultDecide } from './client.mjs';
import { MODEL } from './contracts.mjs';
import { digest, stateDirectory, telemetry } from './automation-store.mjs';

const HARNESSES = ['hermes', 'claude', 'codex', 'grok'];

/**
 * Which agent started this on-demand call. `JEV_HARNESS` wins (set by the Hermes plugin); then the
 * variables each host puts in its tool processes, innermost first: Grok `GROK_SESSION_ID`, Codex
 * `CODEX_THREAD_ID`, Claude Code `CLAUDECODE`, Hermes `HERMES_SESSION_ID`. Only the name is logged.
 * @param {string} fallback @param {Record<string, string | undefined>} [env]
 */
function harness(fallback, env = process.env) {
  if (HARNESSES.includes(env.JEV_HARNESS || '')) return /** @type {string} */ (env.JEV_HARNESS);
  if (env.GROK_SESSION_ID || env.GROK_AGENT) return 'grok';
  if (env.CODEX_THREAD_ID || env.CODEX_SESSION_ID) return 'codex';
  if (env.CLAUDECODE) return 'claude';
  if (env.HERMES_SESSION_ID || env._HERMES_GATEWAY) return 'hermes';
  return fallback;
}

/** Every call outside the automatic hooks is "no meio do trabalho"; `JEV_ORIGIN=teste` keeps test calls apart.
 * @param {Record<string, string | undefined>} [env] */
export const onDemandOrigin = (env = process.env) => (env.JEV_ORIGIN === 'teste' ? 'teste' : 'meio_do_trabalho');

/**
 * Metadata-only record of a catalog decision or a manual `jev_decide` call: id, schema
 * version, status, reason, time and token counts. State, questions and answers are never written.
 * @param {Record<string, unknown>} entry @param {{stateDir?: string, now?: number}} [options]
 */
export async function logDecision(entry, { stateDir = stateDirectory(), now = Date.now() } = {}) {
  try {
    await mkdir(stateDir, { recursive: true, mode: 0o700 });
    await telemetry(stateDir, { at: new Date(now).toISOString(), model: MODEL, ...entry }, now);
  } catch { /* Logging must never change the decision result. */ }
}

/** @param {{available: boolean, reason?: string, ms?: number, usage?: {input_tokens: number, output_tokens: number}}} result @param {boolean} attempted */
export const outcome = (result, attempted) => ({
  status: result.available ? 'ok' : attempted ? 'fallback' : 'skipped', reason: result.reason,
  decision_attempted: attempted, input_tokens: result.usage?.input_tokens || 0,
  output_tokens: result.usage?.output_tokens || 0, ms: result.ms || 0,
});

/** Schema fingerprint of a manual call: question ids, types and wording, hashed. No state.
 * @param {unknown} args */
function schemaOf(args) {
  const questions = args && typeof args === 'object' && !Array.isArray(args) ? /** @type {{questions?: unknown}} */ (args).questions : undefined;
  return questions && typeof questions === 'object' ? digest(questions).slice(0, 12) : 'invalid';
}

/**
 * Manual `jev_decide` (MCP or CLI `--decide`) with the same metadata log as the catalog.
 * @param {unknown} args @param {string} source
 * @param {{client?: typeof defaultDecide, stateDir?: string, env?: Record<string, string | undefined>, version?: string}} [options]
 */
export async function decideAndLog(args, source, { client = defaultDecide, stateDir, env = process.env, version = 'manual' } = {}) {
  const result = await client(args);
  const attempted = result.available || !['invalid_arguments', 'missing_key'].includes(result.reason || '');
  const questions = args && typeof args === 'object' && !Array.isArray(args) ? /** @type {{questions?: unknown}} */ (args).questions : undefined;
  await logDecision({ version, schema: schemaOf(args), harness: harness(source === 'ask' ? 'cli' : source, env), origin: onDemandOrigin(env), via: source,
    event: 'jev_decide', questions: questions && typeof questions === 'object' ? Object.keys(questions).length : 0, ...outcome(result, attempted) },
  stateDir ? { stateDir } : {});
  return result;
}

export { harness };
