#!/usr/bin/env python3
"""Mosaico de miniaturas numeradas dos slides de uma apresentação.

Uso:
    python3 mosaico.py ARQUIVO.pptx PREFIXO_SAIDA [--colunas 3] [--largura 400] [--limite 180]

Converte a apresentação em PDF pelo LibreOffice (sem janela, perfil isolado),
gera uma imagem por página com o pdftoppm e monta a grade com o Pillow, com o
número de cada slide escrito em cima da miniatura.

Cada imagem leva no máximo 12 slides. Com mais de 12, saem várias imagens:
PREFIXO_SAIDA-1.jpg, PREFIXO_SAIDA-2.jpg e assim por diante. Com até 12, sai
uma só: PREFIXO_SAIDA.jpg.

Slides ocultos aparecem no mosaico como um quadro cinza marcado "oculto", para
a numeração bater com a ordem real da apresentação.

Códigos de saída: 0 gerou, 2 argumento errado, 3 falta programa ou arquivo,
4 o LibreOffice ou o pdftoppm falhou.
"""
import argparse
import math
import os
import posixpath
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

MAX_POR_IMAGEM = 12

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def sair(msg, codigo):
    print(msg, file=sys.stderr)
    sys.exit(codigo)


def rodar(cmd, limite, env=None):
    """Roda um programa externo com limite de tempo, matando o grupo inteiro se estourar."""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=env, start_new_session=True)
    try:
        saida, erro = proc.communicate(timeout=limite)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.communicate()
        return None, "", f"passou do limite de {limite} s"
    return proc.returncode, saida.decode("utf-8", "replace"), erro.decode("utf-8", "replace")


def ordem_dos_slides(caminho):
    """Lê a lista oficial de slides e diz quais estão ocultos. Devolve lista de bool (True = oculto)."""
    try:
        from lxml import etree
    except ImportError:
        return None
    try:
        with zipfile.ZipFile(caminho) as z:
            pres = etree.fromstring(z.read("ppt/presentation.xml"))
            rels = etree.fromstring(z.read("ppt/_rels/presentation.xml.rels"))
            alvos = {}
            for r in rels.findall(f"{{{NS_REL}}}Relationship"):
                alvo = r.get("Target", "")
                if alvo.startswith("/"):
                    alvos[r.get("Id")] = alvo.lstrip("/")
                else:
                    alvos[r.get("Id")] = posixpath.normpath(posixpath.join("ppt", alvo))
            ocultos = []
            for sld in pres.iter(f"{{{NS_P}}}sldId"):
                parte = alvos.get(sld.get(f"{{{NS_R}}}id"))
                oculto = False
                if parte and parte in z.namelist():
                    raiz = etree.fromstring(z.read(parte))
                    oculto = raiz.get("show") in ("0", "false")
                ocultos.append(oculto)
            return ocultos
    except (KeyError, zipfile.BadZipFile, etree.XMLSyntaxError):
        return None


def carregar_fonte(tamanho):
    from PIL import ImageFont
    for nome in ("DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(nome, tamanho)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=tamanho)
    except TypeError:
        return ImageFont.load_default()


def montar(paginas, numeros, ocultos, colunas, largura, destino):
    """Monta uma grade com as miniaturas e grava em destino (JPG)."""
    from PIL import Image, ImageDraw

    imagens = []
    altura_ref = None
    for p in paginas:
        if p is None:
            imagens.append(None)
            continue
        im = Image.open(p).convert("RGB")
        if im.width != largura:
            nova_altura = max(1, round(im.height * largura / im.width))
            im = im.resize((largura, nova_altura), Image.LANCZOS)
        if altura_ref is None:
            altura_ref = im.height
        imagens.append(im)
    if altura_ref is None:
        altura_ref = round(largura * 9 / 16)

    faixa = max(28, largura // 9)
    margem = max(10, largura // 30)
    fonte = carregar_fonte(int(faixa * 0.7))
    linhas = math.ceil(len(imagens) / colunas)
    cols_usadas = min(colunas, len(imagens))
    alt_celula = faixa + altura_ref
    tela = Image.new("RGB", (margem + cols_usadas * (largura + margem),
                             margem + linhas * (alt_celula + margem)), (235, 235, 235))
    d = ImageDraw.Draw(tela)
    for i, im in enumerate(imagens):
        lin, col = divmod(i, colunas)
        x = margem + col * (largura + margem)
        y = margem + lin * (alt_celula + margem)
        d.rectangle([x, y, x + largura - 1, y + faixa - 1], fill=(30, 30, 30))
        rotulo = f"{numeros[i]}"
        if ocultos[i]:
            rotulo += "  (oculto)"
        d.text((x + faixa // 4, y + faixa // 2), rotulo, fill=(255, 255, 255), font=fonte, anchor="lm")
        if im is None:
            d.rectangle([x, y + faixa, x + largura - 1, y + faixa + altura_ref - 1], fill=(190, 190, 190))
            d.text((x + largura // 2, y + faixa + altura_ref // 2), "oculto", fill=(90, 90, 90),
                   font=fonte, anchor="mm")
        else:
            tela.paste(im.crop((0, 0, largura, min(im.height, altura_ref))), (x, y + faixa))
        d.rectangle([x, y, x + largura - 1, y + alt_celula - 1], outline=(120, 120, 120))
    tela.save(destino, "JPEG", quality=88)


def main():
    ap = argparse.ArgumentParser(
        description="Gera o mosaico de miniaturas numeradas dos slides (LibreOffice, pdftoppm, Pillow).")
    ap.add_argument("arquivo", help="apresentação .pptx (ou .ppt, .odp)")
    ap.add_argument("prefixo", help="prefixo dos JPG de saída, por exemplo saida/deck-mosaico")
    ap.add_argument("--colunas", type=int, default=3, help="colunas da grade (padrão 3)")
    ap.add_argument("--largura", type=int, default=400, help="largura de cada miniatura em pixels (padrão 400)")
    ap.add_argument("--limite", type=int, default=180,
                    help="segundos máximos para o LibreOffice converter (padrão 180)")
    a = ap.parse_args()

    if a.colunas < 1 or a.colunas > MAX_POR_IMAGEM:
        sair(f"--colunas precisa ficar entre 1 e {MAX_POR_IMAGEM}.", 2)
    if a.largura < 80 or a.largura > 2000:
        sair("--largura precisa ficar entre 80 e 2000 pixels.", 2)
    if a.limite < 1:
        sair("--limite precisa ser positivo.", 2)

    origem = Path(a.arquivo)
    if not origem.is_file():
        sair(f"Arquivo não encontrado: {origem}", 3)
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        sair("Falta o LibreOffice (comando soffice). Instale o pacote libreoffice-impress.", 3)
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        sair("Falta o pdftoppm. Instale o pacote poppler-utils.", 3)
    try:
        import PIL  # noqa: F401
    except ImportError:
        sair("Falta a biblioteca Pillow. Instale com: pip install Pillow", 3)

    with tempfile.TemporaryDirectory(prefix="mosaico-") as tmp:
        tmp = Path(tmp)
        perfil = tmp / "perfil"
        entrada = tmp / ("entrada" + origem.suffix.lower())
        shutil.copyfile(origem, entrada)
        env = dict(os.environ, HOME=str(tmp), SAL_USE_VCLPLUGIN="svp")
        cmd = [soffice, f"-env:UserInstallation={perfil.as_uri()}", "--headless", "--norestore",
               "--nologo", "--nodefault", "--nolockcheck",
               "--convert-to", "pdf", "--outdir", str(tmp), str(entrada)]
        cod, out, err = rodar(cmd, a.limite, env)
        pdf = tmp / "entrada.pdf"
        if cod is None:
            sair(f"O LibreOffice não terminou a conversão para PDF: {err}.", 4)
        if cod != 0 or not pdf.is_file():
            sair(f"O LibreOffice falhou ao converter para PDF (código {cod}). {err.strip()[:400]}", 4)

        cod, out, err = rodar([pdftoppm, "-jpeg", "-jpegopt", "quality=90",
                               "-scale-to-x", str(a.largura), "-scale-to-y", "-1",
                               str(pdf), str(tmp / "pag")], a.limite)
        if cod != 0:
            sair(f"O pdftoppm falhou (código {cod}). {err.strip()[:400]}", 4)
        paginas = sorted(tmp.glob("pag-*.jpg"), key=lambda p: int(re.search(r"(\d+)$", p.stem).group(1)))
        if not paginas:
            sair("O PDF gerado não tem páginas. A apresentação está vazia?", 4)

        # Casa páginas com slides: o PDF do LibreOffice deixa de fora os slides ocultos.
        ocultos = ordem_dos_slides(origem) if origem.suffix.lower() == ".pptx" else None
        aviso = None
        if ocultos and len(ocultos) == len(paginas):
            itens = [(p, i + 1, ocultos[i]) for i, p in enumerate(paginas)]
        elif ocultos and len(paginas) == ocultos.count(False):
            fila = iter(paginas)
            itens = [(None if oc else next(fila), i + 1, oc) for i, oc in enumerate(ocultos)]
        else:
            if ocultos is not None:
                aviso = (f"Aviso: o PDF tem {len(paginas)} páginas e a apresentação lista {len(ocultos)} slides; "
                         "a numeração segue as páginas do PDF.")
            itens = [(p, i + 1, False) for i, p in enumerate(paginas)]

        prefixo = Path(a.prefixo)
        if prefixo.suffix.lower() in (".jpg", ".jpeg"):
            prefixo = prefixo.with_suffix("")
        prefixo.parent.mkdir(parents=True, exist_ok=True)
        grupos = [itens[i:i + MAX_POR_IMAGEM] for i in range(0, len(itens), MAX_POR_IMAGEM)]
        gerados = []
        for n, grupo in enumerate(grupos, 1):
            destino = Path(f"{prefixo}.jpg") if len(grupos) == 1 else Path(f"{prefixo}-{n}.jpg")
            montar([g[0] for g in grupo], [g[1] for g in grupo], [g[2] for g in grupo],
                   a.colunas, a.largura, destino)
            gerados.append((destino, grupo[0][1], grupo[-1][1]))

    if aviso:
        print(aviso)
    total = len(itens)
    print(f"{total} slides em {len(gerados)} imagem(ns):")
    for destino, ini, fim in gerados:
        print(f"  {destino}  (slides {ini} a {fim})")
    if len(gerados) > 1:
        print(f"Dica: cada imagem leva no máximo {MAX_POR_IMAGEM} slides; abra todas para ver o deck inteiro.")
    n_ocultos = sum(1 for g in itens if g[2])
    if n_ocultos:
        print(f"{n_ocultos} slide(s) oculto(s), marcados 'oculto' no mosaico.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
