// Cria o projeto de um reel a partir da gravação do celular e transcreve a fala.
// Rode na PASTA DE TRABALHO (onde ficam perfil.json, node_modules e video-projects/):
//   node <skill>/scripts/novo-reel.mjs "<video>" <slug> [--sem-transcricao]
// Cria video-projects/<slug>/ com assets/raw.mp4 (1080x1920, 30 fps), assets/raw.json (tempo por palavra),
// assets/words.txt (palavras com tempo e pausas), fontes, gsap, reel.json (identidade) e src/index.template.html.
// --sem-transcricao: só monta o projeto; ponha um assets/raw.json seu e rode de novo para gerar o words.txt.
import { execFileSync, spawnSync } from "node:child_process";
import { cpSync, copyFileSync, mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { dirname, join, resolve, extname, isAbsolute } from "node:path";
import { homedir } from "node:os";

const args = process.argv.slice(2);
const semTranscricao = args.includes("--sem-transcricao");
const [src, slug] = args.filter((a) => !a.startsWith("--"));
if (!src || !slug) { console.error('uso: node novo-reel.mjs "<video>" <slug> [--sem-transcricao]'); process.exit(1); }
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) { console.error("slug em minúsculas, sem acento, com hífens (ex.: reel-algoritmo)"); process.exit(1); }

const skill = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const trabalho = process.cwd();
const perfil = existsSync("perfil.json") ? JSON.parse(readFileSync("perfil.json", "utf8")) : null;
if (!perfil) console.warn("aviso: sem perfil.json nesta pasta. Identidade neutra: só branco e a fonte livre padrão. Esquema em references/perfil.md.");

const proj = resolve("video-projects", slug);
const a = join(proj, "assets");
for (const d of ["assets/fonts", "assets/prints", "src", "renders"]) mkdirSync(join(proj, d), { recursive: true });

// GSAP: vem da instalação da pasta de trabalho (Primeiros passos do SKILL.md).
let gsap;
try { gsap = createRequire(join(trabalho, "package.json")).resolve("gsap/dist/gsap.min.js"); }
catch { console.error("FALTA gsap. Na pasta de trabalho: npm install hyperframes@0.8.93 gsap@3.14.2"); process.exit(2); }
copyFileSync(gsap, join(a, "gsap.min.js"));

// Fontes: rótulo livre sempre; título = a do perfil (se o dono declarou e o arquivo existe) ou a livre padrão.
copyFileSync(join(skill, "template", "fonts", "Inter-Bold.otf"), join(a, "fonts", "Inter-Bold.otf"));
let fonteTitulo = "assets/fonts/titulo.ttf", origemFonte = "padrão livre: DM Serif Display (OFL 1.1)";
const fp = perfil?.fonte_titulo ? (isAbsolute(perfil.fonte_titulo) ? perfil.fonte_titulo : resolve(trabalho, perfil.fonte_titulo)) : "";
if (fp && existsSync(fp)) {
  fonteTitulo = `assets/fonts/titulo${extname(fp).toLowerCase()}`;
  copyFileSync(fp, join(proj, fonteTitulo));
  origemFonte = `perfil.json: ${perfil.fonte_titulo}`;
} else {
  if (fp) console.warn(`aviso: fonte_titulo do perfil não encontrada (${perfil.fonte_titulo}); usando a livre padrão.`);
  copyFileSync(join(skill, "template", "fonts", "DMSerifDisplay-Regular.ttf"), join(proj, fonteTitulo));
}

// Identidade do vídeo: reel.json (pode ser ajustado à mão por vídeo).
const hex = /^#[0-9a-fA-F]{6}$/;
if (perfil?.cor_acento && !hex.test(perfil.cor_acento)) console.warn(`aviso: cor_acento "${perfil.cor_acento}" não é #RRGGBB; ficando sem acento.`);
if (!existsSync(join(proj, "reel.json"))) {
  writeFileSync(join(proj, "reel.json"), JSON.stringify({
    capTop: 1380,
    acento: perfil?.cor_acento && hex.test(perfil.cor_acento) ? perfil.cor_acento : "",
    fonteTitulo, origemFonte,
  }, null, 2) + "\n");
}
writeFileSync(join(proj, "meta.json"), JSON.stringify({ id: "reel", name: slug, width: 1096, height: 1920, fps: 30 }, null, 2) + "\n");
writeFileSync(join(proj, "hyperframes.json"), JSON.stringify({ paths: { blocks: "compositions", components: "compositions/components", assets: "assets" } }, null, 2) + "\n");
if (!existsSync(join(proj, "src", "index.template.html"))) cpSync(join(skill, "template", "index.template.html"), join(proj, "src", "index.template.html"));

if (!existsSync(join(a, "raw.mp4"))) {
  console.log("convertendo para 1080x1920, 30 fps…");
  // o ffmpeg aplica a rotação gravada pelo celular, então a saída fica em pé
  execFileSync("ffmpeg", ["-y", "-v", "error", "-i", src, "-map", "0:v:0", "-map", "0:a:0", "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", join(a, "raw.mp4")], { stdio: "inherit" });
}

if (!existsSync(join(a, "raw.json")) && !semTranscricao) {
  const venv = join(homedir(), ".venvs", "whisper", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const PY = process.env.WHISPER_PYTHON || (existsSync(venv) ? venv : (process.platform === "win32" ? "python" : "python3"));
  const ok = spawnSync(PY, ["-c", "import faster_whisper"], { stdio: "ignore" }).status === 0;
  if (!ok) {
    console.error(`FALTA a transcrição local (faster-whisper) em ${PY}. Veja "Primeiros passos" no SKILL.md.\nO projeto já está montado em ${proj}; rode este comando de novo depois de instalar.`);
    process.exit(2);
  }
  console.log("transcrevendo (na primeira vez baixa o modelo, demora)…");
  execFileSync(PY, [join(skill, "scripts", "transcrever.py"), join(a, "raw.mp4"), join(a, "raw.json")],
    { stdio: ["ignore", "inherit", "inherit"], env: { ...process.env, PYTHONIOENCODING: "utf-8" } });
}

if (!existsSync(join(a, "raw.json"))) { console.log(`projeto montado: ${proj} (sem raw.json ainda)`); process.exit(0); }
const t = JSON.parse(readFileSync(join(a, "raw.json"), "utf8"));
let out = "", line = "", ls = 0, prev = 0;
for (const w of t.words) {
  if (w.start - prev > 0.5 || line.length > 90) { if (line) out += `${ls.toFixed(2).padStart(7)} ${line}\n`; if (w.start - prev > 0.5) out += `        --- pausa ${(w.start - prev).toFixed(1)}s\n`; line = ""; ls = w.start; }
  line += `${w.text}@${w.start.toFixed(2)} `; prev = w.end;
}
out += `${ls.toFixed(2).padStart(7)} ${line}\n`;
writeFileSync(join(a, "words.txt"), out);
console.log(`pronto: ${proj}  (duração ${t.audio_duration_secs}s, ${t.words.length} palavras; veja assets/words.txt)`);
