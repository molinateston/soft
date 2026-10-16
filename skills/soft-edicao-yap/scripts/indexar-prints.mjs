// Monta um índice pesquisável dos prints do dono, com OCR local (Linux, Mac e Windows).
// Rode na pasta de trabalho: node <skill>/scripts/indexar-prints.mjs [--pasta <dir>] [--saida prints-index.json] [--lang por]
// Pasta padrão: "pasta_prints" do perfil.json. Incremental: imagem já indexada (mesmo caminho e tamanho) é pulada.
// OCR: usa o programa tesseract se estiver instalado. Sem ele, o índice sai só com nome, data e tamanho
// (a busca vira por nome e data) e o script diz como instalar.
import { readFileSync, writeFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { join, resolve, isAbsolute } from "node:path";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const perfil = existsSync("perfil.json") ? JSON.parse(readFileSync("perfil.json", "utf8")) : {};
let pasta = opt("--pasta", perfil.pasta_prints || "");
if (!pasta) { console.error("diga onde ficam os prints: --pasta <dir> ou \"pasta_prints\" no perfil.json"); process.exit(1); }
if (pasta.startsWith("~")) pasta = join(process.env.HOME || process.env.USERPROFILE || "", pasta.slice(1));
pasta = isAbsolute(pasta) ? pasta : resolve(pasta);
if (!existsSync(pasta)) { console.error(`pasta de prints não encontrada: ${pasta}`); process.exit(1); }
const saida = resolve(opt("--saida", "prints-index.json"));

const tess = spawnSync("tesseract", ["--list-langs"], { encoding: "utf8" });
const temOcr = tess.status === 0;
let lang = opt("--lang", "por");
if (temOcr && !tess.stdout.split(/\s+/).includes(lang)) {
  console.warn(`aviso: o tesseract não tem o idioma "${lang}"; usando "eng". Instale o pacote de idioma português para ler acentos.`);
  lang = "eng";
}
if (!temOcr) console.warn("aviso: tesseract não encontrado; o índice sai sem texto. Instale: Linux \"sudo apt install tesseract-ocr tesseract-ocr-por\", Mac \"brew install tesseract tesseract-lang\", Windows \"winget install UB-Mannheim.TesseractOCR\" (marque Portuguese).");

const index = new Map();
if (existsSync(saida)) for (const x of JSON.parse(readFileSync(saida, "utf8").replace(/^﻿/, ""))) index.set(x.file, x);

const files = [];
const walk = (d) => { for (const e of readdirSync(d, { withFileTypes: true })) { const p = join(d, e.name); if (e.isDirectory()) walk(p); else if (/\.(png|jpe?g)$/i.test(e.name)) files.push(p); } };
walk(pasta);

const pad = (n) => String(n).padStart(2, "0");
let novos = 0;
for (const file of files) {
  const st = statSync(file);
  const old = index.get(file);
  if (old && old.bytes === st.size && (old.ocr || !temOcr)) continue;
  const pr = spawnSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", file], { encoding: "utf8" });
  const [w, h] = (pr.stdout || "0x0").trim().split("x").map(Number);
  let text = "";
  if (temOcr) {
    const r = spawnSync("tesseract", [file, "stdout", "-l", lang], { encoding: "utf8", maxBuffer: 1 << 24 });
    text = r.status === 0 ? r.stdout.replace(/\s+/g, " ").trim().slice(0, 600) : "";
  }
  const m = st.mtime;
  index.set(file, { file, name: file.split(/[\\/]/).pop(), date: `${m.getFullYear()}-${pad(m.getMonth() + 1)}-${pad(m.getDate())} ${pad(m.getHours())}:${pad(m.getMinutes())}`, w: w || 0, h: h || 0, bytes: st.size, ocr: temOcr, text });
  novos++;
}
const lista = [...index.values()].filter((x) => existsSync(x.file)).sort((a, b) => b.date.localeCompare(a.date));
writeFileSync(saida, JSON.stringify(lista, null, 1));
console.log(`indexados novos=${novos} total=${lista.length} ocr=${temOcr ? lang : "não"} -> ${saida}`);
