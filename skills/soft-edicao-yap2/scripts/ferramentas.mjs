// Onde moram as ferramentas do motor (HyperFrames e GSAP) e como chamá-las, igual em Linux, Mac e Windows.
// A pasta das ferramentas é a variável EDICAO_FERRAMENTAS ou, sem ela, ./ferramentas-video na pasta de trabalho.
// Instalação (uma vez, ver "Primeiros passos" no SKILL.md):
//   npm install --prefix ferramentas-video hyperframes@0.8.93 gsap@3.14.2
//   node ferramentas-video/node_modules/hyperframes/bin/hyperframes.mjs browser ensure
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

export const pastaFerramentas = () => resolve(process.env.EDICAO_FERRAMENTAS || "ferramentas-video");
export const binHyperframes = () => join(pastaFerramentas(), "node_modules", "hyperframes", "bin", "hyperframes.mjs");
export const arquivoGsap = () => join(pastaFerramentas(), "node_modules", "gsap", "dist", "gsap.min.js");
// O teto de 300 s do motor para extrair quadros estoura em máquina carregada: 900 s.
export const envMotor = () => ({ ...process.env, HYPERFRAMES_NO_TELEMETRY: "1", FFMPEG_PROCESS_TIMEOUT_MS: process.env.FFMPEG_PROCESS_TIMEOUT_MS || "900000" });

// Roda o HyperFrames com o node atual. Devolve o resultado do spawnSync.
export function hyperframes(args, opcoes = {}) {
  const bin = binHyperframes();
  if (!existsSync(bin)) {
    console.error(`HyperFrames não encontrado em ${bin}.\nInstale: npm install --prefix ferramentas-video hyperframes@0.8.93 gsap@3.14.2`);
    process.exit(2);
  }
  return spawnSync(process.execPath, [bin, ...args], { stdio: "inherit", env: envMotor(), ...opcoes });
}

// Procura o perfil.json do dono: na pasta atual e subindo até a raiz.
export function lerPerfil(inicio = process.cwd()) {
  let d = resolve(inicio);
  for (;;) {
    const p = join(d, "perfil.json");
    if (existsSync(p)) return { caminho: p, dados: JSON.parse(readFileSync(p, "utf8").replace(/^﻿/, "")) };
    const cima = dirname(d);
    if (cima === d) return { caminho: null, dados: {} };
    d = cima;
  }
}

// Python da transcrição: WHISPER_PYTHON, ou o ambiente ~/.venvs/whisper, ou python3/python do sistema.
export function pythonTranscricao(home) {
  if (process.env.WHISPER_PYTHON) return process.env.WHISPER_PYTHON;
  const venv = join(home, ".venvs", "whisper", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");
  if (existsSync(venv)) return venv;
  return process.platform === "win32" ? "python" : "python3";
}
