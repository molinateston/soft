// Renderiza o index.html do projeto e entrega o MP4 1080x1920 sem faixa preta na borda direita.
// Rode na raiz do projeto: node <skill>/scripts/renderizar.mjs [--rascunho] [--saida renders/<slug>-final.mp4] [--workers auto] [--quadros png|jpg]
// --quadros jpg: extrai os quadros da câmera em jpg (cerca de 6 vezes menos disco que png). Só com camZoom de 1.02
// ou mais no reel.json: o zoom empurra para fora da tela a borda direita onde a faixa preta apareceria.
// Por quê: o render do HyperFrames deixa uma faixa preta de 8 px na borda direita do vídeo da câmera em dois casos
// medidos: janela de exatamente 1080 px e extração de quadros do vídeo em jpg. O template usa janela de 1096 px,
// o render extrai os quadros em png, e aqui o resultado é recortado de volta para 1080.
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, rmSync, mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import { join, dirname, resolve } from "node:path";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const rascunho = argv.includes("--rascunho");
const meta = existsSync("meta.json") ? JSON.parse(readFileSync("meta.json", "utf8")) : {};
const saida = resolve(opt("--saida", `renders/${rascunho ? "draft" : `${meta.name || "reel"}-final`}.mp4`));
if (!existsSync("index.html")) { console.error("sem index.html: rode antes o montar-index.mjs"); process.exit(1); }

let bin;
try { bin = join(dirname(createRequire(join(process.cwd(), "package.json")).resolve("hyperframes/package.json")), "bin", "hyperframes.mjs"); }
catch { console.error("FALTA hyperframes. Na pasta de trabalho: npm install hyperframes@0.8.93 gsap@3.14.2"); process.exit(2); }

mkdirSync(dirname(saida), { recursive: true });
const bruto = join(dirname(saida), `.bruto-${Date.now()}.mp4`);
const env = { ...process.env, HYPERFRAMES_NO_TELEMETRY: "1" };
const r = spawnSync(process.execPath, [bin, "render", ".", "-o", bruto, "-q", rascunho ? "draft" : "looks", "--workers", opt("--workers", "auto"), "--video-frame-format", opt("--quadros", "png"), "--quiet"], { stdio: "inherit", env });
if (r.status !== 0 || !existsSync(bruto)) { console.error("o render falhou; veja a saída acima"); process.exit(1); }

const largura = Number(execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", bruto], { encoding: "utf8" }).trim());
if (largura < 1080) { console.error(`o render saiu com ${largura} px de largura; esperado 1096`); process.exit(1); }
execFileSync("ffmpeg", ["-y", "-v", "error", "-i", bruto, "-vf", "crop=1080:1920:0:0,setsar=1", "-c:v", "libx264", "-preset", rascunho ? "veryfast" : "slow",
  "-crf", rascunho ? "23" : "16", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "copy", "-movflags", "+faststart", saida], { stdio: "inherit" });
rmSync(bruto, { force: true });

const info = execFileSync("ffprobe", ["-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration,size", "-of", "compact=p=0", saida], { encoding: "utf8" }).trim();
const integro = spawnSync("ffmpeg", ["-v", "error", "-i", saida, "-f", "null", "-"], { encoding: "utf8" }).stderr.trim() === "";
console.log(`${saida}\n${info}\narquivo íntegro: ${integro ? "sim" : "NÃO"}`);
process.exit(integro ? 0 : 1);
