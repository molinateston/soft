// Renderiza o reel e confere o arquivo. Rode na raiz do projeto, depois do montar-index.mjs:
//   node <skill>/scripts/renderizar.mjs --rascunho   -> renders/<slug>-rascunho.mp4 (rápido, para olhar)
//   node <skill>/scripts/renderizar.mjs --final      -> renders/<slug>-final.mp4
//   acrescente --workers N para limitar os processos (máquina carregada ou pequena)
// Passos: lint do HyperFrames, render numa janela de 1096 px com quadros do vídeo extraídos em PNG, recorte para
// 1080x1920 e conferência: tamanho, 30 fps, áudio, integridade, borda direita.
// Por que a janela larga e o PNG: medido nesta skill, a janela de 1080 px ou a extração padrão dos quadros deixam
// uma faixa preta de 8 px na borda direita (o vídeo some a partir da coluna 1072). Só as duas juntas resolvem.
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, rmSync, statSync } from "node:fs";
import { hyperframes } from "./ferramentas.mjs";

const final = process.argv.includes("--final");
const iw = process.argv.indexOf("--workers"), workers = iw >= 0 ? process.argv[iw + 1] : "";
const tipo = final ? "final" : "rascunho";
if (!existsSync("index.html")) { console.error("falta index.html: rode o montar-index.mjs na raiz do projeto"); process.exit(1); }
const slug = (existsSync("meta.json") && JSON.parse(readFileSync("meta.json", "utf8")).name) || "reel";

console.log("1/3 lint do HyperFrames");
const lint = hyperframes(["lint", "."]);
if (lint.status !== 0) { console.error("o lint achou erro; conserte antes de renderizar"); process.exit(1); }

console.log(`2/3 render ${tipo} (pode levar alguns minutos)`);
const janela = `renders/.janela-${tipo}.mp4`, saida = `renders/${slug}-${tipo}.mp4`;
const r = hyperframes(["render", ".", "-o", janela, "-q", final ? "delivery" : "draft", "-f", "30", "--video-frame-format", "png", ...(workers ? ["--workers", workers] : []), "--quiet"]);
if (r.status !== 0 || !existsSync(janela)) { console.error("o render falhou; leia a saída acima"); process.exit(1); }
execFileSync("ffmpeg", ["-y", "-v", "error", "-i", janela, "-vf", "crop=1080:1920:0:0,setsar=1", "-c:v", "libx264",
  "-preset", final ? "slow" : "veryfast", "-crf", final ? "17" : "23", "-pix_fmt", "yuv420p", "-r", "30",
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", saida], { stdio: "inherit" });
rmSync(janela, { force: true });

console.log("3/3 conferência");
const pr = JSON.parse(execFileSync("ffprobe", ["-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration,size", "-of", "json", saida], { encoding: "utf8" }));
const v = pr.streams.find((s) => s.codec_type === "video"), temAudio = pr.streams.some((s) => s.codec_type === "audio");
const dur = Number(pr.format.duration), mb = statSync(saida).size / 1e6;
const integ = spawnSync("ffmpeg", ["-v", "error", "-i", saida, "-f", "null", "-"], { encoding: "utf8" }).stderr.trim();
// Borda direita: média das 8 últimas colunas no quadro do meio, contra as colunas logo antes.
const raw = execFileSync("ffmpeg", ["-v", "error", "-ss", (dur / 2).toFixed(2), "-i", saida, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], { maxBuffer: 64 * 1024 * 1024 });
const media = (x0, x1) => { let s = 0; for (let y = 0; y < 1920; y++) for (let x = x0; x < x1; x++) s += raw[y * 1080 + x]; return s / (1920 * (x1 - x0)); };
const borda = media(1072, 1080), vizinha = media(1056, 1068);
const checks = [
  ["1080x1920", v.width === 1080 && v.height === 1920, `${v.width}x${v.height}`],
  ["30 fps", v.r_frame_rate === "30/1", v.r_frame_rate],
  ["áudio presente", temAudio, temAudio ? "sim" : "não"],
  ["menos de 300 MB", mb < 300, `${mb.toFixed(1)} MB`],
  ["arquivo íntegro", integ === "", integ ? integ.split("\n")[0] : "sem erro"],
  ["sem faixa preta na direita", !(borda < 4 && vizinha > 16), `borda ${borda.toFixed(1)}, vizinha ${vizinha.toFixed(1)}`],
];
for (const [nome, ok, val] of checks) console.log(`${ok ? "ok   " : "FALHA"} ${nome.padEnd(28)} ${val}`);
console.log(`${saida}  (${dur.toFixed(2)} s)`);
process.exit(checks.every((c) => c[1]) ? 0 : 1);
