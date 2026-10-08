#!/usr/bin/env node
import { readFile, lstat, mkdir, open, rename, unlink } from 'node:fs/promises';
import { dirname, isAbsolute, resolve } from 'node:path';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { HARNESS_NAMES, record } from './normalize.mjs';

export const MARKER = 'JEV_AUTO_HOOK_V1=1';
/** Codex and Grok keep the hooks a conversation had when it was opened. */
export const REOPEN_NOTICE = {
  codex: 'Conversas do Codex abertas antes da instalação não têm hook: feche e reabra o Codex Desktop/CLI e abra uma conversa nova.',
  grok: 'Sessões do Grok abertas antes da instalação não têm hook: feche e reabra o Grok e abra uma sessão nova.',
};
const BASE_EVENTS = ['UserPromptSubmit', 'PreToolUse', 'PostToolUse', 'Stop', 'SubagentStop'];

/** @param {string} value */
export function shellQuote(value) {
  if (typeof value !== 'string' || value.includes('\0')) throw new Error('invalid_arguments');
  return `'${value.replaceAll("'", "'\\''")}'`;
}

/** Explicit paths make registrations auditable and independent of PATH aliases.
 * Authentication is inherited from the host; no credential is serialized.
 * @param {{harness:string,runtime:string,node:string,profile:string,shell?:string}} options */
export function buildCommand({ harness, runtime, node, profile, shell }) {
  if (!HARNESS_NAMES.includes(harness) || !isAbsolute(runtime) || !isAbsolute(node)) throw new Error('invalid_arguments');
  if (shell && !['/bin/zsh', '/bin/bash'].includes(shell)) throw new Error('invalid_shell');
  const command = `env ${MARKER} ${shellQuote(node)} ${shellQuote(resolve(runtime, 'hooks/adapter.mjs'))} --harness ${shellQuote(harness)} --profile ${shellQuote(profile)}`;
  return shell ? `${shellQuote(shell)} ${shell === '/bin/bash' ? '-lc' : '-c'} ${shellQuote(`exec ${command}`)}` : command;
}

/** Remove only this integration's handlers, preserving other groups and fields.
 * @param {unknown} existing @param {{harness:string,command?:string,remove?:boolean}} options */
export function mergeHooks(existing, { harness, command, remove = false }) {
  if (!record(existing) || !HARNESS_NAMES.includes(harness)) throw new Error('invalid_configuration');
  const next = structuredClone(existing);
  if (next.hooks !== undefined && !record(next.hooks)) throw new Error('invalid_configuration');
  const hooks = next.hooks ?? {};
  for (const [event, groups] of Object.entries(hooks)) {
    if (!Array.isArray(groups)) throw new Error('invalid_configuration');
    hooks[event] = groups.flatMap((group) => {
      if (!record(group) || !Array.isArray(group.hooks)) throw new Error('invalid_configuration');
      const handlers = group.hooks.filter((handler) => !(record(handler)
        && typeof handler.command === 'string' && handler.command.includes(MARKER)));
      if (handlers.length === group.hooks.length) return [group];
      return handlers.length ? [{ ...group, hooks: handlers }] : [];
    });
    if (!hooks[event].length) delete hooks[event];
  }
  if (!remove) {
    if (!command) throw new Error('invalid_arguments');
    const events = harness === 'codex' ? BASE_EVENTS : [...BASE_EVENTS, 'PostToolUseFailure'];
    for (const event of events) {
      hooks[event] ??= [];
      hooks[event].push({ hooks: [{ type: 'command', command, timeout: 8 }] });
    }
  }
  next.hooks = hooks;
  return next;
}

/** @param {{config:string,harness:string,runtime?:string,node?:string,profile?:string,shell?:string,remove?:boolean,apply?:boolean}} options */
export async function installHooks(options) {
  if (!isAbsolute(options.config) || !HARNESS_NAMES.includes(options.harness)) throw new Error('invalid_arguments');
  let existing = {};
  let mode = 0o600;
  try {
    const metadata = await lstat(options.config);
    if (!metadata.isFile() || metadata.isSymbolicLink()) throw new Error('configuration_not_regular_file');
    mode = metadata.mode & 0o777;
    existing = JSON.parse(await readFile(options.config, 'utf8'));
  } catch (error) {
    if (error.code !== 'ENOENT') throw new Error('configuration_read_failed');
  }
  const command = options.remove ? undefined : buildCommand({
    harness: options.harness, runtime: options.runtime, node: options.node,
    profile: options.profile ?? dirname(options.config), shell: options.shell,
  });
  const next = mergeHooks(existing, { harness: options.harness, command, remove: options.remove });
  const changed = JSON.stringify(existing) !== JSON.stringify(next);
  if (options.apply && changed) {
    await mkdir(dirname(options.config), { recursive: true, mode: 0o700 });
    const temporary = `${options.config}.jev-${randomUUID()}.tmp`;
    let handle;
    try {
      handle = await open(temporary, 'wx', mode);
      await handle.writeFile(`${JSON.stringify(next, null, 2)}\n`, 'utf8');
      await handle.sync();
      await handle.close();
      handle = undefined;
      await rename(temporary, options.config);
    } finally {
      await handle?.close().catch(() => {});
      await unlink(temporary).catch(() => {});
    }
  }
  return {
    status: options.apply ? 'applied' : 'dry_run', changed,
    harness: options.harness, config: options.config,
    action: options.remove ? 'remove' : 'install',
    events: Object.entries(next.hooks).filter(([, groups]) => groups.some((group) => group.hooks.some((handler) => handler.command?.includes(MARKER)))).map(([event]) => event),
    ...(command ? { command } : {}),
    trust: options.harness === 'codex' ? 'review_exact_hash_with_native_hooks_list' : 'existing_host_policy_preserved',
    ...(!options.remove && Object.hasOwn(REOPEN_NOTICE, options.harness) ? { reopen: REOPEN_NOTICE[/** @type {'codex'|'grok'} */ (options.harness)] } : {}),
  };
}

async function main() {
  const options = {};
  const args = process.argv.slice(2);
  for (let index = 0; index < args.length; index += 1) {
    const flag = args[index];
    if (flag === '--apply' || flag === '--remove') options[flag.slice(2)] = true;
    else {
      if (!['--config', '--harness', '--runtime', '--node', '--profile', '--shell'].includes(flag) || !args[index + 1]) throw new Error('invalid_arguments');
      options[flag.slice(2)] = args[++index];
    }
  }
  process.stdout.write(`${JSON.stringify(await installHooks(options))}\n`);
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  main().catch(() => {
    process.stdout.write('{"status":"error","reason":"configuration_not_changed_or_write_failed"}\n');
    process.exitCode = 1;
  });
}
