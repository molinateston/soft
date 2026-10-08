import { randomUUID } from 'node:crypto';
import { decide, fallback } from './client.mjs';
import { MODEL } from './contracts.mjs';
import { AUTOMATION_VERSION, PHASES, buildRequest, candidates, guidance, observeEnabled } from './automation-policy.mjs';
import { acquireState, digest, stateDirectory, telemetry } from './automation-store.mjs';
import { VERIFY_KINDS, checkCompletion, emptyVerify } from './verification.mjs';
import { keySource } from './client.mjs';

// Circuit opens after 3 consecutive failures; each reopening without a success waits longer (A0.4).
export const LIMITS = Object.freeze({ turn: 8, sessionDay: 256, cacheMs: 300_000, circuitFailures: 3,
  circuitSteps: Object.freeze([60_000, 300_000, 900_000]) });
/** @typedef {import('./automation-types.js').AutomationEvent} AutomationEvent */
/** @typedef {import('./automation-types.js').Guidance} Guidance */

/** @param {unknown} input @returns {AutomationEvent|null} */
export function validateEvent(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) return null;
  const value = /** @type {AutomationEvent} */ (input);
  if (!PHASES.includes(value.event) || !['codex', 'claude', 'grok', 'hermes'].includes(value.harness)
    || typeof value.session_id !== 'string' || !value.session_id || value.session_id.length > 512
    || (value.turn_id !== undefined && (typeof value.turn_id !== 'string' || value.turn_id.length > 512))
    || (value.profile !== undefined && (typeof value.profile !== 'string' || value.profile.length > 512))) return null;
  for (const field of ['text', 'request']) {
    const text = value[/** @type {'text'|'request'} */ (field)];
    if (text !== undefined && typeof text !== 'string') return null;
  }
  // Build a new allowlisted object: extraneous host payload fields can never reach the API.
  return { event: value.event, harness: value.harness, session_id: value.session_id, turn_id: value.turn_id,
    profile: value.profile, text: value.text, request: value.request, skills: candidates(value.skills),
    tools: candidates(value.tools), personas: candidates(value.personas), explicit_choice: value.explicit_choice === true,
    consume_preparation: value.consume_preparation === true,
    evidence: { status: ['success', 'failure'].includes(value.evidence?.status || '') ? value.evidence?.status : 'unknown',
      wrote_files: value.evidence?.wrote_files === true,
      verify: Array.isArray(value.evidence?.verify) ? VERIFY_KINDS.filter((kind) => value.evidence?.verify?.includes(kind)) : [] },
    ...(['automatic_notification', 'too_large'].includes(value.skip_reason || '') ? { skip_reason: value.skip_reason } : {}),
    ...(typeof value.origin === 'string' && /^[a-z][a-z0-9_]{0,23}$/.test(value.origin) ? { origin: value.origin } : {}) };
}

/** Evidence of a new turn. `verify`/`seq` stay local; only the four counters go upstream.
 * @returns {import('./automation-types.js').Evidence} */
const freshEvidence = () => ({ success: 0, failure: 0, unknown: 0, writes: 0, verify: emptyVerify(), seq: 0, last_write: 0, last_verify: 0 });

/** @param {string} event @param {string} turn @param {string} reason @param {'skipped'|'fallback'} [status] @returns {Guidance} */
export const skipped = (event, turn, reason, status = 'skipped') => ({ status, event, turn_id: turn,
  context: '', selection: {}, observations: {}, reason, ms: 0 });

/** @param {unknown} input @param {import('./automation-types.js').AutomationOptions} [options] @returns {Promise<Guidance>} */
export async function runAutomation(input, { stateDir = stateDirectory(), client = decide, now = Date.now, observe = observeEnabled() } = {}) {
  const event = validateEvent(input);
  if (!event) return skipped('invalid', '', 'invalid_event');
  const time = now();
  // No account or user identifier is sent upstream or written verbatim to disk.
  const scope = digest([event.harness, event.profile || 'default', event.session_id]);
  const lock = await acquireState(stateDir, scope, time).catch(() => null);
  if (!lock) return skipped(event.event, '', 'state_busy_or_unavailable', 'fallback');
  const { state } = lock;
  let called = false;
  let masked = 0;
  /** @type {string | undefined} */
  let sensitive;
  try {
    const requestedTurn = event.turn_id ? (event.turn_id === state.turn_id ? event.turn_id : digest(event.turn_id)) : '';
    const fingerprint = digest([event.text, event.skills, event.tools, event.personas]);
    const duplicatePrepare = event.event === 'prepare' && !requestedTurn && state.prepare_fingerprint === fingerprint
      && time - state.prepare_at < 5_000;
    // An automatic notification (subagent finished, reminder) continues the current human turn.
    const continuesTurn = event.skip_reason === 'automatic_notification';
    if (!continuesTurn && ((requestedTurn && requestedTurn !== state.turn_id) || (event.event === 'prepare' && !requestedTurn && !duplicatePrepare) || !state.turn_id)) {
      state.turn_id = requestedTurn || digest(randomUUID());
      state.turn_calls = 0; state.seen = {}; state.guidance = null; state.guidance_consumed = false;
      state.evidence = freshEvidence();
    }
    if (!state.turn_id) state.turn_id = digest(randomUUID());
    state.evidence = { ...freshEvidence(), ...state.evidence, verify: { ...emptyVerify(), ...(state.evidence.verify || {}) } };
    if (event.event === 'prepare' && !event.skip_reason) { state.prepare_fingerprint = fingerprint; state.prepare_at = time; }
    /** @type {Guidance} */
    let result;
    /** @type {string[] | undefined} */
    let dropped;
    let textos;
    if (event.skip_reason) {
      // Logged, never sent: the harness fired a hook that is not a human request we can read.
      result = skipped(event.event, state.turn_id, event.skip_reason);
    } else if (event.event === 'collect') {
      const evidence = state.evidence;
      evidence[event.evidence?.status || 'unknown']++;
      evidence.seq = (evidence.seq || 0) + 1;
      if (event.evidence?.wrote_files) { evidence.writes++; evidence.last_write = evidence.seq; }
      const verified = event.evidence?.status !== 'failure' ? event.evidence?.verify || [] : [];
      for (const kind of verified) /** @type {Record<string, number>} */ (evidence.verify)[kind]++;
      if (verified.length) evidence.last_verify = evidence.seq;
      result = skipped(event.event, state.turn_id, 'evidence_collected_without_api');
      if (event.consume_preparation && !state.guidance_consumed && state.guidance?.context) {
        result = { ...state.guidance, event: 'collect', status: 'cached', reason: 'preparation_delivered_after_first_tool', usage: undefined, ms: 0 };
        state.guidance_consumed = true;
      }
    } else {
      const evidence = event.event === 'file_review' && event.evidence?.wrote_files
        ? { ...state.evidence, writes: Math.max(1, state.evidence.writes) } : state.evidence;
      const request = buildRequest(event, evidence, { observe });
      const key = digest([AUTOMATION_VERSION, MODEL, event.event, request.args]);
      const cached = state.cache[key];
      masked = request.masked || 0; sensitive = request.sensitive; dropped = request.dropped; textos = request.textos;
      if (!request.args) result = skipped(event.event, state.turn_id, request.reason || 'ineligible');
      else if (state.seen[key]) result = { ...state.seen[key], status: state.seen[key].status === 'ok' ? 'cached' : state.seen[key].status, usage: undefined, ms: 0 };
      else if (cached && time - cached.at < LIMITS.cacheMs) result = { ...cached.result, status: 'cached', turn_id: state.turn_id, usage: undefined, ms: 0 };
      else if (state.circuit_until > time) result = skipped(event.event, state.turn_id, 'circuit_open', 'fallback');
      else if (state.calls >= LIMITS.sessionDay || state.turn_calls >= LIMITS.turn) result = skipped(event.event, state.turn_id, 'request_budget_reached', 'fallback');
      else {
        // Persist reservation before I/O so a killed hook cannot evade the cap.
        called = true; state.calls++; state.turn_calls++;
        await lock.save(state);
        let response;
        try { response = await client(request.args); } catch { response = fallback('upstream_unavailable'); }
        result = guidance(event, response, state.turn_id);
        if (response.available) { state.failures = 0; state.circuit_until = 0; state.circuit_trips = 0; state.cache[key] = { at: time, result }; }
        else if (++state.failures >= LIMITS.circuitFailures) {
          const trips = state.circuit_trips || 0;
          state.circuit_until = time + LIMITS.circuitSteps[Math.min(trips, LIMITS.circuitSteps.length - 1)];
          state.circuit_trips = trips + 1;
        }
      }
      state.seen[key] = result;
      if (event.event === 'prepare') state.guidance = result;
      // "Pronto sem prova" em código: roda mesmo quando a consulta foi pulada (filtro, observe desligado).
      if (event.event === 'observe' || event.event === 'file_review') {
        result = { ...result, code_check: checkCompletion(event.text, state.evidence) };
      }
    }
    state.cache = Object.fromEntries(Object.entries(state.cache).filter(([, item]) => time - item.at < LIMITS.cacheMs).slice(-64));
    state.seen = Object.fromEntries(Object.entries(state.seen).slice(-64));
    await lock.save(state);
    await telemetry(stateDir, { at: new Date(time).toISOString(), version: AUTOMATION_VERSION, model: MODEL,
      scope: scope.slice(0, 16), harness: event.harness,
      event: event.event, turn: state.turn_id.slice(0, 16), status: result.status, reason: result.reason,
      decision_attempted: called, input_tokens: result.usage?.input_tokens || 0, output_tokens: result.usage?.output_tokens || 0,
      ms: result.ms, context_bytes: Buffer.byteLength(result.context), hint_generated: Boolean(result.context),
      observation_review: result.observations.review, observation_file_review: result.observations.file_review,
      preparation_consumed: event.event === 'collect' && Boolean(result.context),
      masked_values: masked, sensitive_kind: sensitive, circuit_trips: state.circuit_trips || 0,
      session_calls: state.calls, turn_calls: state.turn_calls,
      // v3: numbers and enum ids only, never text.
      origin: event.origin, key_source: called ? keySource() : undefined,
      signals: result.signals, fired: result.fired, shadow_fired: result.shadow_fired, dropped,
      // Versão da calibração viva em vigor (só id curto `[\w.-]`), quando houver ajuste válido.
      calibration: result.calibration,
      // Versão do texto vivo das perguntas v3 (self-learning v3), quando algum texto foi trocado.
      textos,
      observation_s_sem_prova: result.observations.s_sem_prova,
      // Destaque na métrica: resposta terminou em "?" pedindo "posso?/confirma?" para passo já mandado (s_fim ≥ 0,5, sombra).
      alarme_confirmacao_toa: result.shadow_fired?.includes('s_fim') ? true : undefined,
      code_claims: result.code_check?.claims.length ? result.code_check.claims : undefined,
      unverified_claims: result.code_check?.missing.length ? result.code_check.missing : undefined,
      edited_after_verify: result.code_check?.claims.length ? result.code_check.edited_after_verify : undefined,
      turn_verify: event.event === 'observe' || event.event === 'file_review' ? state.evidence.verify : undefined }, time).catch(() => {});
    return result;
  } catch { return skipped(event.event, state.turn_id, 'automation_unavailable', 'fallback'); }
  finally { await lock.release().catch(() => {}); }
}
