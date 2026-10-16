// Monta <projeto>/index.html a partir de src/index.template.html, da transcrição e do perfil do dono.
// Rode na raiz do projeto: node <skill>/scripts/montar-index.mjs
// Lê:
//   assets/transcricao.json   transcrição do limpo.mp4, com tempo por palavra
//   assets/correcoes.json     {"palavra errada": "certa", "palavra-que-sai": ""}  (vale para toda ocorrência)
//      correção num tempo só: {"_em": [{"em": 59.5, "para": "dou"}, {"em": 120.1, "juntar": 2, "para": "agente"}]}
//      (a palavra mais próxima de "em", até 0,3 s; "juntar" funde essa palavra com as seguintes numa só)
//   assets/destaques.json     {"palavras": ["pausa"], "em": [12.4], "pequeno": [[3.6, 6.2]], "ocultar": [[0.0, 3.6]]}
//      palavras -> toda ocorrência vai no serifado itálico, na cor de acento;  em -> só a palavra mais próxima daquele tempo (até 0,3 s)
//      pequeno -> trechos em que a legenda cai para o tamanho de aparte;  ocultar -> trechos sem legenda
//      (use ocultar enquanto uma pilha de frase ou um elemento de tela cheia carrega as palavras)
//   ajustes.json              {"altura_legenda": 1330}
//   perfil.json               procurado na pasta do projeto e subindo: cor_acento, fonte_texto, fonte_destaque
// Sem cor_acento no perfil, o destaque sai em branco (só a troca de fonte marca a palavra).
import { readFileSync, writeFileSync, existsSync, copyFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { extname, isAbsolute, join, dirname } from "node:path";
import { lerPerfil } from "./ferramentas.mjs";

const ler = (p, padrao) => (existsSync(p) ? JSON.parse(readFileSync(p, "utf8").replace(/^﻿/, "")) : padrao);
const t = ler("assets/transcricao.json", null);
if (!t) { console.error("falta assets/transcricao.json (transcreva o limpo.mp4 antes)"); process.exit(1); }
// Duração: a do limpo.mp4 medida com ffprobe (a da transcrição pode passar uns décimos e o motor avisa).
const medirLimpo = () => { try { return Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/limpo.mp4"], { encoding: "utf8" }).trim()); } catch { return NaN; } };
const durLimpo = medirLimpo();
const dur = Number.isFinite(durLimpo) && durLimpo > 0 ? durLimpo : t.audio_duration_secs;
const fix = ler("assets/correcoes.json", {});
const fixar = (t) => { if (t in fix) return fix[t]; const m = t.match(/^(.*?)([.,;:!?…]+)$/); return m && m[1] in fix ? (fix[m[1]] ? fix[m[1]] + m[2] : "") : t; };
const em = { palavras: [], em: [], pequeno: [], ocultar: [], ...ler("assets/destaques.json", {}) };
const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9%]/g, "");
const emWords = new Set(em.palavras.map(norm));
const dentro = (x, rs) => rs.some(([a, b]) => x >= a && x < b);

// ---- identidade do dono
const { caminho: perfilPath, dados: perfil } = lerPerfil();
const hex = /^#[0-9a-fA-F]{6}$/;
let acento = "#ffffff";
if (perfil.cor_acento) {
  if (hex.test(perfil.cor_acento)) acento = perfil.cor_acento;
  else { console.error(`cor_acento inválida no perfil (${perfil.cor_acento}); use #RRGGBB`); process.exit(1); }
}
const formato = { ".woff2": "woff2", ".woff": "woff", ".ttf": "truetype", ".otf": "opentype" };
mkdirSync("assets/fonts", { recursive: true });
// Fonte do dono, se declarada, é copiada para assets/fonts/; senão fica a livre que vem com a skill.
const fonteDoDono = (campo, nome) => {
  const f = perfil[campo];
  if (!f) return null;
  const abs = isAbsolute(f) ? f : join(dirname(perfilPath), f);
  const ext = extname(abs).toLowerCase();
  if (!existsSync(abs) || !formato[ext]) { console.error(`${campo} não encontrada ou formato fora de woff2/woff/ttf/otf: ${f}`); process.exit(1); }
  copyFileSync(abs, `assets/fonts/${nome}${ext}`);
  return `url("assets/fonts/${nome}${ext}") format("${formato[ext]}")`;
};
const sansDono = fonteDoDono("fonte_texto", "dono-texto");
const serifDono = fonteDoDono("fonte_destaque", "dono-destaque");
const fontes = [
  sansDono ? `@font-face{font-family:"EdSans";src:${sansDono};font-weight:500 600}`
    : `@font-face{font-family:"EdSans";src:url("assets/fonts/Inter-SemiBold.ttf") format("truetype");font-weight:600}\n@font-face{font-family:"EdSans";src:url("assets/fonts/Inter-Medium.ttf") format("truetype");font-weight:500}`,
  serifDono ? `@font-face{font-family:"EdSerif";src:${serifDono};font-style:italic}`
    : `@font-face{font-family:"EdSerif";src:url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2");font-style:italic}`,
  `@font-face{font-family:"EdHand";src:url("assets/fonts/Caveat-Bold.woff2") format("woff2")}`,
].join("\n");

// ---- palavras (junta divisões da transcrição como "e" + "-mail" e "100" + "%")
const palavraMaisPerto = (lista, x, max) => { let b = -1, bd = 1e9; lista.forEach((w, i) => { const d = Math.abs(w.start - x); if (d < bd) { bd = d; b = i; } }); return bd <= max ? b : -1; };
const noTempo = new Map();
for (const c of (Array.isArray(fix._em) ? fix._em : [])) { const k = palavraMaisPerto(t.words, c.em, 0.3); if (k >= 0) noTempo.set(k, c); }
const words = [];
for (let i = 0; i < t.words.length; i++) {
  const w = t.words[i], n = t.words[i + 1];
  if (noTempo.has(i)) {
    const c = noTempo.get(i), qtd = Math.max(1, c.juntar || 1), ultima = t.words[Math.min(i + qtd - 1, t.words.length - 1)];
    if (c.para) words.push({ text: c.para, start: w.start, end: ultima.end });
    i += qtd - 1; continue;
  }
  if (n && (n.text.startsWith("-") || n.text === "%")) { words.push({ text: w.text + n.text, start: w.start, end: n.end }); i++; continue; }
  const txt = fixar(w.text);
  if (txt) words.push({ text: txt, start: w.start, end: w.end });
}

// destaque por tempo: só a palavra mais próxima de cada tempo pedido (não as vizinhas)
const idxEm = new Set(em.em.map((x) => palavraMaisPerto(words, x, 0.3)).filter((k) => k >= 0));

// ---- um clipe de legenda por palavra (do início dela até a próxima, no máximo 1,0 s)
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
let nDestaques = 0;
const caps = words.map((w, i) => {
  if (dentro(w.start, em.ocultar)) return "";
  const prox = words[i + 1] ? words[i + 1].start : dur;
  const d = Math.min(prox - w.start, 1.0);
  if (d <= 0.01) return "";
  const cls = ["w", "clip"];
  if (emWords.has(norm(w.text)) || idxEm.has(i)) { cls.push("em"); nDestaques++; }
  if (dentro(w.start, em.pequeno)) cls.push("sm");
  return `<div class="${cls.join(" ")}" id="w${i}" data-start="${w.start.toFixed(3)}" data-duration="${d.toFixed(3)}" data-track-index="5">${esc(w.text.toLowerCase())}</div>`;
}).filter(Boolean).join("\n");

const JANELA = 1096; // janela de render; o renderizar.mjs recorta para 1080
const cfg = { altura_legenda: 1330, ...ler("ajustes.json", {}) };
const html = readFileSync("src/index.template.html", "utf8")
  .replace("/*__FONTES__*/", fontes).replace("__ACENTO__", acento)
  .replaceAll("__DUR__", dur.toFixed(3)).replaceAll("__JANELA__", String(JANELA)).replace("__CAPTIONS__", caps).replace("__CAP_TOP__", String(cfg.altura_legenda));
writeFileSync("index.html", html);
const meta = ler("meta.json", {});
Object.assign(meta, { id: "reel", width: JANELA, height: 1920, fps: 30 });
writeFileSync("meta.json", JSON.stringify(meta, null, 2) + "\n");
console.log(`index.html montado: ${dur.toFixed(2)}s, ${words.length} palavras, ${nDestaques} em destaque, acento ${acento}` +
  `${perfilPath ? "" : " (sem perfil.json: só branco)"}, fontes ${sansDono ? "do dono" : "livres da skill"}/${serifDono ? "do dono" : "livres da skill"}`);
