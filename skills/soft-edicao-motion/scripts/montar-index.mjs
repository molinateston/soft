// Monta <projeto>/index.html a partir de src/index.template.html, src/cenas.json e assets/transcript.json.
// Rode na raiz do projeto:  node <skill>/scripts/montar-index.mjs
// - legenda: grupos curtos (até 4 palavras e 23 letras), a palavra falada na cor de acento, na fonte da legenda
//   correções em assets/caption-fixes.json: {"errada": "certa", "apaga-esta": ""}
//   ou {"frases": [{"de": "sempre sendo", "para": "100%"}]} para trocar uma sequência inteira
// - cenas: src/cenas.json vai inteiro para window.CENAS; o kit (assets/motion-kit.js) desenha cada uma
// - identidade e enquadramento: reel.json (acento, fontes, capY, camZoom, camOrigemY, rosto)
// Confere o mapa antes de montar: tipo conhecido, tempos dentro do vídeo, cena sem sobrepor outra de takeover.
import { readFileSync, writeFileSync, existsSync, copyFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const skill = join(dirname(fileURLToPath(import.meta.url)), "..");
const t = JSON.parse(readFileSync("assets/transcript.json", "utf8"));
const dur = t.audio_duration_secs;
const fixRaw = existsSync("assets/caption-fixes.json") ? JSON.parse(readFileSync("assets/caption-fixes.json", "utf8")) : {};
const fixar = (t) => { if (t in fix) return fix[t]; const m = t.match(/^(.*?)([.,;:!?…]+)$/); return m && m[1] in fix ? (fix[m[1]] ? fix[m[1]] + m[2] : "") : t; };
const frases = fixRaw.frases || [];
const fix = Object.fromEntries(Object.entries(fixRaw).filter(([k]) => k !== "frases"));
const cfg = { capY: 1490, capTam: 41, capMax: 4, capLetras: 23, acento: "", fonteTitulo: "assets/fonts/titulo.otf", fonteLegenda: "assets/fonts/legenda.ttf", ...(existsSync("reel.json") ? JSON.parse(readFileSync("reel.json", "utf8")) : {}) };
const cenas = JSON.parse(readFileSync("src/cenas.json", "utf8"));
for (const f of [cfg.fonteTitulo, cfg.fonteLegenda]) if (!existsSync(f)) { console.error(`FALTA a fonte ${f} (rode o novo-reel.mjs ou ajuste o reel.json)`); process.exit(1); }
copyFileSync(join(skill, "template", "motion-kit.js"), "assets/motion-kit.js"); // sempre a versão da skill (vai embutido no index.html)

// ---- palavras: junta pedaços ("e" + "-mail", "100" + "%"), aplica as correções
const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9%]/g, "");
let words = [];
for (let i = 0; i < t.words.length; i++) {
  const w = t.words[i], n = t.words[i + 1];
  if (n && (n.text.startsWith("-") || n.text === "%")) { words.push({ text: w.text + n.text, start: w.start, end: n.end }); i++; continue; }
  words.push({ text: w.text, start: w.start, end: w.end });
}
for (const f of frases) {
  const de = f.de.split(/\s+/).map(norm);
  for (let i = 0; i + de.length <= words.length; i++) {
    if (!de.every((x, j) => norm(words[i + j].text) === x)) continue;
    const pont = (words[i + de.length - 1].text.match(/[,.?!]+$/) || [""])[0];
    const para = f.para ? f.para.split(/\s+/) : [];
    const s0 = words[i].start, s1 = words[i + de.length - 1].end, passo = (s1 - s0) / Math.max(1, para.length);
    // a frase nova ocupa o mesmo tempo da errada, dividido igual entre as palavras
    words.splice(i, de.length, ...para.map((p, j) => ({ text: p + (j === para.length - 1 && !/[,.?!]$/.test(p) ? pont : ""), start: +(s0 + j * passo).toFixed(3), end: +(s0 + (j + 1) * passo).toFixed(3) })));
    i += para.length - 1;
  }
}
words = words.map((w) => ({ ...w, text: fixar(w.text) })).filter((w) => w.text);

// ---- grupos: até capMax palavras e capLetras letras; quebra no fim de frase (. ? !) ou em respiro de 0,3 s
const caixaAlta = cfg.capCaixaAlta !== false;
const grupos = [];
let cur = [];
words.forEach((w, i) => {
  cur.push(w);
  const n = words[i + 1];
  const letras = cur.map((x) => x.text).join(" ").length;
  const fim = !n || /[.?!]$/.test(w.text) || n.start - w.end > 0.3 || cur.length >= cfg.capMax || letras + 1 + n.text.length > cfg.capLetras;
  if (fim) { grupos.push(cur); cur = []; }
});
// na abertura a headline fala por si: sem legenda até o fim dela (a menos que a cena peça "legenda": true)
const abert = (cenas.cenas || []).find((c) => c.tipo === "abertura");
if (abert && !abert.legenda) while (grupos.length && grupos[0][0].start < abert.ate - 0.05) grupos.shift();
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const caps = grupos.map((g, i) => {
  const de = g[0].start, prox = grupos[i + 1] ? grupos[i + 1][0].start : dur;
  const ate = Math.min(prox, g[g.length - 1].end + 1.2, dur);
  return `<div class="grp" data-de="${de.toFixed(3)}" data-ate="${ate.toFixed(3)}">${g.map((w) => `<span data-t="${w.start.toFixed(3)}">${esc(caixaAlta ? w.text.toLocaleUpperCase("pt-BR") : w.text)}</span>`).join(" ")}</div>`;
}).join("\n");

// ---- confere o mapa de cenas
const TIPOS = ["abertura", "arquivo", "timeline", "rede", "destino", "cartao", "tela", "chat", "celular", "anel", "mente", "agente", "niveis", "palavra"];
const TAKE = { abertura: false, timeline: false, rede: false, cartao: false };
const erros = [];
const lista = (cenas.cenas || []).slice().sort((a, b) => a.de - b.de);
lista.forEach((c, i) => {
  if (!TIPOS.includes(c.tipo)) erros.push(`cena ${i + 1}: tipo "${c.tipo}" não existe (${TIPOS.join(", ")})`);
  if (!(c.ate > c.de) || c.de < 0 || c.ate > dur + 0.01) erros.push(`cena ${i + 1} (${c.tipo}): tempos ${c.de}..${c.ate} fora de 0..${dur.toFixed(2)}`);
  const take = c.takeover != null ? c.takeover : TAKE[c.tipo] !== false;
  const ant = lista.slice(0, i).find((p) => p.ate > c.de + 0.01 && (p.takeover != null ? p.takeover : TAKE[p.tipo] !== false) && take);
  if (ant) erros.push(`cena ${i + 1} (${c.tipo}) começa em ${c.de} dentro do takeover ${ant.tipo} (${ant.de}..${ant.ate}): encadeie (de = ate da anterior)`);
});
if (erros.length) { console.error(erros.join("\n")); process.exit(1); }

// ---- identidade
const acento = /^#[0-9a-fA-F]{6}$/.test(cfg.acento || "") ? cfg.acento : "#ffffff"; // sem identidade: só branco
const reel = { acento, capY: cfg.capY, camZoom: cfg.camZoom || 1, camOrigemY: cfg.camOrigemY ?? 960, aberturaCamY: cfg.aberturaCamY ?? 490, rosto: cfg.rosto };
const ab = lista.find((c) => c.tipo === "abertura");
// headline cabe em 960 px: largura média medida da fonte do título padrão = 0,52 do tamanho por letra
const maiorLinha = Math.max(1, ...(ab?.linhas || []).map((l) => l.replace(/\*/g, "").length));
const tamHeadline = Math.min(ab?.tam ?? 89, Math.floor(960 / (maiorLinha * 0.52)));
if (ab && tamHeadline < (ab.tam ?? 89)) console.log(`headline reduzida para ${tamHeadline} px para caber na largura`);
const html = readFileSync("src/index.template.html", "utf8").replaceAll("__DUR__", dur.toFixed(3)).replace("__CAPTIONS__", () => caps)
  .replace("__CAP_Y__", String(cfg.capY)).replace("__CAP_TAM__", String(cfg.capTam)).replace("__CTA_Y__", String(cenas.cta?.y ?? cfg.capY + 110))
  .replace("__HEADLINE_TAM__", String(tamHeadline))
  .replace("__FONTE_TITULO__", cfg.fonteTitulo).replace("__FONTE_LEGENDA__", cfg.fonteLegenda)
  .replace("__REEL__", () => JSON.stringify(reel)).replace("__CENAS__", () => JSON.stringify(cenas))
  .replace("__KIT__", () => readFileSync("assets/motion-kit.js", "utf8"));
writeFileSync("index.html", html);
const meta = existsSync("meta.json") ? JSON.parse(readFileSync("meta.json", "utf8")) : {};
Object.assign(meta, { id: "reel", width: 1096, height: 1920, fps: 30 });
writeFileSync("meta.json", JSON.stringify(meta, null, 2));
const take = lista.filter((c) => (c.takeover != null ? c.takeover : TAKE[c.tipo] !== false)).reduce((s, c) => s + c.ate - c.de, 0);
console.log(`index.html montado: ${dur.toFixed(2)}s, ${words.length} palavras em ${grupos.length} grupos de legenda, ${lista.length} cenas (${take.toFixed(1)}s de takeover, ${(100 * take / dur).toFixed(0)}% do vídeo), acento ${cfg.acento ? acento : "nenhum (branco)"}`);
