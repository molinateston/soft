// Monta <projeto>/index.html do estilo Direto a partir de src/index.template.html e do reel.json.
// Rode na raiz do projeto:  node <skill>/scripts/montar-index.mjs
// Lê: reel.json (identidade, recorte, abertura, apoios, CTA), assets/transcript.json (do cortar.mjs) e,
//     se existir, assets/caption-fixes.json ({"errada": "certa", "apaga-esta": ""}).
// Escreve: index.html, meta.json e textos-tela.md (headline e CTA, para o lint da casa).
// Para com erro quando o plano quebra uma regra do estilo (apoio fora de 2 a 3 s, imagem faltando, fala não achada).
import { readFileSync, writeFileSync, existsSync } from "node:fs";

const erros = [], avisos = [];
const reel = JSON.parse(readFileSync("reel.json", "utf8"));
const t = JSON.parse(readFileSync("assets/transcript.json", "utf8"));
const dur = t.audio_duration_secs;
const fix = existsSync("assets/caption-fixes.json") ? JSON.parse(readFileSync("assets/caption-fixes.json", "utf8")) : {};
const fixar = (t) => { if (t in fix) return fix[t]; const m = t.match(/^(.*?)([.,;:!?…]+)$/); return m && m[1] in fix ? (fix[m[1]] ? fix[m[1]] + m[2] : "") : t; };
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9%]/g, "");
const f3 = (n) => (+n).toFixed(3);

// ---- palavras (junta pedaços que a transcrição separa, como "e" + "-mail" e "100" + "%")
const words = [];
for (let i = 0; i < t.words.length; i++) {
  const w = t.words[i], n = t.words[i + 1];
  if (n && (n.text.startsWith("-") || n.text === "%")) { words.push({ text: w.text + n.text, start: w.start, end: n.end }); i++; continue; }
  const txt = fixar(w.text);
  if (txt) words.push({ text: txt, start: w.start, end: w.end });
}
// tempo da primeira palavra da frase falada; ultima=true pega a última ocorrência (o pedido do CTA vem no fim)
const achar = (frase, depois = 0, ultima = false) => {
  const p = String(frase).split(/\s+/).map(norm).filter(Boolean), hits = [];
  for (let i = 0; i < words.length; i++) if (words[i].start >= depois && p.length && p.every((x, j) => words[i + j] && norm(words[i + j].text) === x)) hits.push(words[i].start);
  return hits.length ? (ultima ? hits.at(-1) : hits[0]) : null;
};

// ---- identidade
const acento = /^#[0-9a-fA-F]{6}$/.test(reel.acento || "") ? reel.acento : "#ffffff"; // sem identidade: só branco
const fonteTitulo = reel.fonteTitulo || "assets/fonts/Inter-Black.otf", fonteChamada = reel.fonteChamada || "assets/fonts/Inter-Bold.otf";
for (const f of [fonteTitulo, fonteChamada, "assets/fonts/JetBrainsMono-Regular.ttf"]) if (!existsSync(f)) erros.push(`fonte faltando: ${f} (rode o novo-reel.mjs ou ajuste o reel.json)`);

// ---- corpo: o take ampliado pelo recorte [largura, altura, x, y] em coordenadas do raw 1080x1920
const [cw, ch, cx, cy] = reel.corpo_recorte || [1080, 1920, 0, 0];
const s = 1080 / cw;
if (Math.abs(ch * s - 1920) > 2) avisos.push(`corpo_recorte ${cw}x${ch} não é 9:16; a imagem vai esticar ou sobrar`);
if (cx < 0 || cy < 0 || cx + cw > 1080 || cy + ch > 1920) erros.push("corpo_recorte sai do quadro 1080x1920");
const corpo = `left:${(-cx * s).toFixed(2)}px;top:${(-cy * s).toFixed(2)}px;width:${(1080 * s).toFixed(2)}px;height:${(1920 * s).toFixed(2)}px`;

// ---- abertura em painel
const ab = reel.abertura || null;
const abS = ab ? +(ab.segundos ?? 5) : 0;
let aberturaHtml = "", tempos = [];
const hlLinhas = [];
if (ab) {
  if (!existsSync(ab.imagem || "")) erros.push(`imagem da abertura faltando: ${ab.imagem}`);
  const linhas = (ab.linhas || []).filter(Boolean);
  if (!linhas.length || linhas.length > 2) erros.push("a headline da abertura tem 1 ou 2 linhas (abertura.linhas)");
  for (const l of linhas) {
    const limpa = l.replace(/\*/g, "");
    hlLinhas.push(limpa);
    if (limpa.length > 21) avisos.push(`linha da headline com ${limpa.length} caracteres (passa de 21): pode estourar 944 px a 89 px; encurte o texto, nunca a fonte`);
  }
  const hl = linhas.map((l) => esc(l).replace(/\*([^*]+)\*/g, '<span class="y">$1</span>')).join("<br>");
  const jy = ab.janela_y ?? cy;
  if (jy < 0 || jy > 986) erros.push("abertura.janela_y entre 0 e 986");
  const janela = `left:0;top:${986 - jy}px;width:1080px;height:1920px;clip-path:inset(${jy}px 0 ${1920 - 934 - jy}px 0)`;
  aberturaHtml = `  <div id="abertura">
    <video id="ab-cam" src="assets/clean.mp4" data-start="0" data-duration="${f3(abS)}" data-track-index="2" muted playsinline style="${janela}"></video>
    <img id="ab-img" src="${esc(ab.imagem)}" alt="">
    <div id="ab-faixa"><div id="ab-hl">${hl}</div></div>
  </div>`;
  tempos.push(`hide("#abertura", ${f3(abS)});`);
}

// ---- apoios: três, tela inteira, 2 a 3 s, ancorados na fala literal
const apoios = reel.apoios || [];
if (apoios.length !== 3) avisos.push(`o estilo pede 3 apoios; o plano tem ${apoios.length} (anote no relatório se foi pedido do dono)`);
const ocup = [];
const apoiosHtml = apoios.map((a, i) => {
  const ini = a.inicio ?? achar(a.fala || "", abS);
  const d = +(a.duracao ?? 2.5);
  if (ini == null) { erros.push(`apoio ${i + 1}: fala não encontrada na transcrição: "${a.fala}" (use o ancoras.mjs ou ponha "inicio")`); return ""; }
  if (!a.fala) erros.push(`apoio ${i + 1}: falta "fala" (o trecho literal que o apoio mostra)`);
  if (d < 2 || d > 3) erros.push(`apoio ${i + 1}: duração ${d}s fora de 2 a 3 s`);
  if (!existsSync(a.imagem || "")) erros.push(`apoio ${i + 1}: imagem faltando: ${a.imagem}`);
  if (ini < abS) erros.push(`apoio ${i + 1}: começa dentro da abertura`);
  if (ini + d > dur) erros.push(`apoio ${i + 1}: passa do fim do vídeo`);
  for (const [o0, o1] of ocup) if (ini < o1 && ini + d > o0) erros.push(`apoio ${i + 1}: encosta em outro apoio`);
  ocup.push([ini, ini + d]);
  a._ini = ini; a._d = d;
  tempos.push(`show("#ap${i + 1}", ${f3(ini)}); zoom("#ap${i + 1}", ${f3(ini)}, ${f3(d)}); hide("#ap${i + 1}", ${f3(ini + d)});`);
  return `  <img class="apoio" id="ap${i + 1}" src="${esc(a.imagem)}" alt="">`;
}).join("\n");

// ---- legenda: grupos de até 4 palavras, no máximo 2 linhas de 23 caracteres, palavra falada na cor de acento
const MAX = 23;
const quebra = (ws) => {
  const txt = ws.map((w) => w.text);
  if (txt.join(" ").length <= MAX) return [txt];
  let best = null;
  for (let k = 1; k < txt.length; k++) {
    const a = txt.slice(0, k).join(" "), b = txt.slice(k).join(" "), m = Math.max(a.length, b.length);
    if (m <= MAX && (!best || m < best.m)) best = { m, l: [txt.slice(0, k), txt.slice(k)] };
  }
  return best ? best.l : null;
};
// Palavra que a transcrição deixou sem duração (começa junto com a seguinte) nunca apareceria acesa:
// ela ganha os últimos 0,08 s da anterior e vai para o relatório, para conferir na escuta.
for (let i = 1; i < words.length - 1; i++) {
  if (words[i + 1].start - words[i].start < 0.034) {
    const novo = Math.max(words[i - 1].start + 0.067, words[i].start - 0.08);
    if (novo < words[i].start) { avisos.push(`palavra sem duração na transcrição: "${words[i].text}" em ${f3(words[i].start)}s (ganhou ${f3(words[i].start - novo)}s; confira na escuta)`); words[i].start = novo; }
  }
}
const primeira = words.findIndex((w) => w.end > abS);
const caps = [];
for (let i = primeira; i >= 0 && i < words.length;) {
  let n = Math.min(4, words.length - i), linhas = null;
  while (n > 1 && !(linhas = quebra(words.slice(i, i + n)))) n--;
  if (!linhas) linhas = [[words[i].text]];
  const grupo = words.slice(i, i + n);
  grupo.forEach((w, j) => {
    const ini = Math.max(w.start, abS), fim = words[i + j + 1] ? words[i + j + 1].start : dur;
    if (fim - ini <= 0.01) return;
    let k = 0;
    const html = linhas.map((l) => l.map((x) => (k++ === j ? `<span class="y">${esc(x)}</span>` : esc(x))).join(" ")).join("\n");
    caps.push(`<div class="c clip" id="c${i + j}" data-start="${f3(ini)}" data-duration="${f3(fim - ini)}" data-track-index="5">${html}</div>`);
  });
  i += n;
}

// ---- CTA: a frase do pedido como foi falada, entra no verbo do pedido e fica até o fim
let ctaHtml = "";
const cta = reel.cta || null;
if (cta && cta.texto) {
  const ini = cta.inicio ?? achar(cta.fala || cta.texto, abS, true);
  if (ini == null) erros.push(`CTA: fala não encontrada na transcrição: "${cta.fala || cta.texto}"`);
  else ctaHtml = `  <div class="cta clip" id="cta" data-start="${f3(ini)}" data-duration="${f3(dur - ini)}" data-track-index="6">${esc(cta.texto)}</div>`;
} else avisos.push("sem CTA no reel.json: o estilo fecha com a frase do pedido falada na gravação");

if (erros.length) { console.error(`o plano do reel.json quebra o estilo:\n  ${erros.join("\n  ")}`); process.exit(1); }

const html = readFileSync("src/index.template.html", "utf8")
  .replaceAll("__DUR__", f3(dur)).replace("__ACENTO__", acento)
  .replace("__FONTE_TITULO__", fonteTitulo).replace("__FONTE_CHAMADA__", fonteChamada)
  .replace("__CORPO__", corpo).replace("__HL_DY__", String(reel.headline_dy ?? 0))
  .replace("__CAP_Y__", String(reel.legenda_y ?? 1490)).replace("__CTA_Y__", String(reel.cta_y ?? 1600))
  .replace("__ABERTURA__", aberturaHtml).replace("__APOIOS__", apoiosHtml)
  .replace("__LEGENDAS__", caps.join("\n")).replace("__CTA__", ctaHtml).replace("__TEMPOS__", tempos.join("\n"));
writeFileSync("index.html", html);
const meta = existsSync("meta.json") ? JSON.parse(readFileSync("meta.json", "utf8")) : {};
Object.assign(meta, { id: "reel", width: 1096, height: 1920, fps: 30 });
writeFileSync("meta.json", JSON.stringify(meta, null, 2));
writeFileSync("textos-tela.md", `# Textos da tela\n\n## Headline da abertura\n\n${hlLinhas.join(" ")}\n\n## CTA\n\n${cta?.texto || ""}\n`);
for (const a of avisos) console.warn(`aviso: ${a}`);
console.log(`index.html montado: ${dur.toFixed(2)}s, ${caps.length} estados de legenda, ${apoios.length} apoios` +
  `${apoios.map((a) => ` [${f3(a._ini)}-${f3(a._ini + a._d)}]`).join("")}, acento ${reel.acento ? acento : "nenhum (branco)"}`);
