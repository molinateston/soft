// Cria o projeto de um reel no estilo Direto a partir da gravação e transcreve a fala.
// Rode na PASTA DE TRABALHO (onde ficam perfil.json, node_modules e video-projects/):
//   node <skill>/scripts/novo-reel.mjs "<video>" <slug> [--transcricao <arquivo.json>] [--sem-transcricao]
// Cria video-projects/<slug>/ com assets/raw.mp4 (1080x1920, 30 fps), assets/raw.json (tempo por palavra),
// assets/words.txt (palavras com tempo e pausas), fontes, gsap, reel.json (identidade e plano do vídeo) e o template.
// --transcricao: usa uma transcrição que já existe (lista de {text|word|w, start|s, end|e} ou {words:[...]}).
// --sem-transcricao: só monta o projeto; ponha um assets/raw.json seu e rode de novo para gerar o words.txt.
import { execFileSync, spawnSync } from "node:child_process";
import { cpSync, copyFileSync, mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import { dirname, join, resolve, extname, isAbsolute } from "node:path";
import { homedir } from "node:os";

const args = process.argv.slice(2);
const semTranscricao = args.includes("--sem-transcricao");
const tIdx = args.indexOf("--transcricao"), transcricaoPronta = tIdx >= 0 ? args[tIdx + 1] : "";
const [src, slug] = args.filter((a, i) => !a.startsWith("--") && !(tIdx >= 0 && i === tIdx + 1));
if (!src || !slug) { console.error('uso: node novo-reel.mjs "<video>" <slug> [--transcricao <arquivo.json>] [--sem-transcricao]'); process.exit(1); }
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) { console.error("slug em minúsculas, sem acento, com hífens (ex.: reel-algoritmo)"); process.exit(1); }

const skill = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const trabalho = process.cwd();
const perfil = existsSync("perfil.json") ? JSON.parse(readFileSync("perfil.json", "utf8")) : null;
if (!perfil) console.warn("aviso: sem perfil.json nesta pasta. Identidade neutra: só branco e a fonte livre padrão. Esquema em references/perfil.md.");

const proj = resolve("video-projects", slug);
const a = join(proj, "assets");
for (const d of ["assets/fonts", "assets/apoios", "src", "renders"]) mkdirSync(join(proj, d), { recursive: true });

// GSAP: vem da instalação da pasta de trabalho (Primeiros passos do SKILL.md).
let gsap;
try { gsap = createRequire(join(trabalho, "package.json")).resolve("gsap/dist/gsap.min.js"); }
catch { console.error("FALTA gsap. Na pasta de trabalho: npm install hyperframes@0.8.93 gsap@3.14.2"); process.exit(2); }
copyFileSync(gsap, join(a, "gsap.min.js"));

// Fontes livres da skill (OFL 1.1): Inter Black (headline), Inter Bold (CTA), JetBrains Mono (legenda).
for (const f of ["Inter-Black.otf", "Inter-Bold.otf", "JetBrainsMono-Regular.ttf"]) copyFileSync(join(skill, "template", "fonts", f), join(a, "fonts", f));
// Fonte do título (headline e CTA): a do perfil, se o dono declarou e o arquivo existe; senão, as livres padrão.
let fonteTitulo = "assets/fonts/Inter-Black.otf", fonteChamada = "assets/fonts/Inter-Bold.otf", origemFonte = "padrão livre: Inter Black e Inter Bold (OFL 1.1)";
const fp = perfil?.fonte_titulo ? (isAbsolute(perfil.fonte_titulo) ? perfil.fonte_titulo : resolve(trabalho, perfil.fonte_titulo)) : "";
if (fp && existsSync(fp)) {
  fonteTitulo = `assets/fonts/titulo${extname(fp).toLowerCase()}`;
  copyFileSync(fp, join(proj, fonteTitulo));
  fonteChamada = fonteTitulo;
  origemFonte = `perfil.json: ${perfil.fonte_titulo}`;
} else if (fp) console.warn(`aviso: fonte_titulo do perfil não encontrada (${perfil.fonte_titulo}); usando a livre padrão.`);

// Identidade do vídeo: reel.json (pode ser ajustado à mão por vídeo).
const hex = /^#[0-9a-fA-F]{6}$/;
if (perfil?.cor_acento && !hex.test(perfil.cor_acento)) console.warn(`aviso: cor_acento "${perfil.cor_acento}" não é #RRGGBB; ficando sem acento.`);
if (!existsSync(join(proj, "reel.json"))) {
  // Plano do vídeo: preencha no fluxo do SKILL.md (os valores abaixo são o padrão do estilo, não de um vídeo).
  writeFileSync(join(proj, "reel.json"), JSON.stringify({
    acento: perfil?.cor_acento && hex.test(perfil.cor_acento) ? perfil.cor_acento : "",
    fonteTitulo, fonteChamada, origemFonte,
    velocidade: 1.2,
    pausa_max: 0.7,
    corpo_recorte: [720, 1280, 180, 320],
    abertura: { segundos: 5, imagem: "assets/abertura.png", linhas: ["Primeira linha da headline", "segunda com *destaque*"], janela_y: null },
    apoios: [
      { imagem: "assets/apoios/apoio-1.png", fala: "trecho literal da fala", duracao: 2.5, origem: "" },
      { imagem: "assets/apoios/apoio-2.png", fala: "trecho literal da fala", duracao: 2.5, origem: "" },
      { imagem: "assets/apoios/apoio-3.png", fala: "trecho literal da fala", duracao: 2.5, origem: "" },
    ],
    cta: { texto: "Frase do pedido como foi falada", fala: "verbo do pedido" },
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

if (!existsSync(join(a, "raw.json")) && transcricaoPronta) {
  // Transcrição que já existe: normaliza para {words:[{text,start,end}], audio_duration_secs}.
  const j = JSON.parse(readFileSync(transcricaoPronta, "utf8"));
  const lista = Array.isArray(j) ? j : j.words || j.palavras || [];
  const words = lista.map((w) => ({ text: String(w.text ?? w.word ?? w.w ?? "").trim(), start: +(w.start ?? w.s), end: +(w.end ?? w.e) }))
    .filter((w) => w.text && Number.isFinite(w.start) && Number.isFinite(w.end));
  if (!words.length) { console.error(`transcrição sem palavras com tempo: ${transcricaoPronta}`); process.exit(1); }
  const dur = Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", join(a, "raw.mp4")], { encoding: "utf8" }).trim());
  writeFileSync(join(a, "raw.json"), JSON.stringify({ origem: transcricaoPronta, audio_duration_secs: +dur.toFixed(3), words }, null, 1));
  console.log(`transcrição importada: ${words.length} palavras`);
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
