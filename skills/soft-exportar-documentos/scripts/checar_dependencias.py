#!/usr/bin/env python3
"""
checar_dependencias.py - diz o que esta maquina consegue exportar HOJE.

Roda antes de qualquer conversao. Ele nao instala nada e nao muda nada: so
olha o que existe e imprime, por formato, a rota que da pra usar e a que nao
da. Quando nenhuma rota de um formato existe, a saida diz a frase que a skill
tem que devolver ao dono (entregar o .md e explicar o que faltou).

USO:
    python3 scripts/checar_dependencias.py            # tabela legivel
    python3 scripts/checar_dependencias.py --json     # saida pra script
    python3 scripts/checar_dependencias.py --formato docx

Sai 0 sempre que consegue medir; a falta de biblioteca nao e erro do script, e
informacao. Sai 1 so quando pedem um formato que nao existe na tabela.
"""

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys

# ---------------------------------------------------------------- deteccao


def tem_binario(nome):
    return shutil.which(nome) is not None


def tem_modulo_py(nome):
    try:
        return importlib.util.find_spec(nome) is not None
    except (ImportError, ValueError):
        return False


def tem_modulo_node(nome):
    if not tem_binario("node"):
        return False
    try:
        r = subprocess.run(
            ["node", "-e", f"require.resolve({json.dumps(nome)})"],
            capture_output=True, timeout=20,
        )
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# ---------------------------------------------------------------- rotas
# Cada rota: (nome, o que precisa, o que ela faz bem). A ordem e a preferencia:
# a primeira rota disponivel da lista e a que a skill usa.

ROTAS = {
    "docx": [
        ("docx-js", [("node", "node"), ("npm:docx", "docx")],
         "cria Word do zero com controle fino de estilo, tabela e sumario"),
        ("python-docx", [("py", "docx")],
         "cria e edita Word em Python, bom pra texto, tabela e imagem simples"),
        ("pandoc", [("bin", "pandoc")],
         "converte markdown em Word direto, sem controle fino de estilo"),
        ("xml-na-mao", [("bin", "unzip"), ("bin", "zip")],
         "descompacta, edita word/document.xml e recompacta; ultima rota"),
    ],
    "pptx": [
        ("pptxgenjs", [("node", "node"), ("npm:pptxgenjs", "pptxgenjs")],
         "cria deck do zero com grafico nativo, imagem e nota do apresentador"),
        ("python-pptx", [("py", "pptx")],
         "cria e edita deck em Python; nao duplica slide nem le SVG de template"),
        ("xml-na-mao", [("bin", "unzip"), ("bin", "zip")],
         "edita ppt/slides/slideN.xml de um template; ultima rota"),
    ],
    "xlsx": [
        ("openpyxl", [("py", "openpyxl")],
         "cria e edita planilha com formula viva, formato de celula e grafico"),
        ("pandas", [("py", "pandas")],
         "despeja tabela grande rapido; nao escreve formula nem formatacao"),
        ("csv", [],
         "sempre disponivel; entrega .csv em vez de .xlsx, sem formula"),
    ],
    "pdf": [
        ("libreoffice", [("bin", "soffice")],
         "converte docx, pptx, xlsx ou html em PDF fiel ao original"),
        ("reportlab", [("py", "reportlab")],
         "monta PDF do zero em Python, com controle de pagina e fonte"),
        ("pypdf", [("py", "pypdf")],
         "junta, separa, gira, marca dagua e protege PDF que ja existe"),
        ("pandoc", [("bin", "pandoc")],
         "markdown em PDF; precisa de um motor de LaTeX instalado junto"),
    ],
}

# Ferramentas de apoio: nao sao rota de saida, sao conferencia.
APOIO = {
    "soffice": ("bin", "soffice", "renderiza o arquivo pra conferir com o olho, e converte formato"),
    "pdftoppm": ("bin", "pdftoppm", "vira o PDF em imagem por pagina pra conferencia visual"),
    "pdftotext": ("bin", "pdftotext", "puxa o texto de um PDF pra conferir conteudo"),
    "pandoc": ("bin", "pandoc", "le .docx e devolve markdown, pra conferir o que entrou"),
    "markitdown": ("bin", "markitdown", "le .pptx e .xlsx e devolve markdown, pra conferir o que entrou"),
    "qpdf": ("bin", "qpdf", "junta, separa e gira PDF pela linha de comando"),
    "pdfplumber": ("py", "pdfplumber", "extrai texto e tabela de PDF com layout preservado"),
    "lxml": ("py", "lxml", "valida o XML do arquivo Office contra o esquema"),
    "defusedxml": ("py", "defusedxml", "le XML de terceiro sem risco; exigido pelos scripts de validacao"),
    "PIL": ("py", "PIL", "monta o mosaico de miniaturas do deck"),
}


def disponivel(tipo, alvo):
    if tipo == "bin":
        return tem_binario(alvo)
    if tipo == "py":
        return tem_modulo_py(alvo)
    if tipo == "node":
        return tem_binario(alvo)
    if tipo.startswith("npm:"):
        return tem_modulo_node(alvo)
    return False


def medir(formato):
    saida = []
    for nome, requisitos, faz in ROTAS[formato]:
        faltando = [alvo for tipo, alvo in requisitos if not disponivel(tipo, alvo)]
        saida.append({
            "rota": nome,
            "disponivel": not faltando,
            "faltando": faltando,
            "faz": faz,
        })
    return saida


def medir_apoio():
    return {
        nome: {"disponivel": disponivel(tipo, alvo), "faz": faz}
        for nome, (tipo, alvo, faz) in APOIO.items()
    }


FRASE_SEM_ROTA = (
    "Sem biblioteca nenhuma pra {formato} nesta maquina. Entregue o conteudo em .md "
    "e diga ao dono, em uma linha: falta {faltou} pra gerar o {formato}; o texto esta "
    "pronto e a conversao roda assim que a biblioteca existir."
)


def relatorio(formatos):
    resultado = {"formatos": {}, "apoio": medir_apoio()}
    for f in formatos:
        rotas = medir(f)
        escolhida = next((r["rota"] for r in rotas if r["disponivel"]), None)
        faltou = ", ".join(sorted({x for r in rotas for x in r["faltando"]}))
        resultado["formatos"][f] = {
            "rotas": rotas,
            "rota_escolhida": escolhida,
            "recado": None if escolhida else FRASE_SEM_ROTA.format(formato=f, faltou=faltou),
        }
    return resultado


def imprimir(resultado):
    for formato, dados in resultado["formatos"].items():
        print(f"== {formato.upper()} ==")
        for r in dados["rotas"]:
            marca = "OK  " if r["disponivel"] else "nao "
            falta = f"  (falta: {', '.join(r['faltando'])})" if r["faltando"] else ""
            print(f"  [{marca}] {r['rota']:14} {r['faz']}{falta}")
        if dados["rota_escolhida"]:
            print(f"  -> use a rota: {dados['rota_escolhida']}")
        else:
            print(f"  -> SEM ROTA. {dados['recado']}")
        print()
    print("== APOIO (conferencia, nao e rota de saida) ==")
    for nome, d in resultado["apoio"].items():
        print(f"  [{'OK  ' if d['disponivel'] else 'nao '}] {nome:12} {d['faz']}")


def main():
    p = argparse.ArgumentParser(description="Mede o que esta maquina consegue exportar.")
    p.add_argument("--formato", choices=sorted(ROTAS), help="mede so um formato")
    p.add_argument("--json", action="store_true", help="saida em JSON")
    args = p.parse_args()

    formatos = [args.formato] if args.formato else sorted(ROTAS)
    resultado = relatorio(formatos)
    if args.json:
        json.dump(resultado, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        imprimir(resultado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
