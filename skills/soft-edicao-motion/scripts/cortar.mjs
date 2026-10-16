// Corta raw.mp4 em clean.mp4 a partir do keeps.json, tirando toda pausa medida, com cortes J/L nas emendas.
// Rode dentro de <projeto>/assets:  node <skill>/scripts/cortar.mjs [--jl 4] [--no-jl] [--velocidade 1.2] [--pausa 0.4]
// --pausa: só sai o silêncio a partir desse tamanho em segundos (padrão 0.4: some a pausa, fica o respiro curto da fala).
// --velocidade: acelera imagem e som juntos depois do corte (1 = sem acelerar; a voz mantém o tom).
// Entradas: raw.mp4, keeps.json ({fps, keeps:[{from,to,why}]}), silences.txt (criado aqui se faltar).
// Saídas: clean.mp4, edit-decisions.json (linha do tempo do áudio = linha do tempo da legenda).
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execFileSync, spawnSync } from "node:child_process";

const args = process.argv.slice(2);
const JL = args.includes("--no-jl") ? 0 : Number(args.includes("--jl") ? args[args.indexOf("--jl") + 1] : 4); // quadros
const { keeps, fps = 30 } = JSON.parse(readFileSync("keeps.json", "utf8"));
const V = Number(args.includes("--velocidade") ? args[args.indexOf("--velocidade") + 1] : 1);
const PAUSA = Number(args.includes("--pausa") ? args[args.indexOf("--pausa") + 1] : 0.4);
if (!(V >= 0.5 && V <= 2)) { console.error("--velocidade entre 0.5 e 2"); process.exit(1); }
const frame = (t) => Math.round(t * fps) / fps;

// 1. silêncios medidos (ffmpeg silencedetect, -30 dB, 0,15 s)
if (!existsSync("silences.txt")) {
  const r = spawnSync("ffmpeg", ["-v", "info", "-i", "raw.mp4", "-vn", "-af", "silencedetect=noise=-30dB:d=0.15", "-f", "null", "-"], { encoding: "utf8" });
  const s = [...r.stderr.matchAll(/silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)/g)].map((m) => `${m[1]} ${m[2]}`);
  writeFileSync("silences.txt", s.join("\n"));
}
// Deixa uma cauda curta depois da fala e uma entrada um pouco maior antes da próxima sílaba.
const TAIL = 0.05, LEAD = 0.08;
const silences = readFileSync("silences.txt", "utf8").trim().split(/\s*\n/).filter(Boolean).map((l) => l.trim().split(" ").map(Number))
  .filter(([a, b]) => b - a >= PAUSA).map(([a, b]) => [a + TAIL, b - LEAD]).filter(([a, b]) => b - a > 0.06);

// 2. pedaços de áudio = trechos mantidos menos os silêncios
const pieces = [];
for (const k of keeps) {
  let cur = k.from;
  for (const [a, b] of silences) {
    if (b <= cur || a >= k.to) continue;
    if (a > cur) pieces.push({ s: frame(cur), e: frame(a), why: k.why });
    cur = b;
  }
  if (k.to > cur) pieces.push({ s: frame(cur), e: frame(k.to), why: k.why });
}
const segs = pieces.filter((p) => p.e - p.s >= 2 / fps);
if (!segs.length) { console.error("nenhum trecho sobrou: confira keeps.json e silences.txt"); process.exit(1); }

// 3. pedaços de vídeo: mesmas durações, mas nas emendas reais o corte da imagem fica deslocado do corte do som.
//    Alterna J (o som do próximo plano chega antes) e L (a imagem do próximo plano chega antes).
const d = JL / fps;
const vsegs = segs.map((g) => ({ s: g.s, e: g.e }));
let flip = 0;
for (let i = 0; i < segs.length - 1 && d > 0; i++) {
  const gap = segs[i + 1].s - segs[i].e;
  if (gap < 0.25) continue; // não é uma emenda visível
  if (flip++ % 2 === 0) { vsegs[i].e += d; vsegs[i + 1].s += d; }      // J: a imagem antiga fica enquanto o som novo começa
  else { vsegs[i].e -= d; vsegs[i + 1].s -= d; }                        // L: a imagem nova chega antes do som dela
}

let out = 0;
const decisions = segs.map((g, i) => {
  const r = { source_start: g.s, source_end: g.e, video_start: +vsegs[i].s.toFixed(3), video_end: +vsegs[i].e.toFixed(3), output_start: +out.toFixed(3), output_end: +(out + (g.e - g.s) / V).toFixed(3), reason: g.why };
  out += (g.e - g.s) / V;
  return r;
});

const f = segs.map((g, i) => {
  const v = vsegs[i], dur = g.e - g.s;
  return `[0:v]trim=${v.s.toFixed(4)}:${v.e.toFixed(4)},setpts=PTS-STARTPTS[v${i}];` +
    `[0:a]atrim=${g.s}:${g.e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st=${(dur - 0.012).toFixed(3)}:d=0.012[a${i}];`;
}).join("") + segs.map((_, i) => `[v${i}]`).join("") + `concat=n=${segs.length}:v=1:a=0${V !== 1 ? `,setpts=PTS/${V}` : ""}[v];` + segs.map((_, i) => `[a${i}]`).join("") + `concat=n=${segs.length}:v=0:a=1${V !== 1 ? `,atempo=${V}` : ""}[a]`;
writeFileSync("cut-filter.txt", f);
execFileSync("ffmpeg", ["-y", "-v", "error", "-i", "raw.mp4", "-filter_complex_script", "cut-filter.txt",
  "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-r", String(fps), "-g", String(fps), "-keyint_min", String(fps),
  "-c:a", "aac", "-b:a", "192k", "-shortest", "clean.mp4"], { stdio: "inherit" });
writeFileSync("edit-decisions.json", JSON.stringify({ source: "assets/raw.mp4", fps, jl_frames: JL, pausa_min: PAUSA, velocidade: V, duration: +out.toFixed(3), segments: decisions }, null, 1));
console.log(`trechos=${segs.length} emendas_jl=${flip} pausa_min=${PAUSA}s velocidade=${V} duracao=${out.toFixed(2)}s`);
