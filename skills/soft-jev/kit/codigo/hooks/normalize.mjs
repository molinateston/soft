import { verificationKinds } from '../src/verification.mjs';

/** Host payloads are untrusted. Only the current message or a selected candidate
 * enters the advisory core; transcripts, command arguments and tool outputs do not
 * (a tool becomes at most a verification kind: git, http, test or read). */
export const MAX_HOOK_BYTES = 256 * 1024;
export const MAX_TEXT_BYTES = 16 * 1024;
export const HARNESS_NAMES = ['codex', 'claude', 'grok'];

const EVENTS = new Map([
  ['user_prompt_submit', 'UserPromptSubmit'], ['pre_tool_use', 'PreToolUse'],
  ['post_tool_use', 'PostToolUse'], ['post_tool_use_failure', 'PostToolUseFailure'],
  ['subagent_stop', 'SubagentStop'], ['stop', 'Stop'],
]);

/** @param {unknown} value */
export function record(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

/** @param {unknown} value @param {number} [maxBytes] */
function string(value, maxBytes = MAX_TEXT_BYTES) {
  return typeof value === 'string' && Buffer.byteLength(value) <= maxBytes ? value : '';
}

/** @param {string} toolName */
function toolLeaf(toolName) {
  return toolName.split(/__|[.:/]/).at(-1).toLowerCase();
}

/** @param {string} name */
function writesFiles(name) {
  return ['write', 'edit', 'multiedit', 'apply_patch', 'search_replace', 'write_file'].includes(toolLeaf(name));
}

/** @param {unknown} result @returns {'success'|'failure'|'unknown'} */
function resultStatus(result) {
  if (!record(result)) return 'unknown';
  if (result.isError === true || result.is_error === true || result.success === false) return 'failure';
  const exitCode = result.exit_code ?? result.exitCode;
  if (typeof exitCode === 'number') return exitCode === 0 ? 'success' : 'failure';
  if (result.success === true || result.isError === false || result.is_error === false) return 'success';
  return 'unknown';
}

/** Only explicit memory file edits supply memory candidates. Shell commands and
 * arbitrary source files are deliberately not interpreted as memory writes.
 * @param {string} toolName @param {Record<string, unknown>} input */
function memoryCandidate(toolName, input) {
  if (!['edit', 'search_replace'].includes(toolLeaf(toolName))) return '';
  const path = string(input.file_path ?? input.path ?? input.filePath, 4096);
  const isMemory = /(?:^|[/\\])MEMORY\.md$/i.test(path)
    || /(?:^|[/\\])(?:memory|memories|agent-memory)[/\\].+\.md$/i.test(path);
  if (!isMemory) return '';
  return string(input.new_string ?? input.newString ?? input.replacement);
}

// Claude injects these as UserPromptSubmit, but no human wrote them.
const AUTOMATIC_PROMPT = /^\s*(?:<task-notification>|<system-reminder>|<local-command-stdout>|This session is being continued from a previous conversation)/;

/** @param {unknown} value */
const oversized = (value) => typeof value === 'string' && Buffer.byteLength(value) > MAX_TEXT_BYTES;

/** Who is typing. Automated jobs (for example, unattended `claude -p` runs launched by
 * your own automation/orchestration layer) keep their preparation; the log separates them
 * from an interactive session.
 * @param {Record<string, string|undefined>} env */
export function origin(env) {
  if (['job', 'human'].includes(env.JEV_ORIGIN || '')) return env.JEV_ORIGIN === 'job' ? 'automated_job' : 'interactive';
  if (env.HERMES_AGENT === 'true' || env._HERMES_GATEWAY === '1' || env.HERMES_CRON_SESSION) return 'automated_job';
  if (env.CLAUDE_CODE_ENTRYPOINT === 'sdk-cli') return 'sdk';
  return 'interactive';
}

/** @param {unknown} raw @param {{harness: string, profile?: string, env?: Record<string, string|undefined>}} options */
export function normalizeHook(raw, { harness, profile = 'default', env = {} }) {
  if (!HARNESS_NAMES.includes(harness) || !record(raw)) return null;
  // Grok imports Claude settings by default. The native Grok entry handles it.
  if (harness === 'claude' && env.GROK_HOOK_EVENT) return null;
  const eventName = EVENTS.get(raw.hookEventName) ?? raw.hook_event_name ?? raw.hookEventName;
  const session = string(raw.session_id ?? raw.sessionId, 1024);
  if (!session || typeof eventName !== 'string') return null;
  const child = eventName === 'SubagentStop' ? string(raw.agent_id ?? raw.agentId, 1024) : '';
  const base = {
    harness, profile: string(profile, 4096),
    session_id: child ? `${session}/agent/${child}` : session,
    ...(string(raw.turn_id ?? raw.promptId, 1024) ? { turn_id: string(raw.turn_id ?? raw.promptId, 1024) } : {}),
    origin: origin(env),
  };
  if (eventName === 'UserPromptSubmit') {
    // Oversized requests are logged (skipped/too_large) instead of vanishing; the text never goes on.
    if (oversized(raw.prompt)) return { eventName, input: { ...base, event: 'prepare', text: '', skip_reason: 'too_large' } };
    const text = string(raw.prompt);
    if (text && AUTOMATIC_PROMPT.test(text)) return { eventName, input: { ...base, event: 'prepare', text: '', skip_reason: 'automatic_notification' } };
    return text ? { eventName, input: { ...base, event: 'prepare', text } } : null;
  }
  if (eventName === 'Stop' || eventName === 'SubagentStop') {
    if (raw.stop_hook_active === true || raw.stopHookActive === true) return null;
    if (harness === 'grok' && raw.reason && raw.reason !== 'end_turn') return null;
    const message = raw.last_assistant_message ?? raw.lastAssistantMessage;
    if (oversized(message)) return { eventName, input: { ...base, event: 'observe', text: '', skip_reason: 'too_large' } };
    const text = string(message);
    return text ? { eventName, input: { ...base, event: 'observe', text } } : null;
  }
  if (!['PreToolUse', 'PostToolUse', 'PostToolUseFailure'].includes(eventName)) return null;
  const toolName = string(raw.tool_name ?? raw.toolName, 256);
  if (!toolName || !/^[\w.:/-]+$/.test(toolName)) return null;
  const input = record(raw.tool_input ?? raw.toolInput) ? (raw.tool_input ?? raw.toolInput) : {};
  if (eventName === 'PreToolUse') {
    if (['agent', 'task', 'spawn_agent', 'spawn_subagent'].includes(toolLeaf(toolName))) {
      // Claude always names the subagent type, so a persona hint would never be used.
      if (harness === 'claude') return null;
      const text = string(input.prompt ?? input.message ?? input.task);
      if (text) return { eventName, input: { ...base, event: 'delegate', text,
        explicit_choice: ['subagent_type', 'agent_type', 'subagentType', 'role', 'persona'].some((key) => typeof input[key] === 'string' && input[key].trim().length > 0),
      } };
    }
    const candidate = memoryCandidate(toolName, input);
    if (candidate) return { eventName, input: { ...base, event: 'memory', text: candidate } };
    // Outcomes are collected only after completion, never as pending duplicates.
    return null;
  }
  const status = eventName === 'PostToolUseFailure' ? 'failure'
    : eventName === 'PreToolUse' ? 'unknown' : resultStatus(raw.tool_response ?? raw.toolResult);
  // The command is classified here and dropped; only the kind reaches the core.
  const verify = status === 'failure' ? [] : verificationKinds(toolName, input.command ?? input.cmd);
  return {
    eventName,
    input: {
      ...base, event: 'collect', text: '',
      evidence: { status, tool_name: toolName, wrote_files: status === 'success' && writesFiles(toolName), ...(verify.length ? { verify } : {}) },
      ...(harness === 'grok' && eventName !== 'PreToolUse' ? { consume_preparation: true } : {}),
    },
  };
}

/** Never emit permissions, replacements, or Stop feedback. The core generates
 * context from trusted local IDs/enums; upstream text is never an instruction.
 * @param {{eventName: string, input: {harness: string}} | null} hook
 * @param {unknown} result */
export function hookOutput(hook, result) {
  if (!hook || !record(result) || !['ok', 'cached'].includes(result.status)) return {};
  const allowed = ['UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'PostToolUseFailure'];
  if (!allowed.includes(hook.eventName)) return {};
  if (hook.input.harness === 'grok' && hook.eventName === 'UserPromptSubmit') return {};
  const context = string(result.context, 8 * 1024);
  return context ? { hookSpecificOutput: { hookEventName: hook.eventName, additionalContext: context } } : {};
}
