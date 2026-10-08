// Adaptado pro OpenRouter (ver ../ADAPTACAO-OPENROUTER.md). Para voltar à API direta da TypeSafe:
// JEV_ENDPOINT=https://api.typesafe.ai/v1/systemone JEV_MODEL=jev-1.13.0
export const MODEL = process.env.JEV_MODEL || 'typesafe/jev-1.13';
export const ENDPOINT = process.env.JEV_ENDPOINT || 'https://openrouter.ai/api/alpha/decisions';
/** O OpenRouter devolve o modelo com data (ex.: typesafe/jev-1.13-20260917): aceita o nome exato ou com sufixo. */
export const modelMatches = (value) => typeof value === 'string' && (value === MODEL || value.startsWith(`${MODEL}-`));
export const MAX_REQUEST_BYTES = 24_000;
export const MAX_RESPONSE_BYTES = 128_000;
export const MAX_QUESTIONS = 16;
export const NETWORK_TIMEOUT_MS = 2_000;

/** @param {unknown} value @returns {value is Record<string, unknown>} */
export function object(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
    && (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null);
}

/** @param {unknown} value @returns {value is number} */
const unit = (value) => typeof value === 'number' && Number.isFinite(value) && value >= 0 && value <= 1;

/** @param {unknown} value @param {number} [depth] @returns {value is import('./types.js').Json} */
function json(value, depth = 0) {
  if (depth > 32) return false;
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return true;
  if (typeof value === 'number') return Number.isFinite(value);
  if (Array.isArray(value)) return value.every((item) => json(item, depth + 1));
  return object(value) && Object.values(value).every((item) => json(item, depth + 1));
}

/** @param {unknown} value @returns {value is import('./types.js').Context} */
const context = (value) => (typeof value === 'string' || Array.isArray(value) || object(value)) && json(value);

/** @param {Record<string, unknown>} value @param {string[]} allowed */
const allowedKeys = (value, allowed) => Object.keys(value).every((key) => allowed.includes(key));

/** @param {unknown} args @returns {args is import('./types.js').Arguments} */
export function validArguments(args) {
  try {
    if (!object(args) || !allowedKeys(args, ['state', 'questions']) || !context(args.state) || !object(args.questions)) return false;
    const entries = Object.entries(args.questions);
    if (entries.length < 1 || entries.length > MAX_QUESTIONS) return false;
    for (const [id, q] of entries) {
      if (!id || id.length > 64 || !object(q) || !context(q.instructions)
        || !allowedKeys(q, ['type', 'instructions', 'criteria'])) return false;
      if (q.type === 'noul') {
        if (Object.hasOwn(q, 'criteria') && (!object(q.criteria)
          || !allowedKeys(q.criteria, ['true', 'false']) || Object.keys(q.criteria).length === 0
          || !Object.values(q.criteria).every(context))) return false;
      } else if (q.type === 'choice') {
        if (!object(q.criteria) || Object.keys(q.criteria).length < 2 || Object.keys(q.criteria).length > 255
          || Object.keys(q.criteria).some((key) => !key)
          || !Object.values(q.criteria).every((value) => value === null || context(value))) return false;
      } else if (q.type === 'score') {
        if (!Array.isArray(q.criteria) || q.criteria.length < 2 || q.criteria.length > 10 || !q.criteria.every(context)) return false;
      } else return false;
    }
    return Buffer.byteLength(JSON.stringify({ model: MODEL, ...args })) <= MAX_REQUEST_BYTES;
  } catch {
    return false;
  }
}

/** @param {unknown} value @param {string[]} keys @returns {Record<string, number>} */
function probabilities(value, keys) {
  if (!object(value) || Object.keys(value).length !== keys.length
    || !keys.every((key) => Object.hasOwn(value, key) && unit(value[key]))) throw new Error('schema');
  const normalized = Object.fromEntries(keys.map((key) => [key, /** @type {number} */ (value[key])]));
  // The provider rounds each probability to two decimals: the sum can drift by up to 0.005 per option
  // (0.99 with 21 options is valid). Floating point makes |0.99 - 1| slightly above 0.01, so allow an epsilon.
  const tolerance = Math.max(0.01, 0.005 * keys.length) + 1e-9;
  if (Math.abs(Object.values(normalized).reduce((sum, probability) => sum + probability, 0) - 1) > tolerance) throw new Error('schema');
  return normalized;
}

/**
 * Return only validated typed fields. In particular, do not echo arbitrary provider text.
 * @param {unknown} value
 * @param {import('./types.js').Arguments} args
 * @returns {{model: string, answers: Record<string, import('./types.js').Answer>, usage: import('./types.js').Usage}}
 */
export function normalizeResponse(value, args) {
  if (!object(value) || !modelMatches(value.model) || !object(value.answers)
    || Object.keys(value.answers).length !== Object.keys(args.questions).length || !object(value.usage)) throw new Error('schema');
  const { input_tokens: inputTokens, output_tokens: outputTokens } = value.usage;
  if (typeof inputTokens !== 'number' || !Number.isSafeInteger(inputTokens) || inputTokens < 0
    || typeof outputTokens !== 'number' || !Number.isSafeInteger(outputTokens) || outputTokens < 0) throw new Error('schema');
  /** @type {Record<string, import('./types.js').Answer>} */
  const answers = {};
  for (const [id, q] of Object.entries(args.questions)) {
    const a = Object.hasOwn(value.answers, id) ? value.answers[id] : undefined;
    if (!object(a) || a.type !== q.type) throw new Error('schema');
    /** @type {import('./types.js').Answer} */
    let answer;
    if (q.type === 'noul') {
      if (!unit(a.noul)) throw new Error('schema');
      answer = { type: 'noul', noul: a.noul };
    } else {
      if (!unit(a.confidence)) throw new Error('schema');
      if (q.type === 'choice') {
        if (typeof a.choice !== 'string' || !Object.hasOwn(q.criteria, a.choice)) throw new Error('schema');
        answer = { type: 'choice', choice: a.choice, probabilities: probabilities(a.probabilities, Object.keys(q.criteria)), confidence: a.confidence };
      } else {
        if (typeof a.score !== 'number' || !Number.isFinite(a.score) || a.score < 0 || a.score > q.criteria.length - 1
          || !object(a.legend) || Object.keys(a.legend).length !== q.criteria.length) throw new Error('schema');
        const keys = q.criteria.map((_, index) => String(index));
        if (!keys.every((key) => Object.hasOwn(/** @type {object} */ (a.legend), key)
          && context(/** @type {Record<string, unknown>} */ (a.legend)[key]))) throw new Error('schema');
        // Local criteria are authoritative; provider-generated descriptions are never forwarded.
        answer = { type: 'score', score: a.score, probabilities: probabilities(a.probabilities, keys),
          legend: Object.fromEntries(q.criteria.map((criterion, index) => [String(index), criterion])), confidence: a.confidence };
      }
    }
    Object.defineProperty(answers, id, { value: answer, enumerable: true });
  }
  return { model: MODEL, answers, usage: { input_tokens: inputTokens, output_tokens: outputTokens } };
}

const contextSchema = { anyOf: [{ type: 'string' }, { type: 'object' }, { type: 'array' }] };
export const INPUT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['state', 'questions'],
  properties: {
    state: { ...contextSchema, description: 'Only the minimal non-sensitive facts needed for the decisions.' },
    questions: {
      type: 'object', minProperties: 1, maxProperties: MAX_QUESTIONS,
      propertyNames: { minLength: 1, maxLength: 64 },
      additionalProperties: {
        oneOf: [
          { type: 'object', additionalProperties: false, required: ['type', 'instructions'], properties: {
            type: { const: 'noul' }, instructions: contextSchema,
            criteria: { type: 'object', minProperties: 1, additionalProperties: false, properties: { true: contextSchema, false: contextSchema } },
          } },
          { type: 'object', additionalProperties: false, required: ['type', 'instructions', 'criteria'], properties: {
            type: { const: 'choice' }, instructions: contextSchema,
            criteria: { type: 'object', minProperties: 2, maxProperties: 255, propertyNames: { minLength: 1 },
              additionalProperties: { anyOf: [...contextSchema.anyOf, { type: 'null' }] } },
          } },
          { type: 'object', additionalProperties: false, required: ['type', 'instructions', 'criteria'], properties: {
            type: { const: 'score' }, instructions: contextSchema,
            criteria: { type: 'array', minItems: 2, maxItems: 10, items: contextSchema },
          } },
        ],
      },
    },
  },
};
