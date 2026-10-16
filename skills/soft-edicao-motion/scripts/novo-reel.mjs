// Cria o projeto de um reel Motion a partir da gravação do celular e transcreve a fala.
// Rode na PASTA DE TRABALHO (onde ficam perfil.json, node_modules e video-projects/):
//   node <skill>/scripts/novo-reel.mjs "<video>" <slug> [--transcricao <arquivo.json>] [--sem-transcricao]
// Cria video-projects/<slug>/ com assets/raw.mp4 (1080x1920, 30 fps), assets/raw.json (tempo por palavra),
// assets/words.txt (palavras com tempo e pausas), fontes, gsap, o kit de cenas, reel.json (identidade) e src/.
// --transcricao: usa uma transcrição que já existe, no tempo do vídeo bruto. Aceita {"words":[{text,start,end}]}
//                ou uma lista [{w|text, s|start, e|end}]. Assim a transcrição não roda de novo.
// --sem-transcricao: só monta o projeto; ponha um assets/raw.json seu e rode de novo para gerar o words.txt.
import { execFileSync, spawnSync } from "node:child_process";
import { cpSync, copyFileSync, mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { dirname, join, resolve, extname, isAbsolute } from "node:path";
import { homedir } from "node:os";

const args = process.argv.slice(2);
const opt = (k) => (args.includes(k) ? args[args.indexOf(k) + 1] : "");
const semTranscricao = args.includes("--sem-transcricao");
const transcricao = opt("--transcricao");
const [src, slug] = args.filter((a, i) => !a.startsWith("--") && args[i - 1] !== "--transcricao");
if (!src || !slug) { console.error('uso: node novo-reel.mjs "<video>" <slug> [--transcricao <arquivo.json>] [--sem-transcricao]'); process.exit(1); }
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) { console.error("slug em minúsculas, sem acento, com hífens (ex.: reel-agentes)"); process.exit(1); }

const skill = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const trabalho = process.cwd();
const perfil = existsSync("perfil.json") ? JSON.parse(readFileSync("perfil.json", "utf8")) : null;
if (!perfil) console.warn("aviso: sem perfil.json nesta pasta. Identidade neutra: só branco e as fontes livres padrão. Esquema em references/perfil.md.");

const proj = resolve("video-projects", slug);
const a = join(proj, "assets");
for (const d of ["assets/fonts", "src", "renders", "conferencia"]) mkdirSync(join(proj, d), { recursive: true });

// GSAP: vem da instalação da pasta de trabalho (Primeiros passos do SKILL.md).
let gsap;
try { gsap = createRequire(join(trabalho, "package.json")).resolve("gsap/dist/gsap.min.js"); }
catch { console.error("FALTA gsap. Na pasta de trabalho: npm install hyperframes@0.8.93 gsap@3.14.2"); process.exit(2); }
copyFileSync(gsap, join(a, "gsap.min.js"));
copyFileSync(join(skill, "template", "motion-kit.js"), join(a, "motion-kit.js"));

// Fontes: título (palavras grandes e objetos) e legenda. A do perfil, se o dono declarou e o arquivo existe; senão a livre padrão.
const fonte = (campo, nome, padrao, rotuloPadrao) => {
  const fp = perfil?.[campo] ? (isAbsolute(perfil[campo]) ? perfil[campo] : resolve(trabalho, perfil[campo])) : "";
  if (fp && existsSync(fp)) {
    const dest = `assets/fonts/${nome}${extname(fp).toLowerCase()}`;
    copyFileSync(fp, join(proj, dest));
    return { arquivo: dest, origem: `perfil.json: ${perfil[campo]}` };
  }
  if (fp) console.warn(`aviso: ${campo} do perfil não encontrada (${perfil[campo]}); usando a livre padrão.`);
  const dest = `assets/fonts/${nome}${extname(padrao)}`;
  copyFileSync(join(skill, "template", "fonts", padrao), join(proj, dest));
  return { arquivo: dest, origem: `padrão livre: ${rotuloPadrao} (OFL 1.1)` };
};
const ft = fonte("fonte_titulo", "titulo", "Inter-Black.otf", "Inter Black");
const fl = fonte("fonte_legenda", "legenda", "JetBrainsMono-Bold.ttf", "JetBrains Mono Bold");

// Identidade do vídeo: reel.json (ajuste por vídeo no passo de enquadramento).
const hex = /^#[0-9a-fA-F]{6}$/;
if (perfil?.cor_acento && !hex.test(perfil.cor_acento)) console.warn(`aviso: cor_acento "${perfil.cor_acento}" não é #RRGGBB; ficando sem acento.`);
if (!existsSync(join(proj, "reel.json"))) {
  writeFileSync(join(proj, "reel.json"), JSON.stringify({
    acento: perfil?.cor_acento && hex.test(perfil.cor_acento) ? perfil.cor_acento : "",
    fonteTitulo: ft.arquivo, origemFonteTitulo: ft.origem,
    fonteLegenda: fl.arquivo, origemFonteLegenda: fl.origem,
    capY: 1490, camZoom: 1, camOrigemY: 960, aberturaCamY: 490,
    rosto: { x: 250, y: 180, w: 570, h: 860 },
  }, null, 2) + "\n");
}
writeFileSync(join(proj, "meta.json"), JSON.stringify({ id: "reel", name: slug, width: 1096, height: 1920, fps: 30 }, null, 2) + "\n");
writeFileSync(join(proj, "hyperframes.json"), JSON.stringify({ paths: { blocks: "compositions", components: "compositions/components", assets: "assets" } }, null, 2) + "\n");
if (!existsSync(join(proj, "src", "index.template.html"))) cpSync(join(skill, "template", "index.template.html"), join(proj, "src", "index.template.html"));
if (!existsSync(join(proj, "src", "cenas.json"))) cpSync(join(skill, "template", "cenas.exemplo.json"), join(proj, "src", "cenas.json"));

if (!existsSync(join(a, "raw.mp4"))) {
  console.log("convertendo para 1080x1920, 30 fps…");
  // o ffmpeg aplica a rotação gravada pelo celular, então a saída fica em pé
  execFileSync("ffmpeg", ["-y", "-v", "error", "-i", src, "-map", "0:v:0", "-map", "0:a:0", "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", join(a, "raw.mp4")], { stdio: "inherit" });
}

if (transcricao && !existsSync(join(a, "raw.json"))) {
  const j = JSON.parse(readFileSync(transcricao, "utf8"));
  const lista = Array.isArray(j) ? j : j.words;
  const words = lista.map((w) => ({ text: String(w.text ?? w.w).trim(), start: +(w.start ?? w.s), end: +(w.end ?? w.e) })).filter((w) => w.text && w.end >= w.start);
  const dur = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", join(a, "raw.mp4")], { encoding: "utf8" }).trim());
  writeFileSync(join(a, "raw.json"), JSON.stringify({ language_code: "pt", audio_duration_secs: +dur.toFixed(3), origem: transcricao, words }, null, 1));
  console.log(`transcrição importada: ${words.length} palavras de ${transcricao}`);
}

if (!existsSync(join(a, "raw.json")) && !semTranscricao) {
  const venv = join(homedir(), ".venvs", "whisper", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  const PY = process.env.WHISPER_PYTHON || (existsSync(venv) ? venv : (process.platform === "win32" ? "python" : "python3"));
  const ok = spawnSync(PY, ["-c", "import faster_whisper"], { stdio: "ignore" }).status === 0;
  if (!ok) {
    console.error(`FALTA a transcrição local (faster-whisper) em ${PY}. Veja "Primeiros passos" no SKILL.md, ou passe uma transcrição pronta com --transcricao.\nO projeto já está montado em ${proj}; rode este comando de novo depois.`);
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
