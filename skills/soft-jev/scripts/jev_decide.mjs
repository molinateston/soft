#!/usr/bin/env node
// jev_decide.mjs: uma decisao do Jev (TypeSafe) pelo OpenRouter, em qualquer harness. Node 18+.
// Uso:  node jev_decide.mjs '{"state": {...}, "questions": {...}}'   ou por stdin.
// Chave: OPENROUTER_API_KEY no ambiente, ou o arquivo apontado por JEV_KEY_FILE (linha OPENROUTER_API_KEY=...).
// Saida: JSON {available: true, answers, usage, ms} ou {available: false, reason}.
// Nunca imprime a chave, nunca repete sozinho, prazo de 2 s.
// Tambem exporta decide(state, questions) pra quem quiser importar.
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const URL_JEV = process.env.JEV_URL || 'https://openrouter.ai/api/alpha/decisions';
const MODEL = process.env.JEV_MODEL || 'typesafe/jev-1.13';
const TIMEOUT_MS = Number(process.env.JEV_TIMEOUT_MS || 2000);
const LIMITE_BYTES = 48000;
const CAMPO_SEGREDO = /(password|senha|api[_-]?key|access[_-]?token|authorization|secret|private[_-]?key)/i;
const CREDENCIAL = /(-----BEGIN .{0,30}PRIVATE KEY|\b(?:sk-|ghp_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{12,}|\beyJ[A-Za-z0-9_-]{20,}\.)/i;

function chave() {
  if (process.env.OPENROUTER_API_KEY) return process.env.OPENROUTER_API_KEY;
  const arquivo = process.env.JEV_KEY_FILE;
  if (!arquivo) return '';
  try {
    for (const linha of readFileSync(arquivo, 'utf8').split('\n')) {
      if (linha.startsWith('OPENROUTER_API_KEY=')) return linha.slice(19).trim().replace(/^['"]|['"]$/g, '');
    }
  } catch {}
  return '';
}

const numero = (v) => typeof v === 'number' && Number.isFinite(v);

function temCampoSegredo(v) {
  if (Array.isArray(v)) return v.some(temCampoSegredo);
  if (v && typeof v === 'object') return Object.entries(v).some(([k, x]) => CAMPO_SEGREDO.test(k) || temCampoSegredo(x));
  return false;
}

function confere(state, questions) {
  if (!questions || typeof questions !== 'object' || Array.isArray(questions)) throw new Error('questions');
  const nomes = Object.keys(questions);
  if (nomes.length < 1 || nomes.length > 32) throw new Error('de 1 a 32 perguntas');
  for (const n of nomes) {
    const p = questions[n];
    if (!/^[a-z][a-z0-9_]{0,47}$/.test(n) || !p || !['choice', 'noul', 'score'].includes(p.type)) throw new Error('pergunta mal formada: ' + n.slice(0, 40));
    if (p.type === 'choice' && (!p.criteria || typeof p.criteria !== 'object' || Array.isArray(p.criteria) || Object.keys(p.criteria).length < 2)) throw new Error('choice precisa de 2 a 100 opcoes');
    if (p.type === 'score' && (!Array.isArray(p.criteria) || p.criteria.length < 2 || p.criteria.length > 10)) throw new Error('score precisa de 2 a 10 niveis');
  }
  const corpo = JSON.stringify({ state, questions });
  if (temCampoSegredo(state) || CREDENCIAL.test(corpo)) throw new Error('segredo no estado');
  if (Buffer.byteLength(corpo) > LIMITE_BYTES) throw new Error('acima de 48 KB');
}

function valida(data, questions) {
  if (!data || !String(data.model || '').startsWith(MODEL)) throw new Error('model');
  const r = data.answers;
  if (!r || Object.keys(r).sort().join() !== Object.keys(questions).sort().join()) throw new Error('questions');
  for (const [n, p] of Object.entries(questions)) {
    const a = r[n];
    if (!a || a.type !== p.type) throw new Error('type');
    if (p.type === 'noul' && !(numero(a.noul) && a.noul >= 0 && a.noul <= 1)) throw new Error('noul');
    if (p.type === 'choice' && (!(a.choice in p.criteria) || !numero(a.confidence))) throw new Error('choice');
    if (p.type === 'score' && !(numero(a.score) && numero(a.confidence))) throw new Error('score');
  }
  return r;
}

export async function decide(state, questions) {
  try { confere(state, questions); } catch (e) { return { available: false, reason: 'pedido_invalido', detail: String(e.message).slice(0, 80) }; }
  const k = chave();
  if (!k) return { available: false, reason: 'missing_key' };
  const t0 = Date.now();
  try {
    const resp = await fetch(URL_JEV, {
      method: 'POST',
      headers: { Authorization: `Bearer ${k}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: MODEL, state, questions }),
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!resp.ok) return { available: false, reason: 'api_error', status: resp.status, ms: Date.now() - t0 };
    const data = await resp.json();
    const answers = valida(data, questions);
    return { available: true, model: data.model, answers, usage: data.usage, ms: Date.now() - t0, advisory_only: true };
  } catch (e) {
    const motivo = e && (e.name === 'TimeoutError' || e.name === 'AbortError') ? 'timeout' : 'invalid_response';
    return { available: false, reason: motivo, ms: Date.now() - t0 };
  }
}

async function principal() {
  let bruto = process.argv[2];
  if (!bruto) { bruto = ''; for await (const pedaco of process.stdin) bruto += pedaco; }
  let pedido;
  try { pedido = JSON.parse(bruto); } catch { console.log(JSON.stringify({ available: false, reason: 'pedido_invalido', detail: 'JSON invalido' })); return; }
  if (!pedido || typeof pedido !== 'object' || Object.keys(pedido).sort().join() !== 'questions,state') {
    console.log(JSON.stringify({ available: false, reason: 'pedido_invalido', detail: 'formato esperado: {state, questions}' }));
    return;
  }
  console.log(JSON.stringify(await decide(pedido.state, pedido.questions)));
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) principal();
