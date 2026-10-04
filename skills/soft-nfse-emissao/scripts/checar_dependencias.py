#!/usr/bin/env python3
"""
checar_dependencias.py - diz o que esta máquina tem para emitir NFS-e.

Não instala nada e não muda nada: mede e imprime o comando de instalação do que
faltar. Quem decide instalar é o dono.

Saída 0: dá pra preparar, assinar e enviar (o PDF pode faltar; o XML é o
documento fiscal). Saída 1: falta algo obrigatório.
"""
import importlib.util
import shutil
import sys

OBRIGATORIOS = [
    ("lxml", "lxml", "montar, assinar e ler o XML"),
    ("cryptography", "cryptography", "abrir o .pfx e assinar"),
]
DO_PDF = [
    ("fpdf", "fpdf2", "gerar o PDF de representação"),
    ("qrcode", "qrcode", "QR da consulta pública"),
    ("PIL", "pillow", "imagem do QR"),
]
SO_AUTOTESTE = [
    ("bin", "pdftotext", "poppler-utils", "conferir o texto do PDF"),
    ("bin", "pdftoppm", "poppler-utils", "renderizar o PDF para ler o QR"),
    ("bin", "openssl", "openssl", "conferir a RSA por mais um caminho"),
    ("bin", "xmlsec1", "xmlsec1", "conferir a assinatura por mais um caminho"),
    ("py", "xmlsec", "xmlsec", "conferir a assinatura com a libxmlsec1"),
    ("py", "cv2", "opencv-python-headless", "ler o QR do PDF renderizado"),
]


def tem_modulo(nome):
    try:
        return importlib.util.find_spec(nome) is not None
    except (ImportError, ValueError):
        return False


def versao_fpdf_ok():
    try:
        import fpdf
        partes = [int(x) for x in fpdf.__version__.split(".")[:3]]
        return partes >= [2, 5, 2], fpdf.__version__
    except Exception:
        return False, "?"


def main():
    faltam, faltam_pdf = [], []
    print(f"python {sys.version.split()[0]}: " + ("ok" if sys.version_info >= (3, 9)
                                                  else "precisa de 3.9 ou mais novo"))
    if sys.version_info < (3, 9):
        faltam.append("python3 3.9+")
    print("\nObrigatório para emitir:")
    for mod, pacote, uso in OBRIGATORIOS:
        ok = tem_modulo(mod)
        print(f"  {'ok   ' if ok else 'FALTA'} {pacote:<14} {uso}")
        if not ok:
            faltam.append(pacote)
    print("\nPara o PDF (sem eles a nota sai, só o PDF fica para depois):")
    for mod, pacote, uso in DO_PDF:
        ok = tem_modulo(mod)
        if ok and mod == "fpdf":
            ok, v = versao_fpdf_ok()
            uso = f"{uso} (versão {v}, precisa 2.5.2 ou mais)"
        print(f"  {'ok   ' if ok else 'FALTA'} {pacote:<14} {uso}")
        if not ok:
            faltam_pdf.append(pacote)
    print("\nSó para o autoteste (opcionais, ampliam a conferência):")
    for tipo, nome, pacote, uso in SO_AUTOTESTE:
        ok = shutil.which(nome) is not None if tipo == "bin" else tem_modulo(nome)
        print(f"  {'ok   ' if ok else '-    '} {nome:<14} {uso} (pacote {pacote})")
    print()
    if faltam:
        print("Falta o obrigatório. Comando de instalação (rode você, a skill não instala):")
        print(f"  python3 -m pip install --user {' '.join(p for p in faltam if ' ' not in p)}")
    if faltam_pdf:
        print("Para o PDF:")
        print(f"  python3 -m pip install --user {' '.join(faltam_pdf)}")
    if faltam or faltam_pdf:
        print("Em Python gerenciado pelo sistema, crie um ambiente virtual numa pasta fora da "
              "skill (python3 -m venv <pasta>) e instale com o pip dele.")
    else:
        print("Tudo o que a emissão e o PDF usam está instalado.")
    return 1 if faltam else 0


if __name__ == "__main__":
    sys.exit(main())
