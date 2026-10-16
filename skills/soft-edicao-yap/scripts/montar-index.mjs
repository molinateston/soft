// Monta <projeto>/index.html a partir de src/index.template.html.
// Rode na raiz do projeto:  node <skill>/scripts/montar-index.mjs
// - __CAPTIONS__     : uma legenda por palavra, do assets/transcript.json, com as correções de assets/caption-fixes.json:
//      palavra:  {"errada": "certa", "apaga-esta": ""}            (toda ocorrência, já com as divisões juntadas)
//      trecho:   {"Digita a gente": "Digita agente"}              (chave com espaço: várias palavras seguidas,
//                                                                  sem diferença de maiúscula e pontuação)
//      num tempo só: {"_em": [{"em": 59.5, "para": "dou"}, {"em": 120.1, "juntar": 2, "para": "agente"}]}
//                (a palavra mais próxima de "em", até 0,3 s; "juntar" funde essa palavra com as seguintes numa só)
// - __DUR__          : duração do clean.mp4 medida com ffprobe (sem ffprobe, a da transcrição)
// - __CAP_TOP__, __ACENTO__, __FONTE_TITULO__ : do reel.json (nasce do perfil.json no novo-reel.mjs)
// - todo emoji do template vira <img class="emo"> com a arte livre do Noto Emoji
//   (template/emoji da skill; o que faltar é baixado da versão fixa v2.047 e guardado em assets/emoji)
import { readFileSync, writeFileSync, existsSync, mkdirSync, copyFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const skill = join(dirname(fileURLToPath(import.meta.url)), "..");
const t = JSON.parse(readFileSync("assets/transcript.json", "utf8"));
// Duração: a do clean.mp4 medida com ffprobe (a da transcrição pode passar uns décimos do vídeo).
const medirClean = () => { try { return Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "assets/clean.mp4"], { encoding: "utf8" }).trim()); } catch { return NaN; } };
const durClean = medirClean();
const dur = Number.isFinite(durClean) && durClean > 0 ? durClean : t.audio_duration_secs;
const fix = existsSync("assets/caption-fixes.json") ? JSON.parse(readFileSync("assets/caption-fixes.json", "utf8").replace(/^\uFEFF/, "")) : {};
const fixPalavra = {}, fixTrecho = [];
for (const [k, v] of Object.entries(fix)) {
  if (k.startsWith("_")) continue;
  if (/\s/.test(k.trim())) fixTrecho.push({ de: k.trim().split(/\s+/), para: String(v).trim() });
  else fixPalavra[k] = v;
}
const norm = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^\p{L}\p{N}%-]/gu, "");

// ---- 1. correção num tempo só, na transcrição crua (a palavra mais próxima de "em", até 0,3 s)
const maisPerto = (lista, x, max) => { let b = -1, bd = 1e9; lista.forEach((w, i) => { const d = Math.abs(w.start - x); if (d < bd) { bd = d; b = i; } }); return bd <= max ? b : -1; };
const noTempo = new Map();
for (const c of (Array.isArray(fix._em) ? fix._em : [])) {
  const k = maisPerto(t.words, c.em, 0.3);
  if (k >= 0) noTempo.set(k, c); else console.error(`aviso: nenhuma palavra a até 0,3 s de ${c.em} (correção "_em" ignorada)`);
}
// ---- 2. junta pedaços que a transcrição separa, como "e" + "-mail", "sub" + "-agentes" e "100" + "%"
let words = [];
for (let i = 0; i < t.words.length; i++) {
  const w = t.words[i], n = t.words[i + 1];
  if (noTempo.has(i)) {
    const c = noTempo.get(i), qtd = Math.max(1, c.juntar || 1), ultima = t.words[Math.min(i + qtd - 1, t.words.length - 1)];
    if (c.para) words.push({ text: c.para, start: w.start, end: ultima.end, fixo: true });
    i += qtd - 1; continue;
  }
  if (n && !noTempo.has(i + 1) && (n.text.startsWith("-") || n.text === "%")) { words.push({ text: w.text + n.text, start: w.start, end: n.end }); i++; continue; }
  words.push({ text: w.text, start: w.start, end: w.end });
}
// ---- 3. correção por palavra (toda ocorrência), já sobre as palavras juntadas
words = words.flatMap((w) => {
  if (w.fixo) return [w];
  const pont = (w.text.match(/[.,;:!?…]+$/) || [""])[0], base = w.text.slice(0, w.text.length - pont.length);
  const chave = w.text in fixPalavra ? w.text : base in fixPalavra ? base : null;
  if (chave === null) return [w];
  const novo = fixPalavra[chave];
  return novo ? [{ ...w, text: chave === base ? novo + pont : novo }] : [];
});
// ---- 4. correção por trecho de várias palavras (a mais longa primeiro); a pontuação final da fala fica
fixTrecho.sort((a, b) => b.de.length - a.de.length);
for (const { de, para } of fixTrecho) {
  const alvo = de.map(norm), novas = para ? para.split(/\s+/) : [];
  for (let i = 0; i + alvo.length <= words.length; i++) {
    const trecho = words.slice(i, i + alvo.length);
    if (trecho.some((w) => w.fixo) || !trecho.every((w, j) => norm(w.text) === alvo[j])) continue;
    const ini = trecho[0].start, fim = trecho[trecho.length - 1].end, pont = (trecho[trecho.length - 1].text.match(/[.,!?;:…]+$/) || [""])[0];
    const troca = novas.map((txt, j) => {
      // mesma quantidade de palavras: cada uma fica no tempo da original; senão, o trecho é dividido por igual
      const s = novas.length === trecho.length ? trecho[j].start : ini + ((fim - ini) * j) / novas.length;
      const e = novas.length === trecho.length ? trecho[j].end : ini + ((fim - ini) * (j + 1)) / novas.length;
      const ultima = j === novas.length - 1 && pont && !/[.,!?;:…]$/.test(txt);
      return { text: ultima ? txt + pont : txt, start: s, end: e, fixo: true };
    });
    words.splice(i, trecho.length, ...troca);
    i += troca.length - 1;
  }
}

// ---- uma legenda por palavra (do início dela até a próxima palavra, no máximo 1,2 s)
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const caps = words.map((w, i) => {
  const next = words[i + 1] ? words[i + 1].start : dur;
  const d = Math.min(next - w.start, 1.2);
  if (d <= 0.01) return "";
  return `<div class="w clip" id="w${i}" data-start="${w.start.toFixed(3)}" data-duration="${d.toFixed(3)}" data-track-index="5">${esc(w.text)}</div>`;
}).join("\n");

// Ajustes por vídeo (reel.json): capTop = topo da legenda em px, no peito, logo abaixo do queixo.
const cfg = { capTop: 1380, acento: "", fonteTitulo: "assets/fonts/titulo.ttf", ...(existsSync("reel.json") ? JSON.parse(readFileSync("reel.json", "utf8")) : {}) };
const acento = /^#[0-9a-fA-F]{6}$/.test(cfg.acento || "") ? cfg.acento : "#ffffff"; // sem identidade: só branco
if (!existsSync(cfg.fonteTitulo)) { console.error(`FALTA a fonte do título: ${cfg.fonteTitulo} (rode o novo-reel.mjs ou ajuste o reel.json)`); process.exit(1); }
let html = readFileSync("src/index.template.html", "utf8").replaceAll("__DUR__", dur.toFixed(3)).replace("__CAPTIONS__", caps)
  .replace("__CAP_TOP__", String(cfg.capTop)).replace("__ACENTO__", acento).replace("__FONTE_TITULO__", cfg.fonteTitulo);

// ---- emoji: cada sequência vira um PNG local do Noto Emoji (licença livre; veja LICENCAS.md)
const NOTO = "https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@v2.047/png/128";
mkdirSync("assets/emoji", { recursive: true });
const re = /(\p{Extended_Pictographic}(\uFE0F|\u200D\p{Extended_Pictographic}|\p{Emoji_Modifier})*|[\u{1F1E6}-\u{1F1FF}]{2})/gu;
const inTags = (s, idx) => s.lastIndexOf("<", idx) > s.lastIndexOf(">", idx); // dentro de tag ou atributo: deixa
const pending = [];
html = html.replace(re, (m, _a, _b, idx, s) => {
  if (inTags(s, idx) || s.lastIndexOf("<script", idx) > s.lastIndexOf("</script>", idx)) return m;
  const code = [...m].map((c) => c.codePointAt(0).toString(16)).filter((c) => c !== "fe0f").join("_");
  const name = `emoji_u${code}.png`;
  pending.push({ m, name });
  return `<img class="emo" src="assets/emoji/${name}" alt="">`;
});
const missing = [];
for (const { m, name } of pending) {
  const dest = join("assets/emoji", name), local = join(skill, "template", "emoji", name);
  if (existsSync(dest)) continue;
  if (existsSync(local)) { copyFileSync(local, dest); continue; }
  try {
    const r = await fetch(`${NOTO}/${name}`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
    console.log(`emoji ${m} baixado do Noto Emoji v2.047`);
  } catch (e) { missing.push(`${m} (${name}: ${e.message})`); }
}
if (missing.length) {
  console.error(`emoji sem arte livre disponível:\n  ${[...new Set(missing)].join("\n  ")}\nTroque por outro emoji, por texto, ou ponha o PNG do Noto em assets/emoji/ e rode de novo.`);
  process.exit(1);
}

writeFileSync("index.html", html);
const meta = existsSync("meta.json") ? JSON.parse(readFileSync("meta.json", "utf8")) : {};
Object.assign(meta, { id: "reel", width: 1096, height: 1920, fps: 30 });
writeFileSync("meta.json", JSON.stringify(meta, null, 2));
console.log(`index.html montado: ${dur.toFixed(2)}s, ${words.length} palavras na legenda, acento ${cfg.acento ? acento : "nenhum (branco)"}`);
