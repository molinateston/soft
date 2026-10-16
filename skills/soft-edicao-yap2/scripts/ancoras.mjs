// Mostra o tempo, na linha do tempo final, de cada frase falada, para marcar a entrada dos elementos.
// Rode na raiz do projeto: node <skill>/scripts/ancoras.mjs "menos seguidores" "do que eu" ...
import { readFileSync } from "node:fs";
const w = JSON.parse(readFileSync("assets/transcricao.json", "utf8")).words;
const n = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9%]/g, "");
for (const frase of process.argv.slice(2)) {
  const p = frase.split(/\s+/).map(n);
  const achados = [];
  for (let i = 0; i < w.length; i++) if (p.every((x, j) => w[i + j] && n(w[i + j].text) === x)) achados.push(`${w[i].start.toFixed(2)} a ${w[i + p.length - 1].end.toFixed(2)}`);
  console.log(`${frase.padEnd(32)} ${achados.join("  ") || "não achei"}`);
}
