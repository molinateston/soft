// Lista os prints candidatos da pasta de prints do dono (campo pasta_prints do perfil.json), do mais novo ao mais velho.
// Uso: node <skill>/scripts/listar-prints.mjs ["termo no nome do arquivo" ...] [--pasta CAMINHO] [--desde 2026-01-01] [--limite 20]
// Não lê o conteúdo da imagem: filtra por nome e data. ABRA cada candidato antes de usar e anote a origem.
import { readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";
import { lerPerfil } from "./ferramentas.mjs";

const argv = process.argv.slice(2);
const opt = (k, d) => (argv.includes(k) ? argv[argv.indexOf(k) + 1] : d);
const comValor = new Set(["--pasta", "--desde", "--limite"]);
const termos = argv.filter((a, i) => !a.startsWith("--") && !comValor.has(argv[i - 1]));
const pasta = opt("--pasta", lerPerfil().dados.pasta_prints);
if (!pasta) { console.error("sem pasta de prints: preencha pasta_prints no perfil.json ou use --pasta"); process.exit(1); }
const desde = opt("--desde", ""), limite = Number(opt("--limite", 20));
const norm = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
const imagens = new Set([".png", ".jpg", ".jpeg", ".webp"]);

const todos = [];
const varre = (d, nivel) => {
  for (const nome of readdirSync(d)) {
    const p = join(d, nome);
    let st; try { st = statSync(p); } catch { continue; }
    if (st.isDirectory() && nivel < 2) varre(p, nivel + 1);
    else if (imagens.has(extname(nome).toLowerCase())) todos.push({ p, data: st.mtime.toISOString().slice(0, 10), kb: Math.round(st.size / 1024) });
  }
};
varre(pasta, 0);
const achados = todos
  .filter((x) => !desde || x.data >= desde)
  .filter((x) => !termos.length || termos.some((t) => norm(x.p).includes(norm(t))))
  .sort((a, b) => b.data.localeCompare(a.data))
  .slice(0, limite);
for (const x of achados) console.log(`${x.data} | ${String(x.kb).padStart(6)} KB | ${x.p}`);
if (!achados.length) console.log("nenhum print encontrado com esse filtro");
