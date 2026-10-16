// Cria o projeto de um reel editorial a partir da gravação e transcreve o bruto.
// Rode na pasta de trabalho do dono:
//   node <skill>/scripts/novo-reel.mjs "<video>" <slug> ["<angulo2>" ...] [--sem-transcricao]
// Vídeos extras são outros ângulos de câmera do MESMO take (sincronizados depois) -> assets/angulo2.mp4 ...
// Cria projetos-video/<slug>/ com assets/bruto.mp4 (1080x1920, 30 fps), bruto.json, palavras.txt,
// fontes, gsap.min.js, src/index.template.html, DESIGN.md e meta.json.
// Pode rodar de novo: o que já existe fica. Se você escreveu assets/bruto.json à mão, ele só gera palavras.txt.
import { execFileSync } from "node:child_process";
import { copyFileSync, cpSync, mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";
import { homedir } from "node:os";
import { arquivoGsap, pythonTranscricao } from "./ferramentas.mjs";

const args = process.argv.slice(2);
const semTranscricao = args.includes("--sem-transcricao");
const [src, slug, ...angulos] = args.filter((a) => !a.startsWith("--"));
if (!src || !slug) { console.error('uso: novo-reel.mjs "<video>" <slug> ["<angulo2>" ...] [--sem-transcricao]'); process.exit(1); }
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) { console.error("slug em minúsculas, sem acento, com hífens (ex.: reel-precos)"); process.exit(1); }
if (!existsSync(src)) { console.error(`vídeo não encontrado: ${src}`); process.exit(1); }

const skill = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const proj = resolve("projetos-video", slug);
const a = join(proj, "assets");
for (const d of [a, join(proj, "src"), join(proj, "renders"), join(proj, "conferencia"), join(a, "prints"), join(a, "thumbs")]) mkdirSync(d, { recursive: true });

cpSync(join(skill, "template", "fonts"), join(a, "fonts"), { recursive: true });
if (!existsSync(join(proj, "src", "index.template.html"))) copyFileSync(join(skill, "template", "index.template.html"), join(proj, "src", "index.template.html"));
copyFileSync(join(skill, "template", "DESIGN.md"), join(proj, "DESIGN.md"));
const gsap = arquivoGsap();
if (!existsSync(gsap)) { console.error(`GSAP não encontrado em ${gsap}. Rode os Primeiros passos do SKILL.md.`); process.exit(2); }
copyFileSync(gsap, join(a, "gsap.min.js"));
if (!existsSync(join(proj, "meta.json"))) writeFileSync(join(proj, "meta.json"), JSON.stringify({ id: "reel", name: slug, width: 1080, height: 1920, fps: 30 }, null, 2) + "\n");

const vertical = (entrada, saida) => execFileSync("ffmpeg", ["-y", "-v", "error", "-i", entrada, "-map", "0:v:0", "-map", "0:a:0?",
  "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
  "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30", "-pix_fmt", "yuv420p",
  "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", saida], { stdio: "inherit" });
if (!existsSync(join(a, "bruto.mp4"))) { console.log("convertendo para 1080x1920, 30 fps..."); vertical(src, join(a, "bruto.mp4")); }
angulos.forEach((p, i) => { const out = join(a, `angulo${i + 2}.mp4`); if (!existsSync(out)) vertical(p, out); });

const json = join(a, "bruto.json");
if (!existsSync(json) && !semTranscricao) {
  console.log("transcrevendo (local; na primeira vez baixa o modelo e demora)...");
  try {
    execFileSync(pythonTranscricao(homedir()), [join(skill, "scripts", "transcrever.py"), join(a, "bruto.mp4"), json],
      { stdio: ["ignore", "inherit", "inherit"], env: { ...process.env, PYTHONIOENCODING: "utf-8" } });
  } catch {
    console.error("A transcrição local não rodou. Instale pelos Primeiros passos do SKILL.md ou escreva assets/bruto.json à mão e rode este comando de novo.");
  }
}
if (!existsSync(json)) { console.log(`projeto criado sem transcrição: ${proj}`); process.exit(0); }

const t = JSON.parse(readFileSync(json, "utf8"));
let out = "", linha = "", ini = 0, ant = 0;
for (const w of t.words) {
  if (w.start - ant > 0.5 || linha.length > 90) {
    if (linha) out += `${ini.toFixed(2).padStart(7)} ${linha}\n`;
    if (w.start - ant > 0.5) out += `        --- pausa ${(w.start - ant).toFixed(1)}s\n`;
    linha = ""; ini = w.start;
  }
  linha += `${w.text}@${w.start.toFixed(2)} `; ant = w.end;
}
out += `${ini.toFixed(2).padStart(7)} ${linha}\n`;
writeFileSync(join(a, "palavras.txt"), out);
console.log(`pronto: ${proj}  (duração ${t.audio_duration_secs}s, ${t.words.length} palavras; leia assets/palavras.txt)`);
