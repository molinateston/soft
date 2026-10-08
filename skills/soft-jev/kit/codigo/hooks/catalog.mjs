import { open, readdir, stat } from 'node:fs/promises';
import { homedir } from 'node:os';
import { dirname, isAbsolute, join, resolve } from 'node:path';

const MAX_SKILL_HEADERS = 256;
const MAX_HEADER_BYTES = 4096;
const MAX_SKILLS = 12;
const ROLE_DESCRIPTIONS = {
  analyst: 'Research, inspect evidence and compare options.',
  architect: 'Design system architecture and technical boundaries.',
  dev: 'Implement a bounded code change.',
  qa: 'Review correctness, security and test coverage.',
  devops: 'Operate deployment, releases, CI and infrastructure.',
  pm: 'Define product scope and requirements.',
  po: 'Validate requirements and acceptance criteria.',
  sm: 'Draft an actionable implementation story.',
  'data-engineer': 'Design and inspect databases, schemas and data pipelines.',
  'ux-design-expert': 'Design and evaluate user interfaces and experience.',
};
const TOOL_FAMILIES = [
  { id: 'shell', description: 'Local command execution family; verify actual tool and permissions in the current session.' },
  { id: 'files', description: 'Local file inspection and editing family; verify actual tool and permissions in the current session.' },
  { id: 'web', description: 'Web lookup family; verify actual tool and permissions in the current session.' },
  { id: 'delegation', description: 'Subagent delegation family; verify actual tool and permissions in the current session.' },
];

// Palavras que não dizem nada sobre a skill (pt/en). Mantida curta de propósito.
const STOPWORDS = new Set(['que', 'para', 'pra', 'com', 'uma', 'uns', 'umas', 'dos', 'das', 'nos', 'nas', 'por', 'isso', 'esse',
  'essa', 'este', 'esta', 'aqui', 'ali', 'mais', 'muito', 'como', 'quando', 'onde', 'qual', 'quais', 'tem', 'ter', 'ser',
  'est', 'sao', 'foi', 'vai', 'faz', 'fazer', 'pode', 'agora', 'ainda', 'tambem', 'sobre', 'entre', 'seu', 'sua', 'meu',
  'minha', 'nao', 'sim', 'the', 'and', 'for', 'with', 'this', 'that', 'from', 'use', 'when', 'into', 'your', 'you', 'are',
  'not', 'all', 'any', 'skill', 'squad', 'agent', 'agente', 'source', 'command', 'migrated', 'novo', 'novos', 'nova', 'novas']);

/** Radical grosseiro: sem o "s" final e cortado em 6 letras, "criativos"/"criativo" e
 * "vídeos"/"vídeo" batem, e "instagram"/"instalação" não. @param {string} value */
function words(value) {
  return (value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().match(/[a-z0-9]{3,}/g) ?? [])
    .filter((word) => !STOPWORDS.has(word)).map((word) => word.replace(/(?<=...)s$/, '').slice(0, 6));
}

/** @param {string} value @param {Set<string>} query */
function score(value, query) {
  return [...new Set(words(value))].reduce((sum, word) => sum + (query.has(word) ? 1 : 0), 0);
}

/** Relevance: words of the request that appear in the id (weight 2) or in the description (weight 1).
 * @param {{id: string, description: string}} skill @param {Set<string>} query */
const relevance = (skill, query) => 2 * score(skill.id.replace(/^source-command-/, ''), query) + score(skill.description, query);

/** @param {string} path */
async function isFile(path) {
  try { return (await stat(path)).isFile(); } catch { return false; }
}

/** First bytes of a file; never the whole body. @param {string} path */
async function head(path) {
  let handle;
  try {
    handle = await open(path, 'r');
    const buffer = Buffer.alloc(MAX_HEADER_BYTES);
    const { bytesRead } = await handle.read(buffer, 0, buffer.length, 0);
    return buffer.subarray(0, bytesRead).toString('utf8');
  } catch { return null; } finally { await handle?.close().catch(() => {}); }
}

/** @param {string} value */
const clean = (value) => value.replace(/^["']|["']$/g, '').replace(/\p{Cc}/gu, ' ').replace(/\s+/g, ' ').trim().slice(0, 160);

/** Description from the bounded YAML header. @param {string} text */
function headerDescription(text) {
  const header = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  const line = header?.match(/^description:[ \t]*([^\r\n]*)$/m)?.[1]?.trim();
  // YAML block scalars (`|`, `>`, `>-`) keep the text on the following indented lines.
  const block = line !== undefined && /^[|>][+-]?$|^$/.test(line)
    ? header?.match(/^description:[^\r\n]*\r?\n((?:[ \t]+[^\r\n]*\r?\n?)+)/m)?.[1]?.split(/\r?\n/).map((part) => part.trim()).filter(Boolean).join(' ')
    : line;
  return block ? clean(block) : null;
}

/** First descriptive paragraph after a `# title`, skipping activation boilerplate.
 * @param {string} text @param {RegExp} [after] */
function paragraphDescription(text, after = /^#\s+\S.*$/m) {
  const start = text.search(after);
  if (start < 0) return null;
  const rest = text.slice(start).split(/\r?\n/).slice(1);
  for (const paragraph of rest.join('\n').split(/\n\s*\n/)) {
    const value = paragraph.trim();
    if (!value || /^(?:#|```|>|Use this skill|Follow ALL|Then,|First,)/i.test(value) || /^[A-Z][A-Z-]{4,}:/.test(value)) continue;
    return clean(value);
  }
  return null;
}

const GENERIC = /^Migrated source command\b/i;
/** @param {string} value */
const flat = (value) => value.toLowerCase().replace(/[^a-z0-9]/g, '');

/** Real text for a migrated command wrapper: `squads/<squad>/skill.md` (frontmatter or first
 * paragraph), then the command template kept in the wrapper itself. Paths stay local; only
 * the text is used. Adapt the `squads` directory convention to whatever your own harness uses
 * for grouping commands, if any.
 * @param {string} id @param {string} text @param {string | null} root */
async function squadDescription(id, text, root) {
  const rest = id.replace(/^source-command-/, '');
  const squad = rest.split(/-(?:agents|tasks)-/)[0];
  /** @type {string | null} */
  let fromSkill = null;
  if (root) {
    try {
      const match = (await readdir(join(root, 'squads'), { withFileTypes: true }))
        .find((entry) => entry.isDirectory() && flat(entry.name) === flat(squad));
      const body = match ? await head(join(root, 'squads', match.name, 'skill.md')) : null;
      if (body) fromSkill = headerDescription(body) ?? paragraphDescription(body);
    } catch { /* no squads directory */ }
  }
  // Codex/Grok wrappers only point to the project copy, which keeps the command template.
  const project = root && !/^## Command Template\s*$/m.test(text) ? await head(join(root, '.agents/skills', id, 'SKILL.md')) : null;
  const fromTemplate = paragraphDescription(project ?? text, /^## Command Template\s*$/m);
  // The whole group: its skill.md. An agent or task inside it: its own template first.
  return rest === squad ? fromSkill ?? fromTemplate : fromTemplate ?? fromSkill;
}

/** Read only the bounded header, never include the skill body in a catalog.
 * @param {string} path @param {string} id @param {string | null} [root] */
async function skillDescription(path, id, root = null) {
  const text = await head(path);
  if (!text) return null;
  const description = headerDescription(text);
  // Without a real one-line definition the skill is not offered as a candidate.
  if (!description) return null;
  if (GENERIC.test(description)) return (await squadDescription(id, text, root)) ?? description;
  return description;
}

/** @param {string} cwd */
async function projectRoot(cwd) {
  if (!isAbsolute(cwd)) return null;
  let path = resolve(cwd);
  for (let depth = 0; depth < 8; depth += 1) {
    if (await isFile(join(path, 'AGENTS.md')) || await isFile(join(path, '.git'))) return path;
    try { if ((await stat(join(path, '.git'))).isDirectory()) return path; } catch { /* absent */ }
    const parent = dirname(path);
    if (parent === path) break;
    path = parent;
  }
  return null;
}

/** Catalogs are a bounded shortlist, not a claim of exhaustive discovery. IDs and
 * short public skill metadata are sent; paths and file bodies stay local.
 * @param {{harness:string,text?:string}} event
 * @param {{cwd?:string,env?:Record<string,string|undefined>,home?:string}} [options] */
export async function loadCatalog(event, { cwd = process.cwd(), env = process.env, home = homedir() } = {}) {
  const root = await projectRoot(cwd);
  const roots = event.harness === 'codex'
    ? [join(env.CODEX_HOME || join(home, '.codex'), 'skills'), join(home, '.agents/skills')]
    : event.harness === 'claude'
      ? [join(env.CLAUDE_CONFIG_DIR || join(home, '.claude'), 'skills'), join(home, '.agents/skills')]
      : [join(env.GROK_HOME || join(home, '.grok'), 'skills')];
  if (root) roots.push(join(root, '.agents/skills'), join(root, event.harness === 'grok' ? '.grok/skills' : event.harness === 'claude' ? '.claude/skills' : '.codex/skills'));
  // Grok's compatibility may be disabled; its foreign directories are omitted.
  const entries = new Map();
  for (const directory of roots) {
    let names;
    try { names = await readdir(directory, { withFileTypes: true }); } catch { continue; }
    for (const entry of names) {
      if ((!entry.isDirectory() && !entry.isSymbolicLink()) || !/^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}$/.test(entry.name) || entry.name === 'none') continue;
      if (!entries.has(entry.name)) entries.set(entry.name, join(directory, entry.name, 'SKILL.md'));
    }
  }
  const query = new Set(words(event.text ?? ''));
  const shortlist = [...entries].sort(([a], [b]) => score(b, query) - score(a, query) || a.localeCompare(b)).slice(0, MAX_SKILL_HEADERS);
  const described = (await Promise.all(shortlist.map(async ([id, path]) => {
    const description = await skillDescription(path, id, root);
    return description ? { id, description, relevance: 0 } : null;
  }))).filter((skill) => skill !== null).map((skill) => ({ ...skill, relevance: relevance(skill, query) }));
  // Relevance first: only when no skill shares a word with the request does the plain
  // alphabetical list stay, so the skill question keeps running as before.
  const relevant = described.filter((skill) => skill.relevance > 0);
  const skills = (relevant.length ? relevant : described)
    .sort((a, b) => b.relevance - a.relevance || a.id.localeCompare(b.id)).slice(0, MAX_SKILLS)
    .map(({ id, description }) => ({ id, description }));
  const personas = [];
  if (root) {
    // Adjust this directory to wherever your own harness keeps per-role agent
    // definitions (one `<id>.md` file per persona); it is optional.
    for (const [id, description] of Object.entries(ROLE_DESCRIPTIONS)) {
      if (await isFile(join(root, '.team-roles/agents', `${id}.md`))) personas.push({ id, description });
    }
  }
  return { ...(skills.length ? { skills } : {}), tools: TOOL_FAMILIES.map((tool) => ({ ...tool })), ...(personas.length ? { personas } : {}) };
}

/** Preserve explicit user skill/persona invocations instead of recommending an
 * alternative from the catalog. No inference of authorization is made here.
 * @param {string} text @param {Array<{id:string}>|undefined} candidates */
export function hasExplicitInvocation(text, candidates) {
  return (candidates ?? []).some(({ id }) => {
    const escaped = id.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return new RegExp(`(?:^|\\s)(?:[@/$](?:role-)?${escaped})(?=$|[\\s.,!?:])`, 'i').test(text)
      || new RegExp(`(?:ativa[r]?|ative|use|activate)\\s+(?:a\\s+|o\\s+)?(?:persona\\s+|agente\\s+|skill\\s+)?${escaped}(?=$|[\\s.,!?:])`, 'i').test(text);
  });
}
