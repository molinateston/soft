// Tira um quadro em cada troca de sobreposição (show/hide do index.html) e junta tudo num mosaico para OLHAR.
// Rode na raiz do projeto: node <skill>/scripts/mosaico.mjs renders/draft.mp4 [--tempos 0,1.5,3] [--saida renders/mosaico.jpg]
// Sem --tempos, usa 0 s, cada show()/hide() do index.html (um quadro depois da troca) e o último segundo.
import { readFileSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname } from "node:path";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const video = argv.find((a, i) => !a.startsWith("--") && !["--tempos", "--saida"].includes(argv[i - 1]));
if (!video || !existsSync(video)) { console.error("uso: node mosaico.mjs <video> [--tempos 0,1.5] [--saida renders/mosaico.jpg]"); process.exit(1); }
const saida = opt("--saida", join(dirname(video), "mosaico.jpg"));
const dur = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], { encoding: "utf8" }).trim());

let tempos = opt("--tempos", "") ? opt("--tempos").split(",").map(Number) : null;
if (!tempos) {
  const html = existsSync("index.html") ? readFileSync("index.html", "utf8") : "";
  const corpo = html.replace(/\/\/.*$/gm, "");
  const trocas = [...corpo.matchAll(/\b(?:show|hide)\(\s*["'][^"']+["']\s*,\s*([\d.]+)\s*\)/g)].map((m) => Number(m[1]) + 1 / 30);
  tempos = [0, ...trocas, Math.max(0, dur - 0.5)];
}
tempos = [...new Set(tempos.filter((t) => t >= 0 && t < dur).map((t) => +t.toFixed(3)))].sort((a, b) => a - b).slice(0, 24);

const tmp = join(dirname(saida), ".mosaico-tmp");
rmSync(tmp, { recursive: true, force: true });
mkdirSync(tmp, { recursive: true });
tempos.forEach((t, i) => execFileSync("ffmpeg", ["-y", "-v", "error", "-ss", String(t), "-i", video, "-frames:v", "1", "-vf", "scale=270:480", join(tmp, `q${String(i).padStart(3, "0")}.png`)]));
const cols = Math.min(6, tempos.length), lin = Math.ceil(tempos.length / cols);
execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", "1", "-i", join(tmp, "q%03d.png"), "-vf", `tile=${cols}x${lin}:padding=6:color=gray`, "-frames:v", "1", saida]);
rmSync(tmp, { recursive: true, force: true });
console.log(`mosaico: ${saida}\nquadros (s, da esquerda para a direita, de cima para baixo): ${tempos.join(", ")}`);
