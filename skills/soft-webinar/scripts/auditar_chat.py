#!/usr/bin/env python3
"""auditar_chat.py: mede o CSV do chat simulado e imprime o bloco de auditoria pronto.

Existe porque o olho nao pega rodizio. Um chat montado como lista circular
(os mesmos 10 nomes, na mesma ordem, bloco apos bloco) parece natural na
leitura e denuncia o gravado na tela do lead. As tres contagens que pegam
isso (nomes com 3+ falas, intervalo fixo, trincas repetidas) foram declaradas
zero, de cabeca, num arquivo que tinha 9 e 13. Este script tira a contagem
da memoria e coloca no disco.

Uso:
    python3 scripts/auditar_chat.py <chat.csv> [opcoes]

Opcoes:
    --link MM:SS       timestamp de video em que o link entra no ar
                       (minuto da oferta no roteiro + offset da sala de espera)
    --teto MM:SS       teto de duracao em tempo de video (duracao + offset)
    --offset MM:SS     fim da sala de espera (default 5:00), para contar entradas
    --tolerancia N     percentual de variacao abaixo do qual dois intervalos
                       consecutivos do mesmo nome contam como fixos (default 15)

Duas contagens que o rodizio de nome nao pega, e por isso saem em linha propria
(b1 da rodada 11): texto repetido de outra linha, com teto de 10% das linhas, e
acento. Chat brasileiro sem um acento em mais de 500 caracteres nao foi
escrito em portugues, foi gerado com o teclado errado, e reprova como
`chat sem acentos`.

O CSV esperado tem as colunas do formato de import: username,message,minutes,seconds.
Nomes de coluna alternativos (name/nome, texto/comentario, min, sec/segundos)
sao aceitos. Sem cabecalho reconhecido, as 4 primeiras colunas valem por posicao.

Saida: o bloco de auditoria pronto pra colar no 06-chat-planejamento.md.
Codigo de saida 0 quando toda checagem passa, 1 quando alguma reprova.
"""

import csv
import re
import sys
from collections import Counter, defaultdict

TOLERANCIA_PADRAO = 15
MIN_NOMES_3_FALAS = 8
PISO_ELENCO_PCT = 15
TETO_ELENCO_PCT = 40
PISO_ENTRADAS = 8
PISO_ENTRADAS_OFFSET_CURTO = 4
# b1 · texto repetido e acento
TETO_REPETIDO_PCT = 10
PISO_CARACTERES_ACENTO = 500
RX_ACENTO = re.compile(r"[áéíóúâêôãõçàüÁÉÍÓÚÂÊÔÃÕÇÀÜ]")
RX_SO_LETRA = re.compile(r"[^0-9a-zà-ÿ ]+", re.I)

# Termos que denunciam comentario de PRECO/OFERTA. A lista e conservadora de
# proposito: so entra o que so faz sentido depois do link. Ficam de fora
# "cartao na mao" e "3x por semana", porque antecipacao ("ja to com o cartao
# esperando") a regra autoriza antes do link, e frequencia de treino nao e
# parcelamento. Cada padrao e regex com fronteira de palavra.
TERMOS_PRECO = [
    r"pre[cç]o", r"\bvalor(es)?\b", r"r\$", r"\breais\b",
    r"\bparcel(a|as|ado|amento)\b", r"\d+\s*x\s*(de|r\$)", r"\bà? ?vista\b",
    r"\bboleto\b", r"\bgarantia\b", r"\breembolso\b", r"\bb[oô]nus\b",
    r"\bdesconto\b", r"\binvestimento\b", r"\bmensalidade\b", r"\bcust[ao]\b",
    r"\bcaro\b", r"\bbarato\b", r"\bcupom\b",
]
RX_PRECO = [re.compile(p) for p in TERMOS_PRECO]


def _norma(s):
    return (s or "").strip().lower()


def mmss(segundos):
    return "%d:%02d" % (segundos // 60, segundos % 60)


def parse_mmss(txt, rotulo):
    txt = (txt or "").strip()
    m = re.match(r"^(\d+):([0-5]?\d)$", txt)
    if not m:
        sys.exit("valor invalido para %s: %r (esperado MM:SS)" % (rotulo, txt))
    return int(m.group(1)) * 60 + int(m.group(2))


def ler_csv(caminho):
    """Devolve a lista de linhas como (username, message, segundos)."""
    try:
        with open(caminho, newline="", encoding="utf-8-sig") as fh:
            linhas = list(csv.reader(fh))
    except OSError as erro:
        sys.exit("nao consegui ler %s: %s" % (caminho, erro))

    linhas = [l for l in linhas if l and any(c.strip() for c in l)]
    if not linhas:
        sys.exit("CSV vazio: %s" % caminho)

    alias = {
        "user": ["username", "user", "name", "nome", "usuario", "usuário"],
        "msg": ["message", "msg", "texto", "comentario", "comentário", "mensagem"],
        "min": ["minutes", "minute", "min", "minutos", "minuto"],
        "sec": ["seconds", "second", "sec", "segundos", "segundo"],
    }
    idx = {}
    cabecalho = [_norma(c) for c in linhas[0]]
    for chave, nomes in alias.items():
        for pos, col in enumerate(cabecalho):
            if col in nomes:
                idx[chave] = pos
                break
    if len(idx) == 4:
        corpo = linhas[1:]
    else:
        # sem cabecalho reconhecido: 4 primeiras colunas por posicao
        idx = {"user": 0, "msg": 1, "min": 2, "sec": 3}
        corpo = linhas

    registros = []
    for numero, linha in enumerate(corpo, start=2):
        if max(idx.values()) >= len(linha):
            continue
        bruto_min = linha[idx["min"]].strip()
        bruto_sec = linha[idx["sec"]].strip()
        try:
            segundos = int(float(bruto_min)) * 60 + int(float(bruto_sec))
        except ValueError:
            sys.exit(
                "linha %d com tempo ilegivel: minutes=%r seconds=%r"
                % (numero, bruto_min, bruto_sec)
            )
        registros.append((linha[idx["user"]].strip(), linha[idx["msg"]].strip(), segundos))

    if not registros:
        sys.exit("nenhuma linha de comentario lida em %s" % caminho)
    return registros


def intervalos_fixos(registros, tolerancia_pct):
    """Nomes cujos intervalos consecutivos entre falas variam menos que a tolerancia."""
    por_nome = defaultdict(list)
    for nome, _, segundos in registros:
        por_nome[nome].append(segundos)

    achados = []
    for nome in sorted(por_nome):
        tempos = sorted(por_nome[nome])
        if len(tempos) < 3:
            continue
        gaps = [b - a for a, b in zip(tempos, tempos[1:])]
        for pos, (g1, g2) in enumerate(zip(gaps, gaps[1:])):
            maior = max(g1, g2)
            if maior == 0:
                continue
            variacao = abs(g1 - g2) / maior * 100
            if variacao < tolerancia_pct:
                achados.append(
                    (nome, mmss(tempos[pos]), mmss(tempos[pos + 2]), g1, g2, round(variacao, 1))
                )
    return achados


def trincas_repetidas(registros):
    """Sequencias de 3 nomes consecutivos que aparecem mais de uma vez."""
    nomes = [r[0] for r in registros]
    contagem = Counter(tuple(nomes[i:i + 3]) for i in range(len(nomes) - 2))
    return sorted(
        ((trinca, n) for trinca, n in contagem.items() if n > 1),
        key=lambda par: (-par[1], par[0]),
    )


def _chave_de_texto(mensagem):
    """A mensagem sem caixa, sem pontuacao e sem espaco duplo, pra comparar."""
    return " ".join(RX_SO_LETRA.sub(" ", _norma(mensagem)).split())


def linhas_repetidas(registros):
    """Linhas cujo texto ja apareceu em outra linha. Devolve (total, exemplos)."""
    chaves = [_chave_de_texto(m) for _, m, _ in registros]
    contagem = Counter(k for k in chaves if k)
    repetidas = sum(c for k, c in contagem.items() if c > 1)
    exemplos = sorted(((c, k) for k, c in contagem.items() if c > 1), reverse=True)
    return repetidas, exemplos


def contar_acentos(registros):
    """Caracteres do texto do chat e quantos deles sao acentuados."""
    texto = "".join(m for _, m, _ in registros)
    return len(texto), len(RX_ACENTO.findall(texto))


def cita_preco(mensagem):
    baixa = _norma(mensagem)
    return any(rx.search(baixa) for rx in RX_PRECO)


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    caminho = args[0]
    opcoes = {"--link": None, "--teto": None, "--offset": "5:00",
              "--tolerancia": str(TOLERANCIA_PADRAO)}
    resto = args[1:]
    while resto:
        chave = resto.pop(0)
        if chave not in opcoes:
            sys.exit("opcao desconhecida: %s (rode --help)" % chave)
        if not resto:
            sys.exit("opcao %s pede um valor" % chave)
        opcoes[chave] = resto.pop(0)

    try:
        tolerancia = float(opcoes["--tolerancia"])
    except ValueError:
        sys.exit("--tolerancia pede um numero (percentual)")

    offset = parse_mmss(opcoes["--offset"], "--offset")
    link = parse_mmss(opcoes["--link"], "--link") if opcoes["--link"] else None
    teto = parse_mmss(opcoes["--teto"], "--teto") if opcoes["--teto"] else None

    registros = ler_csv(caminho)
    total = len(registros)
    por_nome = Counter(r[0] for r in registros)
    distintos = len(por_nome)
    com_3_mais = [n for n, c in por_nome.items() if c >= 3]
    piso_20pct = max(1, round(distintos * 0.20))

    fixos = intervalos_fixos(registros, tolerancia)
    trincas = trincas_repetidas(registros)

    pct_elenco = distintos / total * 100
    entradas = sum(1 for _, _, s in registros if 30 <= s <= offset)
    piso_entradas = PISO_ENTRADAS if offset >= 120 else PISO_ENTRADAS_OFFSET_CURTO

    tempos = [s for _, _, s in registros]
    maior = max(tempos)
    fora_de_ordem = sum(1 for a, b in zip(tempos, tempos[1:]) if b <= a)
    duplicados = total - len(set(tempos))
    acima_do_teto = sum(1 for s in tempos if teto is not None and s > teto)
    precos = sorted(s for _, m, s in registros if cita_preco(m))

    reprovas = []
    linhas = []
    linhas.append("## Auditoria do chat, medida por script")
    linhas.append("")
    linhas.append("Arquivo: `%s` · comando: `python3 scripts/auditar_chat.py %s`"
                  % (caminho, " ".join(args)))
    linhas.append("")
    linhas.append("```")
    linhas.append("linhas do CSV: %d" % total)
    linhas.append("nomes distintos: %d (%.1f%% das linhas, regua %d%% a %d%%)"
                  % (distintos, pct_elenco, PISO_ELENCO_PCT, TETO_ELENCO_PCT))
    if not (PISO_ELENCO_PCT <= pct_elenco <= TETO_ELENCO_PCT):
        reprovas.append("elenco em %.1f%% das linhas, fora da regua de %d%% a %d%%"
                        % (pct_elenco, PISO_ELENCO_PCT, TETO_ELENCO_PCT))

    linhas.append("nomes com 3+ falas: %d (minimo %d, piso de 20%% do elenco: %d)"
                  % (len(com_3_mais), MIN_NOMES_3_FALAS, piso_20pct))
    if len(com_3_mais) < max(MIN_NOMES_3_FALAS, piso_20pct):
        reprovas.append("nomes com 3+ falas: %d, abaixo do minimo de %d"
                        % (len(com_3_mais), max(MIN_NOMES_3_FALAS, piso_20pct)))

    linhas.append("com intervalo fixo: %d (tolerancia %.0f%%)" % (len(fixos), tolerancia))
    if fixos:
        reprovas.append("intervalo fixo em %d par(es) de falas consecutivas" % len(fixos))

    linhas.append("sequencias de 3 nomes repetidas: %d" % len(trincas))
    if trincas:
        reprovas.append("%d trinca(s) de nomes repetida(s), sinal de rodizio" % len(trincas))

    linhas.append("entradas na sala de espera (00:30 ate %s): %d (piso %d)"
                  % (mmss(offset), entradas, piso_entradas))
    if entradas < piso_entradas:
        reprovas.append("sala de espera com %d entradas, abaixo do piso de %d"
                        % (entradas, piso_entradas))

    linhas.append("maior timestamp do arquivo: %s" % mmss(maior))
    if teto is not None:
        linhas.append("teto: %s · linhas acima do teto: %d" % (mmss(teto), acima_do_teto))
        if acima_do_teto:
            reprovas.append("%d linha(s) acima do teto de %s" % (acima_do_teto, mmss(teto)))
    else:
        linhas.append("teto: nao informado (rode com --teto MM:SS)")

    if link is not None:
        linhas.append("link no ar em: %s" % mmss(link))
        primeiros = precos[:3]
        linhas.append("3 primeiros timestamps que citam preco, parcela, garantia ou bonus: %s"
                      % (", ".join(mmss(s) for s in primeiros) if primeiros else "nenhum"))
        antes = [s for s in precos if s < link]
        linhas.append("citacoes de preco antes do link: %d" % len(antes))
        if antes:
            reprovas.append("%d citacao(oes) de preco antes do link (%s)"
                            % (len(antes), ", ".join(mmss(s) for s in antes[:5])))
    else:
        linhas.append("link no ar: nao informado (rode com --link MM:SS)")

    # b1 · texto repetido de outra linha. O rodizio de nome passa batido quando
    # o mesmo comentario volta com outro autor: quem le a tela ve a repeticao.
    n_repetidas, exemplos_rep = linhas_repetidas(registros)
    teto_rep = total * TETO_REPETIDO_PCT / 100.0
    linhas.append("linhas com texto repetido de outra linha: %d (teto %d%% das linhas: %.1f)"
                  % (n_repetidas, TETO_REPETIDO_PCT, teto_rep))
    if n_repetidas > teto_rep:
        reprovas.append("texto repetido em %d de %d linhas, acima do teto de %d%%"
                        % (n_repetidas, total, TETO_REPETIDO_PCT))

    # b1 · acento. Zero acento em chat brasileiro longo denuncia texto gerado
    # sem o teclado do idioma, e o lead le isso na tela.
    n_chars, n_acentos = contar_acentos(registros)
    linhas.append("linhas com acento: %d de %d · caracteres: %d · acentos: %d"
                  % (sum(1 for _, m, _ in registros if RX_ACENTO.search(m or "")),
                     total, n_chars, n_acentos))
    if n_acentos == 0 and n_chars > PISO_CARACTERES_ACENTO:
        reprovas.append("chat sem acentos: 0 acento em %d caracteres (piso %d)"
                        % (n_chars, PISO_CARACTERES_ACENTO))

    linhas.append("linhas fora de ordem crescente: %d · timestamps duplicados: %d"
                  % (fora_de_ordem, duplicados))
    if fora_de_ordem or duplicados:
        reprovas.append("ordem quebrada: %d fora de ordem, %d duplicado(s)"
                        % (fora_de_ordem, duplicados))
    linhas.append("```")
    linhas.append("")

    if fixos:
        linhas.append("### Intervalo fixo, par a par")
        linhas.append("")
        linhas.append("| nome | 1a fala do par | 3a fala do par | intervalos (s) | variacao |")
        linhas.append("|---|---|---|---|---|")
        for nome, ini, fim, g1, g2, var in fixos:
            linhas.append("| %s | %s | %s | %d e %d | %.1f%% |" % (nome, ini, fim, g1, g2, var))
        linhas.append("")

    if trincas:
        linhas.append("### Trincas de nomes repetidas")
        linhas.append("")
        linhas.append("| trinca consecutiva | vezes |")
        linhas.append("|---|---|")
        for trinca, vezes in trincas:
            linhas.append("| %s | %d |" % (" > ".join(trinca), vezes))
        linhas.append("")

    if exemplos_rep:
        linhas.append("### Texto repetido, do mais repetido pro menos")
        linhas.append("")
        linhas.append("| texto normalizado | vezes |")
        linhas.append("|---|---|")
        for vezes, chave in exemplos_rep[:20]:
            linhas.append("| %s | %d |" % (chave, vezes))
        linhas.append("")

    linhas.append("Ordem conferida: as %d linhas do CSV estao em ordem crescente de "
                  "(minutes, seconds), sem duas no mesmo segundo: %s"
                  % (total, "sim" if not fora_de_ordem and not duplicados else "NAO"))
    linhas.append("")
    if reprovas:
        linhas.append("**VEREDITO: REPROVA.** Motivos:")
        for motivo in reprovas:
            linhas.append("- %s" % motivo)
    else:
        linhas.append("**VEREDITO: PASSA.** Nenhuma checagem reprovou.")

    print("\n".join(linhas))
    return 1 if reprovas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
