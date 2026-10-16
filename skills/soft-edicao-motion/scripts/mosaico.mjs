// Tira quadros do vídeo nos momentos que importam e junta tudo num mosaico para OLHAR.
// Rode na raiz do projeto: node <skill>/scripts/mosaico.mjs renders/draft.mp4 [--tempos 0,1.5,3] [--contra outro.mp4] [--saida renders/mosaico.jpg]
// Sem --tempos, usa o src/cenas.json: entrada de cada cena (+0,4 s), o meio e a volta ao rosto (+0,2 s depois do fim).
// --contra: põe, embaixo de cada quadro, o quadro do mesmo tempo de outro vídeo (uma referência aprovada, uma versão anterior).
import { readFileSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname } from "node:path";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const video = argv.find((a, i) => !a.startsWith("--") && !["--tempos", "--saida", "--contra"].includes(argv[i - 1]));
if (!video || !existsSync(video)) { console.error("uso: node mosaico.mjs <video> [--tempos 0,1.5] [--contra outro.mp4] [--saida renders/mosaico.jpg]"); process.exit(1); }
const contra = opt("--contra", "");
const saida = opt("--saida", join(dirname(video), contra ? "mosaico-contra.jpg" : "mosaico.jpg"));
const dur = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], { encoding: "utf8" }).trim());

let tempos = opt("--tempos", "") ? opt("--tempos").split(",").map(Number) : null;
if (!tempos) {
  const cenas = existsSync("src/cenas.json") ? JSON.parse(readFileSync("src/cenas.json", "utf8")).cenas || [] : [];
  tempos = [0.5];
  for (const c of cenas) tempos.push(c.de + 0.4, (c.de + c.ate) / 2, c.ate + 0.2);
  tempos.push(Math.max(0, dur - 0.5));
}
tempos = [...new Set(tempos.filter((t) => t >= 0 && t < dur).map((t) => +t.toFixed(2)))].sort((a, b) => a - b).slice(0, contra ? 12 : 30);

const tmp = join(dirname(saida), ".mosaico-tmp");
rmSync(tmp, { recursive: true, force: true });
mkdirSync(tmp, { recursive: true });
const quadro = (v, t, arq, rotulo) => execFileSync("ffmpeg", ["-y", "-v", "error", "-ss", String(t), "-i", v, "-frames:v", "1", "-vf",
  `scale=270:480,drawtext=text='${rotulo}':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6`, arq]);
tempos.forEach((t, i) => {
  quadro(video, t, join(tmp, `a${String(i).padStart(3, "0")}.png`), `${t.toFixed(1)}s`);
  if (contra) quadro(contra, t, join(tmp, `b${String(i).padStart(3, "0")}.png`), `ref ${t.toFixed(1)}s`);
});
const cols = Math.min(6, tempos.length), lin = Math.ceil(tempos.length / cols);
if (!contra) {
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", "1", "-i", join(tmp, "a%03d.png"), "-vf", `tile=${cols}x${lin}:padding=6:color=gray`, "-frames:v", "1", saida]);
} else {
  // cada coluna: candidato em cima, referência embaixo
  tempos.forEach((_, i) => {
    const n = String(i).padStart(3, "0");
    execFileSync("ffmpeg", ["-y", "-v", "error", "-i", join(tmp, `a${n}.png`), "-i", join(tmp, `b${n}.png`), "-filter_complex", "vstack", join(tmp, `p${n}.png`)]);
  });
  execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", "1", "-i", join(tmp, "p%03d.png"), "-vf", `tile=${cols}x${lin}:padding=6:color=gray`, "-frames:v", "1", saida]);
}
rmSync(tmp, { recursive: true, force: true });
console.log(`mosaico: ${saida}\nquadros (s, da esquerda para a direita, de cima para baixo): ${tempos.join(", ")}`);
