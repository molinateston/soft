#!/usr/bin/env python3
"""lint_binario.py: roda o anti-IA (lint_copy.py) sobre o TEXTO EXTRAIDO
de cada binario gerado, nunca sobre o .md como procuracao.

Motivo de existir: o .md de origem pode estar limpo e o binario que o dono
abre carregar sujeira injetada na conversao (travessao longo digitado dentro
do script gerador e o caso classico). Quem le o .md conclui por analogia;
quem extrai o texto do binario mede.

Rotas de extracao, por formato:
  .docx / .pptx  -> zip interno (word/document.xml, ppt/slides/*.xml),
                    tags removidas; sem dependencia externa.
  .pdf           -> pdftotext, quando existir na maquina.
  .md / .txt     -> lido direto.

Uso:
  python3 scripts/lint_binario.py <arquivo> [<arquivo> ...]

Saida: uma linha por arquivo, na forma exigida pelo gate,
  <arquivo> (texto extraido): exit N
e no fim o total. Exit 1 se qualquer arquivo reprovar ou nao puder ser lido.
"""
import re
import subprocess
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LINT = AQUI / "lint_copy.py"

TAG = re.compile(r"<[^>]+>")
QUEBRA = re.compile(r"</w:p>|</a:p>|<w:br\b[^>]*/?>|<a:br\b[^>]*/?>")


def _do_xml(bruto: str) -> str:
    """XML do Office vira texto: paragrafo fecha linha, o resto perde a tag."""
    texto = QUEBRA.sub("\n", bruto)
    texto = TAG.sub("", texto)
    for ent, char in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                      ("&quot;", '"'), ("&apos;", "'")):
        texto = texto.replace(ent, char)
    return texto


def extrair(caminho: Path) -> str:
    ext = caminho.suffix.lower()
    if ext in (".md", ".txt"):
        return caminho.read_text(encoding="utf-8", errors="replace")
    if ext in (".docx", ".pptx", ".xlsx"):
        partes = []
        with zipfile.ZipFile(caminho) as z:
            nomes = z.namelist()
            alvos = [n for n in nomes if n == "word/document.xml"]
            alvos += sorted(n for n in nomes
                            if n.startswith("ppt/slides/slide") and n.endswith(".xml"))
            alvos += sorted(n for n in nomes
                            if n.startswith("ppt/notesSlides/") and n.endswith(".xml"))
            alvos += [n for n in nomes if n == "xl/sharedStrings.xml"]
            if not alvos:
                raise ValueError(f"nenhuma parte de texto encontrada em {caminho.name}")
            for nome in alvos:
                partes.append(_do_xml(z.read(nome).decode("utf-8", errors="replace")))
        return "\n".join(partes)
    if ext == ".pdf":
        try:
            saida = subprocess.run(["pdftotext", str(caminho), "-"],
                                   capture_output=True, check=True)
        except FileNotFoundError:
            raise ValueError("pdftotext ausente na maquina; instale poppler-utils "
                             "ou declare a rota no relatorio")
        return saida.stdout.decode("utf-8", errors="replace")
    raise ValueError(f"formato sem rota de extracao: {ext}")


def main() -> int:
    alvos = [Path(a) for a in sys.argv[1:]]
    if not alvos:
        print(__doc__)
        return 2
    linhas, ok = [], 0
    for alvo in alvos:
        if not alvo.exists():
            linhas.append(f"{alvo.name} (texto extraido): exit 2 (arquivo ausente)")
            continue
        try:
            texto = extrair(alvo)
        except Exception as erro:  # noqa: BLE001
            linhas.append(f"{alvo.name} (texto extraido): exit 2 ({erro})")
            continue
        tmp = alvo.with_suffix(alvo.suffix + ".extraido.txt")
        tmp.write_text(texto, encoding="utf-8")
        try:
            res = subprocess.run([sys.executable, str(LINT), str(tmp)],
                                 capture_output=True)
            código = res.returncode
            linhas.append(f"{alvo.name} (texto extraido): exit {código}")
            if código != 0:
                sys.stdout.write(res.stdout.decode("utf-8", errors="replace"))
            else:
                ok += 1
        finally:
            tmp.unlink(missing_ok=True)
    for linha in linhas:
        print(linha)
    print(f"binarios linteados: {len(linhas)} · exit 0: {ok} · "
          f"exit diferente de 0: {len(linhas) - ok}")
    return 0 if ok == len(linhas) else 1


if __name__ == "__main__":
    sys.exit(main())
