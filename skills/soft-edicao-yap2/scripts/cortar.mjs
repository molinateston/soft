// Corta o bruto no limpo a partir de trechos.json, tirando toda pausa medida.
// Rode dentro de <projeto>/assets:
//   node <skill>/scripts/cortar.mjs                      -> bruto.mp4 vira limpo.mp4 (corte seco, sem J/L)
//   node <skill>/scripts/cortar.mjs --jl 4               -> com J/L de 4 quadros nos pontos de edição (opcional)
//   node <skill>/scripts/cortar.mjs --angulo angulo2.mp4 -> corta outro ângulo com os MESMOS cortes (só imagem)
// Entradas: bruto.mp4, trechos.json ({"fps":30,"trechos":[{"de":0.4,"ate":12.8,"motivo":"gancho, take 2"}]}),
//           silencios.txt (gerado aqui se faltar: silencedetect -30 dB, 0,15 s).
// Saídas: limpo.mp4 e cortes.json (linha do tempo do áudio = linha do tempo da legenda).
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execFileSync, spawnSync } from "node:child_process";

const args = process.argv.slice(2);
const JL = args.includes("--jl") ? Number(args[args.indexOf("--jl") + 1] || 4) : 0; // quadros
const angulo = args.includes("--angulo") ? args[args.indexOf("--angulo") + 1] : null;

if (angulo) {
  // Outro ângulo do mesmo take, já sincronizado e aparado no mesmo início do bruto.
  const { fps, segmentos } = JSON.parse(readFileSync("cortes.json", "utf8"));
  const f = segmentos.map((s, i) => `[0:v]trim=start_frame=${Math.round(s.video_de * fps)}:end_frame=${Math.round(s.video_ate * fps)},setpts=PTS-STARTPTS[v${i}];`).join("") +
    segmentos.map((_, i) => `[v${i}]`).join("") + `concat=n=${segmentos.length}:v=1:a=0[v]`;
  writeFileSync("filtro-angulo.txt", f);
  const saida = angulo.replace(/\.mp4$/i, "") + "-limpo.mp4";
  execFileSync("ffmpeg", ["-y", "-v", "error", "-i", angulo, "-filter_complex_script", "filtro-angulo.txt", "-map", "[v]",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-r", String(fps), "-g", String(fps), "-keyint_min", String(fps), "-pix_fmt", "yuv420p", "-an", saida], { stdio: "inherit" });
  console.log(`ângulo cortado: ${saida}`);
  process.exit(0);
}

const cfg = JSON.parse(readFileSync("trechos.json", "utf8"));
const fps = cfg.fps || 30;
const trechos = cfg.trechos.map((k) => ({ de: k.de, ate: k.ate, motivo: k.motivo || "" }));
const quadro = (t) => Math.round(t * fps) / fps;

// 1. silêncios medidos
if (!existsSync("silencios.txt")) {
  const r = spawnSync("ffmpeg", ["-v", "info", "-i", "bruto.mp4", "-vn", "-af", "silencedetect=noise=-30dB:d=0.15", "-f", "null", "-"], { encoding: "utf8" });
  const s = [...r.stderr.matchAll(/silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)/g)].map((m) => `${m[1]} ${m[2]}`);
  writeFileSync("silencios.txt", s.join("\n"));
}
// Sobra curta depois da fala e entrada um pouco maior antes da próxima sílaba.
const CAUDA = 0.05, ENTRADA = 0.08;
const silencios = readFileSync("silencios.txt", "utf8").trim().split(/\s*\n/).filter(Boolean).map((l) => l.trim().split(" ").map(Number))
  .map(([a, b]) => [a + CAUDA, b - ENTRADA]).filter(([a, b]) => b - a > 0.06);

// 2. pedaços de áudio = trechos menos silêncios
const pedacos = [];
for (const k of trechos) {
  let cur = k.de;
  for (const [a, b] of silencios) {
    if (b <= cur || a >= k.ate) continue;
    if (a > cur) pedacos.push({ s: quadro(cur), e: quadro(a), motivo: k.motivo });
    cur = b;
  }
  if (k.ate > cur) pedacos.push({ s: quadro(cur), e: quadro(k.ate), motivo: k.motivo });
}
const segs = pedacos.filter((p) => p.e - p.s >= 2 / fps);
if (!segs.length) { console.error("nenhum trecho sobrou depois de tirar as pausas; confira trechos.json"); process.exit(1); }

// 3. imagem: mesmas durações; com --jl, o corte de imagem se desloca do corte de som (J e L alternados).
const d = JL / fps;
const vsegs = segs.map((g) => ({ s: g.s, e: g.e }));
let jl = 0;
for (let i = 0; i < segs.length - 1 && d > 0; i++) {
  if (segs[i + 1].s - segs[i].e < 0.25) continue; // não é ponto de edição visível
  if (jl++ % 2 === 0) { vsegs[i].e += d; vsegs[i + 1].s += d; } else { vsegs[i].e -= d; vsegs[i + 1].s -= d; }
}

let saida = 0;
const segmentos = segs.map((g, i) => {
  const r = { bruto_de: g.s, bruto_ate: g.e, video_de: +vsegs[i].s.toFixed(3), video_ate: +vsegs[i].e.toFixed(3),
    saida_de: +saida.toFixed(3), saida_ate: +(saida + g.e - g.s).toFixed(3), motivo: g.motivo };
  saida += g.e - g.s;
  return r;
});

const f = segs.map((g, i) => {
  const v = vsegs[i], dur = g.e - g.s;
  return `[0:v]trim=start_frame=${Math.round(v.s * fps)}:end_frame=${Math.round(v.e * fps)},setpts=PTS-STARTPTS[v${i}];` +
    `[0:a]atrim=${g.s}:${g.e},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st=${(dur - 0.012).toFixed(3)}:d=0.012[a${i}];`;
}).join("") + segs.map((_, i) => `[v${i}]`).join("") + `concat=n=${segs.length}:v=1:a=0[v];` +
  segs.map((_, i) => `[a${i}]`).join("") + `concat=n=${segs.length}:v=0:a=1[a]`;
writeFileSync("filtro-corte.txt", f);
execFileSync("ffmpeg", ["-y", "-v", "error", "-i", "bruto.mp4", "-filter_complex_script", "filtro-corte.txt",
  "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-r", String(fps), "-g", String(fps), "-keyint_min", String(fps), "-pix_fmt", "yuv420p",
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "limpo.mp4"], { stdio: "inherit" });
writeFileSync("cortes.json", JSON.stringify({ origem: "assets/bruto.mp4", fps, jl_quadros: JL, duracao: +saida.toFixed(3), segmentos }, null, 1));
console.log(`segmentos=${segs.length} cortes_jl=${jl} duracao=${saida.toFixed(2)}s -> limpo.mp4`);
