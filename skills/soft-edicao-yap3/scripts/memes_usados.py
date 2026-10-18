#!/usr/bin/env python3
"""Memes já usados na série: lê a semente da skill e o registro do dono, e grava os novos fora da skill.

A semente `assets/memes-usados.json` vem com a skill e é só leitura: a pasta da skill pode ser
trocada inteira a cada versão, então nada é gravado nela. O registro do dono é um arquivo de dados:
  1. YAP_MEMES_USADOS, se definida (caminho do arquivo);
  2. senão $LEON_DATA_DIR/soft-edicao-yap3/memes-usados.json;
  3. senão ~/.leon/dados/soft-edicao-yap3/memes-usados.json.

Uso:
  python3 memes_usados.py ver [--json]
      lista os memes usados (semente e registro juntos) e diz onde está o registro
  python3 memes_usados.py somar <episodio> <plano-gif.json> [<plano-gif.json> ...]
      depois da entrega, grava no registro os memes dos planos (termo, palavra, página e som)

Saídas: 0 pronto, 1 dado ilegível ou plano sem meme, 2 argumento errado ou registro dentro da skill.
"""
import json, os, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SEMENTE = SKILL / "assets" / "memes-usados.json"
CAMPOS = ("palavra", "termo", "pagina", "som")
REGRA = ("memes nunca repetem os de episódio anterior da série. Este é o registro do dono, fora da skill; "
         "a semente da skill (assets/memes-usados.json) é só leitura.")


def caminho_registro():
    if os.environ.get("YAP_MEMES_USADOS"):
        return Path(os.environ["YAP_MEMES_USADOS"]).expanduser()
    base = Path(os.environ["LEON_DATA_DIR"]).expanduser() if os.environ.get("LEON_DATA_DIR") else Path.home() / ".leon" / "dados"
    return base / "soft-edicao-yap3" / "memes-usados.json"


def ler(caminho):
    if not caminho.exists():
        return {}
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        return dados.get("episodios", {}) if isinstance(dados, dict) else {}
    except (OSError, ValueError) as e:
        print(f"ERRO: {caminho} ilegível ({e}); conserte ou apague o arquivo e rode de novo", file=sys.stderr)
        sys.exit(1)


def chave(m):
    return (m.get("pagina") or "").strip().lower() or (m.get("termo") or "").strip().lower()


def ver(como_json):
    reg = caminho_registro()
    semente, registro = ler(SEMENTE), ler(reg)
    if como_json:
        print(json.dumps({"registro": str(reg), "semente": semente, "registro_do_dono": registro}, ensure_ascii=False, indent=1))
        return 0
    print(f"registro do dono: {reg} ({'existe' if reg.exists() else 'ainda não existe; o primeiro somar cria'})")
    print(f"semente da skill (só leitura): {SEMENTE.relative_to(SKILL)}")
    total = 0
    for origem, eps in (("semente", semente), ("registro", registro)):
        for ep, memes in eps.items():
            for m in memes:
                total += 1
                print(f"  {ep} ({origem}): {m.get('palavra', '?')} -> {m.get('termo', '?')} | {m.get('pagina', '?')} | som {m.get('som', '?')}")
    print(f"{total} memes já usados. Não repita termo nem página de episódio anterior.")
    return 0


def somar(ep, planos):
    reg = caminho_registro()
    try:
        reg.resolve().relative_to(SKILL)
        print(f"ERRO: o registro {reg} fica dentro da pasta da skill, que é trocada a cada versão. "
              "Aponte YAP_MEMES_USADOS para um arquivo fora dela.", file=sys.stderr)
        return 2
    except ValueError:
        pass
    novos = []
    for p in planos:
        try:
            momentos = json.loads(Path(p).read_text(encoding="utf-8")).get("momentos", [])
        except (OSError, ValueError, AttributeError) as e:
            print(f"ERRO: plano ilegível {p} ({e})", file=sys.stderr)
            return 1
        for m in momentos:
            item = {k: m[k] for k in CAMPOS if m.get(k)}
            if chave(item) and chave(item) not in {chave(x) for x in novos}:
                novos.append(item)
    if not novos:
        print("ERRO: nenhum meme com termo ou página nos planos dados", file=sys.stderr)
        return 1
    semente, registro = ler(SEMENTE), ler(reg)
    for origem, eps in (("semente", semente), ("registro", registro)):
        for outro, memes in eps.items():
            if outro == ep:
                continue
            for x in memes:
                for m in novos:
                    if chave(x) == chave(m):
                        print(f"aviso: {m.get('termo') or m.get('pagina')} já tinha sido usado em {outro} ({origem})")
    atual = registro.get(ep, [])
    vistos = {chave(x) for x in atual}
    atual += [m for m in novos if chave(m) not in vistos]
    registro[ep] = atual
    try:
        reg.parent.mkdir(parents=True, exist_ok=True)
        tmp = reg.with_name(reg.name + ".parcial")
        tmp.write_text(json.dumps({"regra": REGRA, "episodios": registro}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        tmp.replace(reg)
    except OSError as e:
        print(f"ERRO: não consegui gravar o registro em {reg} ({e}). Aponte YAP_MEMES_USADOS para um arquivo "
              "numa pasta em que você grava, fora da skill, e rode de novo.", file=sys.stderr)
        return 1
    print(f"{ep}: {len(atual)} memes no registro {reg}")
    return 0


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    if argv[0] == "ver" and set(argv[1:]) <= {"--json"}:
        return ver("--json" in argv[1:])
    if argv[0] == "somar" and len(argv) >= 3:
        return somar(argv[1], argv[2:])
    print(f"argumento errado: {' '.join(argv)}\n{__doc__}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
