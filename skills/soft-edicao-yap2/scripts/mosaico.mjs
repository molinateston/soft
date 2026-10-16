// Folha de contato: quadros do vídeo em tempos escolhidos, lado a lado, numa imagem só.
// Uso: node <skill>/scripts/mosaico.mjs <video.mp4> [--tempos 0,1,3,5.5] [--saida conferencia/mosaico.jpg] [--colunas 4]
// Sem --tempos: 0 s, 1 s, 3 s e depois a cada 5 s até o fim (a régua da folha de contato).
// Imprime a ordem dos tempos (da esquerda para a direita, de cima para baixo) para você ler a imagem.
import { execFileSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";

const args = process.argv.slice(2);
const opt = (k, d) => (args.includes(k) ? args[args.indexOf(k) + 1] : d);
const video = args.find((a, i) => !a.startsWith("--") && !String(args[i - 1]).startsWith("--"));
if (!video) { console.error("uso: mosaico.mjs <video.mp4> [--tempos 0,1,3] [--saida arquivo.jpg] [--colunas 4]"); process.exit(1); }
const pr = JSON.parse(execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate:format=duration", "-of", "json", video], { encoding: "utf8" }));
const [nu, de] = pr.streams[0].r_frame_rate.split("/").map(Number);
const fps = nu / (de || 1), dur = Number(pr.format.duration);
let tempos = opt("--tempos", "") ? opt("--tempos").split(",").map(Number) : [0, 1, 3];
if (!opt("--tempos", "")) for (let t = 5; t < dur; t += 5) tempos.push(t);
tempos = tempos.filter((t) => t < dur);
const quadros = [...new Set(tempos.map((t) => Math.min(Math.round(t * fps), Math.floor(dur * fps) - 1)))];
const col = Math.min(Number(opt("--colunas", 4)), quadros.length), lin = Math.ceil(quadros.length / col);
const saida = opt("--saida", "conferencia/mosaico.jpg");
mkdirSync(dirname(saida), { recursive: true });
const sel = quadros.map((n) => `eq(n\\,${n})`).join("+");
execFileSync("ffmpeg", ["-y", "-v", "error", "-i", video, "-vf", `select='${sel}',scale=360:640,tile=${col}x${lin}:padding=6:color=white`,
  "-frames:v", "1", "-fps_mode", "passthrough", "-q:v", "3", saida], { stdio: "inherit" });
console.log(`mosaico: ${saida}`);
console.log(`quadros (s): ${quadros.map((n) => (n / fps).toFixed(2)).join(", ")}`);
