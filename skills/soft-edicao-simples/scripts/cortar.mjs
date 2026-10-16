// Corta raw.mp4 em clean.mp4 no estilo Direto: só os trechos de keeps.json, só as pausas longas saem, e tudo a 1,2x.
// Rode dentro de <projeto>/assets:  node <skill>/scripts/cortar.mjs [--velocidade 1.2] [--pausa-max 0.7] [--fade-ms 30]
// Entradas: raw.mp4, raw.json (tempo por palavra), keeps.json ({keeps:[{from,to,why,fade_in_ms?}]}), ../reel.json (velocidade, pausa_max).
// Saídas: clean.mp4 (já acelerado), edit-decisions.json e transcript.json (as palavras na linha do tempo do clean.mp4).
// Regra: dentro de cada trecho, um silêncio entre palavras de pausa_max segundos ou mais vira corte, com 0,1 s de folga
// depois da última palavra e antes da próxima. Pausa mais curta fica: a 1,2x ela vira o respiro natural do estilo.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? Number(argv[argv.indexOf(k) + 1]) : d);
const reel = existsSync("../reel.json") ? JSON.parse(readFileSync("../reel.json", "utf8")) : {};
const speed = opt("--velocidade", reel.velocidade || 1.2);
const pausaMax = opt("--pausa-max", reel.pausa_max ?? 0.7);
const fadeMs = opt("--fade-ms", 30);
const FOLGA = 0.1;
if (!(speed > 0)) { console.error("velocidade inválida"); process.exit(1); }
const { keeps } = JSON.parse(readFileSync("keeps.json", "utf8"));
const words = JSON.parse(readFileSync("raw.json", "utf8")).words;

// 1. trechos: cada keep, partido nas pausas longas entre palavras
const pieces = [];
for (const k of keeps) {
  const ws = words.filter((w) => w.start >= k.from && w.end <= k.to + 0.05);
  let s = k.from;
  for (let i = 1; i < ws.length; i++) {
    const gap = ws[i].start - ws[i - 1].end;
    if (gap >= pausaMax) {
      pieces.push({ s, e: +(ws[i - 1].end + FOLGA).toFixed(3), why: k.why, fi: k.fade_in_ms });
      s = +(ws[i].start - FOLGA).toFixed(3);
    }
  }
  pieces.push({ s, e: k.to, why: k.why, fi: k.fade_in_ms });
}
if (!pieces.length || pieces.some((p) => p.e <= p.s)) { console.error("trecho vazio ou invertido: confira keeps.json"); process.exit(1); }

// 2. linha do tempo de saída (cada trecho dura (fim - início) / velocidade)
let out = 0;
const segs = pieces.map((p) => { const d = (p.e - p.s) / speed; const r = { ...p, o: out, d }; out += d; return r; });

const f = segs.map((g, i) => {
  const fi = (g.fi ?? fadeMs) / 1000, fo = fadeMs / 1000;
  return `[0:v]trim=start=${g.s}:end=${g.e},setpts=(PTS-STARTPTS)/${speed},fps=30[v${i}];` +
    `[0:a]atrim=start=${g.s}:end=${g.e},asetpts=PTS-STARTPTS,atempo=${speed},apad,atrim=duration=${g.d.toFixed(4)},` +
    `afade=t=in:d=${fi},afade=t=out:st=${Math.max(0, g.d - fo).toFixed(4)}:d=${fo}[a${i}];`;
}).join("") + segs.map((_, i) => `[v${i}]`).join("") + `concat=n=${segs.length}:v=1:a=0[v];` + segs.map((_, i) => `[a${i}]`).join("") + `concat=n=${segs.length}:v=0:a=1[a]`;
writeFileSync("cut-filter.txt", f);
execFileSync("ffmpeg", ["-y", "-v", "error", "-i", "raw.mp4", "-filter_complex_script", "cut-filter.txt", "-map", "[v]", "-map", "[a]",
  "-t", out.toFixed(4), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p", "-r", "30",
  "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "clean.mp4"], { stdio: "inherit" });

// 3. palavras na linha do tempo do clean.mp4 (mesma conta do corte: nada de nova transcrição para achar o tempo)
const mapped = [];
for (const w of words) {
  const g = segs.find((x) => w.start >= x.s - 0.02 && w.start < x.e);
  if (!g) continue;
  const t = (v) => +(g.o + (Math.min(Math.max(v, g.s), g.e) - g.s) / speed).toFixed(3);
  const start = t(w.start), end = Math.max(t(w.end), start + 0.02);
  mapped.push({ text: w.text, start, end: +end.toFixed(3), source_start: w.start, source_end: w.end });
}
writeFileSync("transcript.json", JSON.stringify({ origem: "raw.json mapeado pelo corte", velocidade: speed, audio_duration_secs: +out.toFixed(3), words: mapped }, null, 1));
writeFileSync("edit-decisions.json", JSON.stringify({ source: "assets/raw.mp4", velocidade: speed, pausa_max: pausaMax, fade_ms: fadeMs, duration: +out.toFixed(3),
  segments: segs.map((g) => ({ source_start: g.s, source_end: g.e, output_start: +g.o.toFixed(3), output_end: +(g.o + g.d).toFixed(3), fade_in_ms: g.fi ?? fadeMs, reason: g.why })) }, null, 1));
console.log(`trechos=${segs.length} velocidade=${speed} duracao=${out.toFixed(3)}s palavras=${mapped.length}/${words.length}`);
