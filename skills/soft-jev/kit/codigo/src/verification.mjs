// "Pronto sem prova" em código (estudo v3, seção 3.4). É regra, não julgamento: nada aqui chama a API.
// Os adaptadores classificam a ferramenta localmente e mandam só o tipo de verificação (enum),
// nunca o comando. O texto final é lido só neste processo e não é gravado.

/** @typedef {'git'|'http'|'test'|'read'} VerifyKind */
export const VERIFY_KINDS = /** @type {const} */ (['git', 'http', 'test', 'read']);

// Mesmos padrões em hermes-plugin/jev-auto/automation.py (`verification_kinds`); os casos de
// test/verification-cases.json rodam nos dois lados.
const COMMAND_KINDS = /** @type {Array<[VerifyKind, RegExp]>} */ ([
  ['git', /\b(?:git\s+(?:push|log|show|status|rev-parse|ls-remote|fetch|diff)|gh\s+(?:pr|run|api|release|repo))\b/i],
  ['test', /\b(?:(?:npm|pnpm|yarn|bun)\s+(?:run\s+)?(?:test|lint|typecheck|build|check|house:check|validate[\w:-]*|smoke)|node\s+--test|pytest|unittest|go\s+test|cargo\s+test|make\s+(?:test|check)|vitest|jest|tsc|eslint|runtime_hooks\.py)\b/i],
  ['http', /\b(?:curl|wget|httpie|lynx)\b/i],
  ['read', /(?:^|[;&|(]\s*)(?:cat|head|tail|less|sed\s+-n|grep|rg|ls|diff|stat|wc|jq|find)\b/i],
]);
const SHELL_TOOLS = new Set(['bash', 'shell', 'exec_command', 'run_terminal_command', 'run_terminal_cmd', 'terminal',
  'local_shell', 'execute_command', 'container.exec']);
const READ_TOOLS = new Set(['read', 'read_file', 'view', 'view_file', 'grep', 'glob', 'search_files', 'list_dir', 'ls',
  'file_search', 'notebookread']);
const HTTP_TOOLS = new Set(['webfetch', 'web_fetch', 'web_extract', 'fetch', 'browser_navigate', 'browser_snapshot',
  'browser_take_screenshot', 'browser_screenshot', 'browser_vision', 'screenshot']);

/** @param {string} toolName */
const leaf = (toolName) => toolName.split(/__|[.:/]/).at(-1)?.toLowerCase() ?? '';

/**
 * Tipos de verificação que uma ferramenta concluída representa. Só o resultado sai daqui.
 * @param {unknown} toolName @param {unknown} [command] @returns {VerifyKind[]}
 */
export function verificationKinds(toolName, command) {
  if (typeof toolName !== 'string' || !toolName) return [];
  const name = leaf(toolName);
  if (READ_TOOLS.has(name)) return ['read'];
  if (HTTP_TOOLS.has(name)) return ['http'];
  if (!SHELL_TOOLS.has(name) && !SHELL_TOOLS.has(toolName.toLowerCase())) return [];
  const text = Array.isArray(command) ? command.filter((part) => typeof part === 'string').join(' ')
    : typeof command === 'string' ? command : '';
  if (!text) return [];
  const bounded = text.slice(0, 4_096);
  return COMMAND_KINDS.filter(([, pattern]) => pattern.test(bounded)).map(([kind]) => kind);
}

/** @typedef {'git'|'live'|'tests'|'done'} ClaimKind */
const CLAIMS = /** @type {Array<[ClaimKind, RegExp]>} */ ([
  ['git', /\b(?:commitad[oa]s?|commitei|fiz (?:o )?commit|push(?:ei|ado|ados)|dei (?:o )?push|subi (?:pr[oa]|para o|no|na) (?:github|main|origin)|na origin\/main|committed|pushed)\b/gi],
  ['live', /\b(?:no ar|publicad[oa]s?|publiquei|deployad[oa]s?|fiz (?:o )?deploy|em produ[cç][aã]o|est[aá] live|deployed|is live)\b/gi],
  ['tests', /\b(?:testes? (?:passa(?:m|ram|ndo)?|verdes?)|todos os testes|gates? (?:verdes?|passa(?:m|ram|ndo)?)|tests? pass(?:ed|ing|es)?|all tests)\b/gi],
  // "feito", "resolvido" e "done" ficaram de fora: no WhatsApp são resposta de conversa, não entrega.
  ['done', /\b(?:conclu[ií]d[oa]s?|conclu[ií]|pront[oa]s?|entregue|entreguei|finalizad[oa]s?|corrigid[oa]s?|consertad[oa]s?|funcionando|completed|fixed)\b/gi],
]);
/** Qual verificação conta para cada tipo de afirmação. */
export const REQUIRED = /** @type {Record<ClaimKind, VerifyKind[]>} */ ({
  git: ['git'], live: ['http'], tests: ['test'], done: ['git', 'http', 'test', 'read'],
});
const NEGATION = /(?:\bn[aã]o|\bnunca|\bainda|\bsem|\bnot|\bisn't|\bnever|\bwhen|\bquando|\bse)\s+(?:\S+\s+){0,2}$/i;

/**
 * Afirmações de fim ("pronto", "no ar", "commitado", "testes passam") no texto final.
 * Negação logo antes ("ainda não está pronto") e perguntas não contam.
 * @param {unknown} text @returns {ClaimKind[]}
 */
export function completionClaims(text) {
  if (typeof text !== 'string' || !text.trim()) return [];
  const bounded = text.slice(0, 64_000);
  /** @type {ClaimKind[]} */
  const found = [];
  for (const [kind, pattern] of CLAIMS) {
    for (const match of bounded.matchAll(pattern)) {
      const before = bounded.slice(Math.max(0, (match.index ?? 0) - 40), match.index);
      const sentenceEnd = bounded.slice(match.index).search(/[.!?\n]/);
      const isQuestion = sentenceEnd >= 0 && bounded[(match.index ?? 0) + sentenceEnd] === '?';
      if (!NEGATION.test(before) && !isQuestion) { found.push(kind); break; }
    }
  }
  return found;
}

/** @typedef {{git: number, http: number, test: number, read: number}} VerifyCounts */
/** @returns {VerifyCounts} */
export const emptyVerify = () => ({ git: 0, http: 0, test: 0, read: 0 });

const LABELS = /** @type {Record<ClaimKind, [string, string]>} */ ({
  git: ['commitado/no GitHub', 'git log/push'],
  live: ['no ar/publicado', 'curl ou abrir a página'],
  tests: ['testes passando', 'rodar os testes'],
  done: ['pronto/concluído', 'teste, leitura, curl ou git'],
});

/**
 * Commit, deploy e testes afirmados sem a verificação correspondente contam sempre. "Pronto" genérico
 * só conta quando o turno fez alguma coisa (ferramenta): sem nenhuma, costuma ser "Pronto! Aqui está…".
 * @param {unknown} text
 * @param {{verify?: Partial<VerifyCounts>, seq?: number, last_write?: number, last_verify?: number}} evidence
 * @returns {{claims: ClaimKind[], missing: ClaimKind[], edited_after_verify: boolean, note?: string}}
 */
export function checkCompletion(text, evidence) {
  const claims = completionClaims(text);
  const verify = { ...emptyVerify(), ...(evidence.verify || {}) };
  const acted = (evidence.seq || 0) > 0;
  const missing = claims.filter((claim) => (claim !== 'done' || acted) && !REQUIRED[claim].some((kind) => verify[kind] > 0));
  const editedAfterVerify = claims.length > 0 && (evidence.last_write || 0) > (evidence.last_verify || 0);
  const result = { claims, missing, edited_after_verify: editedAfterVerify };
  if (!missing.length) return result;
  // "done" repete o que um tipo mais específico já disse.
  const shown = missing.length > 1 ? missing.filter((claim) => claim !== 'done') : missing;
  const said = shown.map((claim) => LABELS[claim][0]).join(', ');
  const needed = shown.map((claim) => LABELS[claim][1]).join('; ');
  return { ...result, note: `JEV (checagem em código): a última resposta disse ${said} sem verificação correspondente no turno (faltou: ${needed}). Confira antes de reafirmar ou de seguir em cima disso.` };
}
