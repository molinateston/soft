// Procura prints candidatos no índice de prints (texto lido por OCR).
// Rode na pasta de trabalho: node <skill>/scripts/achar-prints.mjs "seguidores" "1,6 mi" [--min-w 600] [--since 2026-01-01] [--limit 15] [--indice prints-index.json]
// Nota = quantos termos da busca aparecem no texto do print (sem diferença de acento e maiúscula).
// SEMPRE abra e olhe o candidato antes de usar.
import { readFileSync, existsSync } from "node:fs";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const flags = new Set(["--min-w", "--since", "--limit", "--indice"]);
const terms = argv.filter((a, i) => !a.startsWith("--") && !flags.has(argv[i - 1]));
const arq = opt("--indice", "prints-index.json");
if (!existsSync(arq)) { console.error(`sem índice em ${arq}. Rode antes: node <skill>/scripts/indexar-prints.mjs`); process.exit(1); }
const idx = JSON.parse(readFileSync(arq, "utf8").replace(/^﻿/, ""));
const norm = (s) => (s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
const minW = Number(opt("--min-w", 0)), since = opt("--since", ""), limit = Number(opt("--limit", 15));

const hits = idx
  .filter((x) => x.w >= minW && (!since || x.date >= since))
  .map((x) => ({ x, score: terms.reduce((n, t) => n + (norm(x.text + " " + x.name).includes(norm(t)) ? 1 : 0), 0) }))
  .filter((h) => h.score > 0 || !terms.length)
  .sort((a, b) => b.score - a.score || b.x.date.localeCompare(a.x.date))
  .slice(0, limit);
for (const { x, score } of hits) console.log(`${score} | ${x.date} | ${x.w}x${x.h} | ${x.file}\n    ${norm(x.text).replace(/\s+/g, " ").slice(0, 160)}`);
if (!hits.length) console.log("nenhum print encontrado");
