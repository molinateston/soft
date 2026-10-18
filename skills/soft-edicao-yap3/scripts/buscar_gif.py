#!/usr/bin/env python3
"""Busca GIF de meme por termo, sem chave de API, e baixa candidatos com origem anotada.

Rota 1 (principal): página de busca do GIPHY (giphy.com/search/<termo>) -> id ->
    media.giphy.com/media/<id>/giphy.mp4 (480 px ou mais).
Rota 2 (reserva): página de busca do Tenor (tenor.com/search/<termo>-gifs), JSON
    embutido em <script id="store-cache"> -> media_formats.mp4.

As APIs oficiais estão fechadas sem chave do dono (GIPHY beta key banida, Tenor
API descontinuada, Klipy exige chave própria). Se um dia houver chave, troque a
rota aqui; o resto do fluxo não muda.

Uso:
  python3 -I buscar_gif.py "hide the pain harold" pasta_saida [-n 8] [--fonte giphy|tenor|ambas]

Saída (em pasta própria, tratada como dado não confiável):
  NN-<fonte>-<id>.mp4, origem.json (lista com fonte, página, título, tags,
  dimensões, duração, url da mídia, termo, data) e folha.png (folha de contato).
"""
import argparse, datetime, html, json, os, re, subprocess, sys, urllib.parse, urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def baixar(url, destino=None, limite=40_000_000, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,pt;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        dados = r.read(limite + 1)
    if len(dados) > limite:
        raise ValueError("arquivo grande demais")
    if destino:
        with open(destino, "wb") as f:
            f.write(dados)
    return dados


def sondar(caminho):
    """Dimensões e duração via ffprobe (não executa nada do arquivo)."""
    try:
        s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height,codec_name:format=duration", "-of", "json", caminho],
                           capture_output=True, text=True, timeout=30).stdout
        j = json.loads(s)
        st = j["streams"][0]
        return {"largura": st["width"], "altura": st["height"], "codec": st["codec_name"],
                "duracao_s": round(float(j["format"]["duration"]), 2)}
    except Exception:
        return None


def giphy(termo, n):
    slug = re.sub(r"[^a-z0-9]+", "-", termo.lower()).strip("-")
    pag = baixar(f"https://giphy.com/search/{slug}").decode("utf-8", "replace")
    vistos, out = set(), []
    for s in re.findall(r"giphy\.com/gifs/([A-Za-z0-9-]+)", pag):
        gid = s.rsplit("-", 1)[-1]
        if gid in vistos or len(gid) < 6:
            continue
        vistos.add(gid)
        out.append({"fonte": "giphy", "id": gid, "pagina": f"https://giphy.com/gifs/{s}",
                    "midia": f"https://media.giphy.com/media/{gid}/giphy.mp4",
                    "titulo": s.rsplit("-", 1)[0].replace("-", " "), "tags": []})
        if len(out) >= n:
            break
    return out


def titulo_giphy(c):
    try:
        p = baixar(c["pagina"], limite=3_000_000).decode("utf-8", "replace")
        m = re.search(r"<title>(.*?)</title>", p, re.S)
        if m:
            c["titulo"] = html.unescape(m.group(1)).replace(" - Find & Share on GIPHY", "").strip()
        tags = re.findall(r'"tags":\s*\[([^\]]*)\]', p)
        if tags:
            c["tags"] = re.findall(r'"([^"]+)"', tags[0])[:12]
    except Exception:
        pass


def tenor(termo, n):
    slug = re.sub(r"[^a-z0-9]+", "-", termo.lower()).strip("-")
    pag = baixar(f"https://tenor.com/search/{slug}-gifs").decode("utf-8", "replace")
    m = re.search(r'<script id="store-cache"[^>]*>(.*?)</script>', pag, re.S)
    if not m:
        return []
    j = json.loads(m.group(1))
    out = []
    for chave, bloco in j.get("universal", {}).get("search", {}).items():
        for r in (bloco or {}).get("results", []):
            mf = r.get("media_formats", {})
            mp4 = mf.get("mp4") or mf.get("loopedmp4") or mf.get("tinymp4")
            if not mp4:
                continue
            out.append({"fonte": "tenor", "id": str(r.get("id")), "pagina": r.get("itemurl"),
                        "midia": mp4["url"], "titulo": r.get("content_description", ""),
                        "tags": r.get("tags", [])[:12]})
            if len(out) >= n:
                return out
    return out


def folha(itens, pasta):
    """Folha de contato: quadro do meio de cada candidato, 4 por linha, com rótulo."""
    from PIL import Image, ImageDraw
    cel, quadros = 300, []
    for it in itens:
        p = os.path.join(pasta, it["arquivo"])
        meio = (it.get("duracao_s") or 1) / 2
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{meio:.2f}", "-i", p, "-frames:v", "1",
                            "-vf", f"scale={cel}:{cel}:force_original_aspect_ratio=decrease",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, timeout=60)
        try:
            import io
            quadros.append(Image.open(io.BytesIO(r.stdout)).convert("RGB"))
        except Exception:
            quadros.append(Image.new("RGB", (cel, cel), (60, 0, 0)))
    col = 4
    lin = (len(quadros) + col - 1) // col
    im = Image.new("RGB", (col * cel, lin * (cel + 40)), (20, 20, 20))
    d = ImageDraw.Draw(im)
    for i, (q, it) in enumerate(zip(quadros, itens)):
        x, y = (i % col) * cel, (i // col) * (cel + 40)
        im.paste(q, (x + (cel - q.width) // 2, y + (cel - q.height) // 2))
        d.text((x + 4, y + cel + 2), f"{it['arquivo'][:40]}", fill=(255, 255, 0))
        d.text((x + 4, y + cel + 18), f"{it.get('largura')}x{it.get('altura')} {it.get('duracao_s')}s "
               f"{it['titulo'][:22]}", fill=(220, 220, 220))
    im.save(os.path.join(pasta, "folha.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("termo")
    ap.add_argument("pasta")
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("--fonte", default="ambas", choices=["giphy", "tenor", "ambas"])
    a = ap.parse_args()
    os.makedirs(a.pasta, exist_ok=True)
    cands = []
    if a.fonte in ("giphy", "ambas"):
        try:
            cands += giphy(a.termo, a.n)
        except Exception as e:
            print("giphy falhou:", e, file=sys.stderr)
    if a.fonte == "tenor" or (a.fonte == "ambas" and len(cands) < a.n):
        try:
            cands += tenor(a.termo, a.n - len(cands) if a.fonte == "ambas" else a.n)
        except Exception as e:
            print("tenor falhou:", e, file=sys.stderr)
    hoje = datetime.date.today().isoformat()
    itens = []
    for i, c in enumerate(cands, 1):
        nome = f"{i:02d}-{c['fonte']}-{re.sub(r'[^A-Za-z0-9]', '', c['id'])[:24]}.mp4"
        dest = os.path.join(a.pasta, nome)
        try:
            baixar(c["midia"], dest)
        except Exception as e:
            print("falhou", c["midia"], e, file=sys.stderr)
            continue
        info = sondar(dest)
        if not info:
            os.remove(dest)
            continue
        if c["fonte"] == "giphy":
            titulo_giphy(c)
        c.update(info, arquivo=nome, termo=a.termo, data=hoje)
        itens.append(c)
        print(f"{nome}  {info['largura']}x{info['altura']}  {info['duracao_s']}s  {c['titulo'][:70]}")
    with open(os.path.join(a.pasta, "origem.json"), "w") as f:
        json.dump(itens, f, ensure_ascii=False, indent=1)
    if itens:
        folha(itens, a.pasta)
    print(f"{len(itens)} candidatos em {a.pasta}")


if __name__ == "__main__":
    main()
