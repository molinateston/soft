// Leva as palavras da transcrição do bruto (assets/raw.json) para o tempo do vídeo limpo, pelo edit-decisions.json.
// Rode na raiz do projeto: node <skill>/scripts/palavras-limpo.mjs
// Saída: assets/transcript.json (o que a legenda e o ancoras.mjs leem) e a lista de palavras que o corte tirou.
// Mais rápido que transcrever o clean.mp4 de novo e mantém as correções já feitas. A conferência por nova
// transcrição continua valendo (passo 5 do SKILL.md) quando o faster-whisper está instalado.
import { readFileSync, writeFileSync } from "node:fs";

const raw = JSON.parse(readFileSync("assets/raw.json", "utf8"));
const ed = JSON.parse(readFileSync("assets/edit-decisions.json", "utf8"));
const V = ed.velocidade || 1;
const segs = ed.segments;
const mapa = (t) => {
  for (const g of segs) if (t >= g.source_start && t <= g.source_end) return g.output_start + (t - g.source_start) / V;
  return null;
};
const words = [], fora = [];
for (const w of raw.words) {
  let s = mapa(w.start), e = mapa(w.end);
  if (s === null) { // começo caiu num trecho cortado: vale se o fim da palavra está dentro de um trecho
    const g = segs.find((x) => w.start < x.source_start && w.end > x.source_start + 0.05);
    if (g) s = g.output_start;
  }
  if (s === null) { fora.push(`${w.text}@${w.start.toFixed(2)}`); continue; }
  if (e === null) { // fim caiu num trecho cortado: termina no fim do trecho onde começou
    const g = segs.find((x) => w.start >= x.source_start - 0.001 && w.start <= x.source_end) || segs.find((x) => w.start < x.source_start);
    e = g ? g.output_end : s + 0.1;
  }
  if (e <= s) e = s + 0.05;
  words.push({ text: w.text, start: +s.toFixed(3), end: +e.toFixed(3) });
}
writeFileSync("assets/transcript.json", JSON.stringify({ language_code: raw.language_code || "pt", audio_duration_secs: ed.duration, origem: "raw.json levado ao tempo do clean.mp4", words }, null, 1));
console.log(`transcript.json: ${words.length} palavras no clean.mp4 (${ed.duration}s, velocidade ${V})`);
if (fora.length) console.log(`saíram no corte (${fora.length}): ${fora.join(" ")}`);
