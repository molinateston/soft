// Confere tudo que a skill usa, nesta máquina, e diz como instalar o que faltar.
// Rode na pasta de trabalho: node <skill>/scripts/conferir-ambiente.mjs
// Sai com 0 quando o obrigatório está ok, 1 quando falta algo obrigatório.
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { join, resolve, dirname, isAbsolute } from "node:path";
import { homedir } from "node:os";

const win = process.platform === "win32", mac = process.platform === "darwin";
const rows = [];
let falta = 0;
const item = (nome, ok, obrig, detalhe, comoInstalar) => {
  rows.push(`${ok ? "ok    " : obrig ? "FALTA " : "aviso "} ${nome.padEnd(22)} ${detalhe}${ok || !comoInstalar ? "" : `\n         como instalar: ${comoInstalar}`}`);
  if (!ok && obrig) falta++;
};
const run = (cmd, args) => { const r = spawnSync(cmd, args, { encoding: "utf8" }); return r.status === 0 ? (r.stdout || r.stderr || "").trim() : null; };

const major = Number(process.versions.node.split(".")[0]);
item("node 22 ou mais", major >= 22, true, `v${process.versions.node}`, "https://nodejs.org (versão LTS 22 ou mais)");

const pacoteSistema = (linux, macos, windows) => (win ? windows : mac ? macos : linux);
const ff = run("ffmpeg", ["-version"]), fp = run("ffprobe", ["-version"]);
item("ffmpeg", !!ff, true, ff ? ff.split("\n")[0].slice(0, 60) : "não encontrado", pacoteSistema("sudo apt install ffmpeg", "brew install ffmpeg", "winget install Gyan.FFmpeg"));
item("ffprobe", !!fp, true, fp ? "presente" : "não encontrado", "vem junto com o ffmpeg");

const req = createRequire(join(process.cwd(), "package.json"));
const versao = (p) => { try { return JSON.parse(readFileSync(req.resolve(`${p}/package.json`), "utf8")).version; } catch { return null; } };
const hf = versao("hyperframes"), gs = versao("gsap");
item("hyperframes", !!hf, true, hf ? `v${hf}${hf === "0.8.93" ? "" : " (a skill foi provada na 0.8.93)"}` : "não instalado nesta pasta", "npm install hyperframes@0.8.93 gsap@3.14.2 (nesta pasta de trabalho)");
item("gsap", !!gs, true, gs ? `v${gs}` : "não instalado nesta pasta", "npm install gsap@3.14.2");

if (hf) {
  const bin = join(dirname(req.resolve("hyperframes/package.json")), "bin", "hyperframes.mjs");
  const p = existsSync(bin) ? run(process.execPath, [bin, "browser", "path"]) : null;
  const caminho = process.env.HYPERFRAMES_BROWSER_PATH || (p ? p.split("\n").pop() : "");
  item("Chrome do render", !!caminho && existsSync(caminho), true, caminho || "não encontrado", "npx hyperframes browser ensure");
}

const venv = join(homedir(), ".venvs", "whisper", win ? "Scripts/python.exe" : "bin/python");
const PY = process.env.WHISPER_PYTHON || (existsSync(venv) ? venv : win ? "python" : "python3");
const pyv = run(PY, ["--version"]);
item("python 3.10 ou mais", !!pyv, true, pyv ? `${pyv} (${PY})` : `não encontrado (${PY})`, "https://www.python.org");
const fw = pyv ? run(PY, ["-c", "import faster_whisper; print(faster_whisper.__version__)"]) : null;
item("faster-whisper", !!fw, true, fw ? `v${fw}` : "não importa nesse python (dispensável só se a transcrição já existe: novo-reel.mjs --transcricao)",
  `${win ? "python" : "python3"} -m venv ${win ? "%USERPROFILE%\\.venvs\\whisper" : "~/.venvs/whisper"} e depois ${win ? "%USERPROFILE%\\.venvs\\whisper\\Scripts\\pip" : "~/.venvs/whisper/bin/pip"} install faster-whisper==1.2.1`);

if (existsSync("perfil.json")) {
  try {
    const p = JSON.parse(readFileSync("perfil.json", "utf8"));
    const f = p.fonte_titulo ? (isAbsolute(p.fonte_titulo) ? p.fonte_titulo : resolve(p.fonte_titulo)) : "";
    item("perfil.json", true, false, `acento ${p.cor_acento || "nenhum (branco)"}; fonte do título ${p.fonte_titulo ? (existsSync(f) ? p.fonte_titulo : p.fonte_titulo + " NÃO ENCONTRADA") : "livre padrão (Inter Black)"}`);
  } catch (e) { item("perfil.json", false, true, `JSON inválido: ${e.message}`, "corrija o arquivo (esquema em references/perfil.md)"); }
} else item("perfil.json", false, false, "ausente: identidade neutra (só branco, fonte livre)", "a skill pergunta uma vez e salva (references/perfil.md)");

console.log(rows.join("\n"));
console.log(falta ? `\n${falta} item(ns) obrigatório(s) faltando.` : "\nAmbiente ok para editar.");
process.exit(falta ? 1 : 0);
