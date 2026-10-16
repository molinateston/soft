// Confere se a máquina tem tudo o que esta skill usa. Rode na pasta de trabalho do dono:
//   node <skill>/scripts/conferir.mjs
// Cada linha sai "ok", "aviso" ou "FALTA", com o que fazer. Não instala nada.
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, isAbsolute, join } from "node:path";
import { homedir } from "node:os";
import { arquivoGsap, binHyperframes, envMotor, lerPerfil, pastaFerramentas, pythonTranscricao } from "./ferramentas.mjs";

const linhas = [];
const marca = (estado, item, detalhe) => linhas.push(`${estado.padEnd(6)}${item.padEnd(22)}${detalhe}`);
const roda = (cmd, args, extra = {}) => spawnSync(cmd, args, { encoding: "utf8", ...extra });

const maior = Number(process.versions.node.split(".")[0]);
marca(maior >= 22 ? "ok" : "FALTA", "node", maior >= 22 ? `v${process.versions.node}` : `v${process.versions.node}; instale o Node 22 ou mais novo (nodejs.org)`);

for (const bin of ["ffmpeg", "ffprobe"]) {
  const r = roda(bin, ["-version"]);
  marca(r.status === 0 ? "ok" : "FALTA", bin, r.status === 0 ? r.stdout.split("\n")[0].slice(0, 60) : "instale o ffmpeg (ffmpeg.org; Mac: brew install ffmpeg; Windows: winget install ffmpeg)");
}
const enc = roda("ffmpeg", ["-hide_banner", "-encoders"]);
for (const e of ["libx264", "aac"]) marca(enc.stdout && enc.stdout.includes(e) ? "ok" : "FALTA", `encoder ${e}`, enc.stdout && enc.stdout.includes(e) ? "presente" : "use um ffmpeg completo (com libx264)");

const hf = binHyperframes();
if (existsSync(hf)) {
  const v = roda(process.execPath, [hf, "--version"], { env: envMotor() });
  marca("ok", "hyperframes", `${(v.stdout || "").trim().split("\n").pop()} em ${pastaFerramentas()}`);
  const b = roda(process.execPath, [hf, "browser", "path"], { env: envMotor() });
  const caminho = (b.stdout || "").trim().split("\n").pop();
  marca(b.status === 0 && caminho ? "ok" : "FALTA", "chrome do render", b.status === 0 && caminho ? caminho.slice(-70) : `rode: node ${hf} browser ensure`);
} else marca("FALTA", "hyperframes", "rode: npm install --prefix ferramentas-video hyperframes@0.8.93 gsap@3.14.2");
marca(existsSync(arquivoGsap()) ? "ok" : "FALTA", "gsap", existsSync(arquivoGsap()) ? "gsap.min.js presente" : "vem no mesmo npm install do hyperframes");

const py = pythonTranscricao(homedir());
const fw = roda(py, ["-c", "import faster_whisper; print(faster_whisper.__version__)"]);
marca(fw.status === 0 ? "ok" : "aviso", "transcrição local", fw.status === 0 ? `faster-whisper ${fw.stdout.trim()} (${py})` : "faster-whisper ausente; veja Primeiros passos, ou escreva a transcrição à mão");

const { caminho, dados } = lerPerfil();
if (!caminho) marca("aviso", "perfil.json", "ainda não existe; a skill pergunta uma vez e salva (sem ele: só branco)");
else {
  const cor = dados.cor_acento;
  const corOk = !cor || /^#[0-9a-fA-F]{6}$/.test(cor);
  marca(corOk ? "ok" : "FALTA", "perfil.json", corOk ? `${caminho} (acento ${cor || "nenhum: só branco"})` : `cor_acento "${cor}" fora do formato #RRGGBB`);
  for (const f of ["fonte_texto", "fonte_destaque", "avatar", "logo"]) if (dados[f] && !existsSync(isAbsolute(dados[f]) ? dados[f] : join(dirname(caminho), dados[f]))) marca("aviso", f, `arquivo não encontrado: ${dados[f]}`);
}

console.log(linhas.join("\n"));
const falta = linhas.filter((l) => l.startsWith("FALTA")).length;
console.log(falta ? `\n${falta} item(ns) faltando. Resolva antes de editar.` : "\nTudo pronto para editar.");
process.exit(falta ? 1 : 0);
