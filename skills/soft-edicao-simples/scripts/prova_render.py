#!/usr/bin/env python3
"""Prova curta de que o ambiente RENDERIZA, antes de qualquer edição. Sem prova, a skill não edita.

Uso:
  python3 prova_render.py --perfil hyperframes --pasta <pasta de trabalho> [--audio <vídeo ou áudio com fala>]
  python3 prova_render.py --perfil ffmpeg --pasta <pasta de trabalho> [--audio <vídeo ou áudio com fala>]

hyperframes: monta um projeto mínimo (1080x1920, 3 s, vídeo de fundo, áudio e um texto), renderiza com o
  HyperFrames da pasta do jeito que as skills renderizam (janela de 1096 px, quadros em png, recorte em 1080),
  confere com ffprobe (1080x1920, 30 fps, 3 s, áudio, arquivo íntegro), confere que o texto apareceu e
  que a borda direita não tem faixa preta.
ffmpeg: gera um vídeo de teste e passa pelas três codificações que as skills usam (conversão, corte e final),
  conferindo cada saída com ffprobe.
Os dois perfis rodam a transcrição local (faster-whisper do venv) sobre um áudio curto. Com --audio, usa os
  primeiros 10 s desse arquivo e exige palavras com tempo; sem --audio, prova que o motor carrega e roda.

Lê o ambiente.json que o instalar_ambiente.py gravou. Grava .ambiente/prova-render.json.
Saídas: 0 prova completa, 1 prova reprovou ou ambiente ausente, 2 argumento errado.
"""
import argparse, json, os, shutil, subprocess, sys, time
from datetime import datetime
from pathlib import Path

DUR, W, H, FPS = 3.0, 1080, 1920, 30
JANELA = 1096  # mesma janela das skills: o recorte para 1080 tira a faixa preta da borda direita


class ParserPt(argparse.ArgumentParser):
    def error(self, message):
        for en, pt in {"the following arguments are required": "faltam os argumentos", "invalid choice": "opção inválida",
                       "unrecognized arguments": "argumentos desconhecidos", "expected one argument": "esperava um valor", "choose from": "escolha entre", "argument ": "argumento "}.items():
            message = message.replace(en, pt)
        sys.stderr.write(f"argumento errado: {message}\n\n{self.format_usage().replace('usage:', 'uso:')}")
        sys.exit(2)


def rodar(cmd, env, cwd=None, timeout=900, binario=False):
    try:
        r = subprocess.run(cmd, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
                           text=not binario, **({} if binario else {"encoding": "utf-8", "errors": "replace"}))
        return r.returncode, r.stdout, (r.stderr if not binario else r.stderr.decode("utf-8", "replace"))
    except (OSError, subprocess.TimeoutExpired) as e:
        return 127, b"" if binario else "", str(e)


class Prova:
    def __init__(self, args):
        self.args = args
        self.pasta = Path(args.pasta).expanduser().resolve()
        self.itens = []
        amb_json = self.pasta / "ambiente.json"
        if not amb_json.exists():
            raise SystemExit(self.fatal(f"não achei {amb_json}. Rode antes: python3 instalar_ambiente.py --perfil {args.perfil} --pasta {self.pasta}"))
        self.amb = json.loads(amb_json.read_text(encoding="utf-8"))
        if args.perfil == "hyperframes" and self.amb.get("perfil") != "hyperframes":
            raise SystemExit(self.fatal(f"o ambiente desta pasta foi instalado no perfil {self.amb.get('perfil')}; rode o instalador com --perfil hyperframes"))
        self.env = dict(os.environ)
        if self.amb.get("path_prefixo"):
            self.env["PATH"] = os.pathsep.join(self.amb["path_prefixo"] + [self.env.get("PATH", "")])
        self.env.update(self.amb.get("env", {}))
        self.ffmpeg = (self.amb.get("ffmpeg") or {}).get("caminho") or "ffmpeg"
        self.ffprobe = (self.amb.get("ffprobe") or {}).get("caminho") or "ffprobe"
        self.dir = self.pasta / ".ambiente" / "prova"
        shutil.rmtree(self.dir, ignore_errors=True)
        (self.dir / "assets").mkdir(parents=True)

    @staticmethod
    def fatal(msg):
        print(f"PROVA DE RENDER: NÃO RODOU\n{msg}", file=sys.stderr)
        return 1

    def item(self, nome, ok, detalhe):
        self.itens.append({"item": nome, "ok": bool(ok), "detalhe": detalhe})
        print(f"  {'ok   ' if ok else 'FALHA'} {nome:<40} {detalhe}", flush=True)
        return ok

    def ff(self, args, nome, timeout=600):
        rc, out, err = rodar([self.ffmpeg, "-y", "-hide_banner", "-v", "error"] + args, self.env, cwd=self.dir, timeout=timeout)
        if rc != 0:
            self.item(nome, False, f"ffmpeg saiu com {rc}: {err.strip()[-300:]}")
        return rc == 0

    # ---------- conferência de um mp4 com ffprobe
    def conferir_mp4(self, arq, rotulo, exige_audio=True):
        rc, out, err = rodar([self.ffprobe, "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration,size",
                              "-of", "json", str(arq)], self.env)
        if rc != 0:
            return self.item(f"{rotulo}: ffprobe", False, err.strip()[-200:])
        d = json.loads(out)
        v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
        a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
        num, _, den = (v.get("r_frame_rate") or "0/1").partition("/")
        fps = float(num) / float(den or 1)
        dur = float(d.get("format", {}).get("duration", 0))
        ok = True
        ok &= self.item(f"{rotulo}: tamanho", (v.get("width"), v.get("height")) == (W, H), f"{v.get('width')}x{v.get('height')} (esperado {W}x{H})")
        ok &= self.item(f"{rotulo}: quadros por segundo", abs(fps - FPS) < 0.01, f"{fps:g} (esperado {FPS})")
        ok &= self.item(f"{rotulo}: duração", abs(dur - DUR) <= 0.1, f"{dur:.3f} s (esperado {DUR:g} s)")
        if exige_audio:
            ok &= self.item(f"{rotulo}: áudio", a is not None, a.get("codec_name") if a else "sem trilha de áudio")
        rc, _, err = rodar([self.ffmpeg, "-v", "error", "-i", str(arq), "-f", "null", "-"], self.env)
        ok &= self.item(f"{rotulo}: arquivo íntegro", rc == 0 and not err.strip(), "decodificado inteiro sem erro" if rc == 0 and not err.strip() else err.strip()[-200:])
        return ok

    def colunas(self, arq, x):
        """Média de luminância de uma coluna em cada quadro."""
        rc, out, err = rodar([self.ffmpeg, "-v", "error", "-i", str(arq), "-vf", f"format=gray,crop=1:{H}:{x}:0", "-f", "rawvideo", "-"], self.env, binario=True)
        if rc != 0 or not out:
            return []
        return [sum(out[i:i + H]) / H for i in range(0, len(out) - H + 1, H)]

    # ---------- perfil hyperframes
    def prova_hyperframes(self):
        a = self.dir / "assets"
        hf = self.amb.get("hyperframes") or {}
        gsap = (self.amb.get("gsap") or {}).get("arquivo")
        node = (self.amb.get("node") or {}).get("caminho") or "node"
        if not hf.get("bin") or not Path(hf["bin"]).exists() or not gsap or not Path(gsap).exists():
            return self.item("HyperFrames e GSAP na pasta", False, "não achei; rode o instalador de novo")
        shutil.copyfile(gsap, a / "gsap.min.js")
        if not self.ff(["-f", "lavfi", "-i", f"color=c=0x808080:s={W}x{H}:r={FPS}:d={DUR}", "-f", "lavfi", "-i", f"sine=frequency=440:duration={DUR}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p", "-r", str(FPS),
                        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", "assets/fundo.mp4"], "vídeo de fundo da prova"):
            return False
        (self.dir / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Prova</title>
<script src="assets/gsap.min.js"></script>
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;width:{JANELA}px;height:{H}px;overflow:hidden;background:#000;color:#fff}}
#reel{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
#cam{{position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover}}
#txt{{position:absolute;left:90px;top:880px;width:900px;text-align:center;font:700 110px/160px sans-serif;color:#fff;opacity:0}}
</style></head><body>
<div id="reel" data-composition-id="reel" data-start="0" data-duration="{DUR:g}" data-width="{JANELA}" data-height="{H}">
  <video id="cam" src="assets/fundo.mp4" data-start="0" data-duration="{DUR:g}" data-track-index="0" muted playsinline></video>
  <audio id="voz" src="assets/fundo.mp4" data-start="0" data-duration="{DUR:g}" data-track-index="1" data-volume="1"></audio>
  <div id="txt">PROVA OK</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.set("#txt", {{ opacity: 1 }}, 0.2);
window.__timelines = window.__timelines || {{}};
window.__timelines["reel"] = tl;
</script>
</body></html>
""", encoding="utf-8")
        (self.dir / "meta.json").write_text(json.dumps({"id": "reel", "name": "prova", "width": JANELA, "height": H, "fps": FPS}) + "\n", encoding="utf-8")
        (self.dir / "hyperframes.json").write_text(json.dumps({"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}) + "\n", encoding="utf-8")
        bruto, final = self.dir / "renders" / "bruto.mp4", self.dir / "renders" / "prova-render.mp4"
        bruto.parent.mkdir()
        t = time.time()
        rc, out, err = rodar([node, hf["bin"], "render", ".", "-o", str(bruto), "-q", "draft", "--workers", "auto", "--video-frame-format", "png", "--quiet"],
                             self.env, cwd=self.dir, timeout=900)
        (self.dir / "render.log").write_text(f"{out}\n{err}", encoding="utf-8")
        if not self.item("render do HyperFrames", rc == 0 and bruto.exists(), f"{time.time() - t:.1f} s" if rc == 0 and bruto.exists() else
                         f"saída {rc}; log em {self.dir / 'render.log'}: {(err or out).strip()[-300:]}"):
            return False
        rc, out, _ = rodar([self.ffprobe, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", str(bruto)], self.env)
        largura = int(out.strip() or 0) if rc == 0 else 0
        if not self.item("janela do render", largura >= W, f"{largura} px (esperado {JANELA}, recortado para {W})"):
            return False
        # Mesmos parâmetros do renderizar.mjs das skills, em rascunho.
        if not self.ff(["-i", str(bruto), "-vf", f"crop={W}:{H}:0:0,setsar=1", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
                        "-r", str(FPS), "-c:a", "copy", "-movflags", "+faststart", str(final)], "recorte para 1080"):
            return False
        bruto.unlink()
        self.saida_video = final
        ok = self.conferir_mp4(final, "render")
        dir_, esq = self.colunas(final, W - 1), self.colunas(final, 0)
        if dir_ and esq and len(dir_) == len(esq):
            # O vídeo de fundo é cinza: a primeira coluna mostra se ele apareceu; a última, se há faixa preta.
            pretos = [i for i, e in enumerate(esq) if e < 60]
            ok &= self.item("vídeo de fundo em todo quadro", not pretos,
                            f"{len(esq)} quadros com o fundo visível" if not pretos else f"{len(pretos)} quadros pretos (primeiro: {pretos[0]}); o vídeo não carregou a tempo")
            pior = min(range(len(dir_)), key=lambda i: dir_[i] - esq[i])
            ok &= self.item("borda direita sem faixa preta", all(d >= 0.6 * e for d, e in zip(dir_, esq)),
                            f"pior quadro {pior}: última coluna {dir_[pior]:.1f}, primeira {esq[pior]:.1f} (faixa preta fica perto de 16)")
        else:
            ok &= self.item("borda direita sem faixa preta", False, "não consegui ler as colunas do vídeo")
        rc, quadro, _ = rodar([self.ffmpeg, "-v", "error", "-ss", "1.5", "-i", str(final), "-frames:v", "1", "-vf", "format=gray", "-f", "rawvideo", "-"], self.env, binario=True)
        if rc == 0 and len(quadro) >= W * H:
            regiao = [quadro[y * W + x] for y in range(880, 1040, 2) for x in range(90, 990, 2)]
            claros = sum(1 for p in regiao if p > 200) / len(regiao)
            ok &= self.item("texto apareceu no quadro", claros > 0.02, f"{claros:.1%} de pixels brancos na área do texto (fundo cinza não tem nenhum)")
        else:
            ok &= self.item("texto apareceu no quadro", False, "não consegui extrair o quadro de 1,5 s")
        return ok

    # ---------- perfil ffmpeg
    def prova_ffmpeg(self):
        r = self.dir / "renders"
        r.mkdir()
        if not self.ff(["-f", "lavfi", "-i", f"testsrc2=s=1920x1080:r=60:d={DUR}", "-f", "lavfi", "-i", f"sine=frequency=440:duration={DUR}",
                        "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", "assets/gravacao.mp4"], "gravação de teste"):
            return False
        ok = True
        passos = [
            ("conversão (novo-reel)", "assets/gravacao.mp4", "renders/raw.mp4",
             ["-map", "0:v:0", "-map", "0:a:0", "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-c:v", "libx264", "-preset", "veryfast",
              "-crf", "20", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]),
            ("corte (cortar)", "renders/raw.mp4", "renders/clean.mp4",
             ["-t", f"{DUR:.4f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-g", "30", "-keyint_min", "30", "-pix_fmt", "yuv420p", "-r", str(FPS),
              "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]),
            ("final (renderizar)", "renders/clean.mp4", "renders/prova-render.mp4",
             ["-vf", f"crop={W}:{H}:0:0,setsar=1", "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy",
              "-movflags", "+faststart"]),
        ]
        for nome, ent, sai, params in passos:
            t = time.time()
            if not self.ff(["-i", ent] + params + [sai], nome):
                return False
            self.item(f"codificação {nome}", True, f"{time.time() - t:.1f} s")
            ok &= self.conferir_mp4(self.dir / sai, nome)
        self.saida_video = self.dir / "renders" / "prova-render.mp4"
        return ok

    # ---------- transcrição local
    def prova_transcricao(self):
        w = self.amb.get("whisper") or {}
        py = w.get("caminho")
        if not py or not Path(py).exists():
            return self.item("transcrição local", False, "venv do faster-whisper ausente; rode o instalador de novo")
        wav = self.dir / "assets" / "fala.wav"
        if self.args.audio:
            fonte = Path(self.args.audio).expanduser().resolve()
            if not fonte.exists():
                return self.item("transcrição local", False, f"não achei o áudio {fonte}")
            if not self.ff(["-t", "10", "-i", str(fonte), "-vn", "-ac", "1", "-ar", "16000", str(wav)], "áudio da prova"):
                return False
        elif not self.ff(["-f", "lavfi", "-i", f"sine=frequency=330:duration={DUR}", "-ac", "1", "-ar", "16000", str(wav)], "áudio da prova"):
            return False
        codigo = (
            "import json,sys\n"
            "from faster_whisper import WhisperModel\n"
            "m = WhisperModel(sys.argv[2], device='cpu', compute_type='int8')\n"
            "seg, info = m.transcribe(sys.argv[1], language='pt', word_timestamps=True, vad_filter=False, condition_on_previous_text=False)\n"
            "ws = [{'text': x.word.strip(), 'start': round(x.start, 3), 'end': round(x.end, 3)} for s in seg for x in (s.words or [])]\n"
            "print(json.dumps({'duracao': round(info.duration, 3), 'palavras': ws}, ensure_ascii=False))\n"
        )
        t = time.time()
        rc, out, err = rodar([py, "-c", codigo, str(wav), self.args.modelo], self.env, timeout=1800)
        dt = time.time() - t
        if rc != 0:
            return self.item("transcrição local", False, f"saída {rc}: {err.strip()[-400:]}")
        try:
            r = json.loads(out.strip().splitlines()[-1])
        except Exception:
            return self.item("transcrição local", False, f"saída ilegível: {out.strip()[-200:]}")
        esperado = None if self.args.audio else DUR
        ok = self.item("transcrição: motor carregou e rodou", True, f"modelo {self.args.modelo} em cpu, {dt:.1f} s (a primeira vez inclui o download do modelo)")
        if esperado:
            ok &= self.item("transcrição: duração do áudio", abs(r["duracao"] - esperado) <= 0.2, f"{r['duracao']:.2f} s (esperado {esperado:g} s)")
        pal = r["palavras"]
        coerentes = all(p["end"] >= p["start"] for p in pal)
        if self.args.audio:
            ok &= self.item("transcrição: palavras com tempo", len(pal) >= 1 and coerentes,
                            f"{len(pal)} palavras; começo: {' '.join(p['text'] for p in pal[:8])}" if pal else "nenhuma palavra reconhecida no trecho")
        else:
            self.item("transcrição: fala", True, f"sem --audio, a prova usa um tom (reconheceu {len(pal)} palavras); passe --audio <vídeo do cliente> para provar a fala")
        self.transcricao = {"modelo": self.args.modelo, "segundos": round(dt, 1), "duracao": r["duracao"], "palavras": len(pal), "inicio": [p["text"] for p in pal[:8]]}
        return ok

    def rodar(self):
        print(f"Prova de render, perfil {self.args.perfil}, pasta {self.pasta}")
        t = time.time()
        self.saida_video, self.transcricao = None, None
        ok = self.prova_hyperframes() if self.args.perfil == "hyperframes" else self.prova_ffmpeg()
        if not self.args.sem_transcricao:
            ok &= bool(self.prova_transcricao())
        ok = ok and all(i["ok"] for i in self.itens)
        dt = time.time() - t
        rel = {"perfil": self.args.perfil, "quando": datetime.now().isoformat(timespec="seconds"), "resultado": "OK" if ok else "REPROVADA",
               "segundos": round(dt, 1), "video": str(self.saida_video) if self.saida_video else None, "transcricao": self.transcricao,
               "itens": self.itens}
        (self.pasta / ".ambiente" / "prova-render.json").write_text(json.dumps(rel, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        falhas = [i["item"] for i in self.itens if not i["ok"]]
        print(f"\nPROVA DE RENDER: {'OK' if ok else 'REPROVADA'} ({dt:.0f} s)")
        if self.saida_video:
            print(f"vídeo da prova: {self.saida_video}")
        print(f"registro: {self.pasta / '.ambiente' / 'prova-render.json'}")
        if not ok:
            print(f"Reprovou em: {', '.join(falhas) or 'transcrição'}. Não edite: diga ao dono o que falta e rode o instalador de novo.")
        return 0 if ok else 1


def main():
    global JANELA
    ap = ParserPt(description="Prova curta de que o ambiente renderiza, antes de editar.")
    ap.add_argument("--perfil", required=True, choices=["hyperframes", "ffmpeg"])
    ap.add_argument("--pasta", required=True, help="a mesma pasta de trabalho do instalador")
    ap.add_argument("--audio", help="vídeo ou áudio com fala (de preferência a gravação que vai ser editada)")
    ap.add_argument("--modelo", default="tiny", help="modelo do faster-whisper para a prova (padrão tiny, o mais leve)")
    ap.add_argument("--janela", type=int, default=1096, help=argparse.SUPPRESS)  # contraprova: 1080 deve reprovar a borda
    ap.add_argument("--sem-transcricao", action="store_true", help="pula a transcrição (só quando a transcrição vem pronta de fora)")
    args = ap.parse_args()
    JANELA = args.janela
    sys.exit(Prova(args).rodar())


if __name__ == "__main__":
    main()
