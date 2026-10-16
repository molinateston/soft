#!/usr/bin/env python3
"""
lint_copy.py, gate de COPY em código (anti-IA / anti-voz Soft).

Automatiza o "CTRL+F cada padrão" do filtro-anti-ia/padroes-banidos.md: escaneia
um texto e sinaliza o que cheira a IA. Antes era prosa que o agente varria no
olho (e esquecia); aqui é código que roda igual em toda execução. Sem dependência
externa: roda em qualquer ambiente onde o bot rode.

USO:
    python3 scripts/lint_copy.py peca.txt          # linta um arquivo, exit 1 se HARD
    echo "texto..." | python3 scripts/lint_copy.py - # linta stdin
    python3 scripts/lint_copy.py                    # self-test

HARD (exit 1, zero tolerância): em-dash e a família "travar".
WARN (não bloqueia): padrões que valem no máximo 1x/peça, e o agente decide
reescrever. A lista vem fiel do padroes-banidos.md; o que não dá pra detectar
em código sem falso-positivo (tricolon, simetria, abstrato-virando-promessa)
continua no olho, via teste-voz-alta.md e teste-construtivo.md.
"""
import sys
import re
import unicodedata


def _fold(s):
    """Remove acento (NFKD + descarta marca combinante). Usado pra pegar cliche
    de IA em peca que chega SEM acento (carrossel exportado em ASCII, por ex.:
    'nao e sorte, e pilotagem' tem que reprovar igual a 'nao e sorte, e pilotagem')."""
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))


def _fold_pattern(rx):
    """Recompila um regex com os literais acentuados do proprio padrao sem acento,
    pra rodar contra texto ja sem-acento (_fold do texto). Sintaxe de regex
    (\\s, \\b, chaves, colchetes) nao tem acento, entao so os literais mudam."""
    return re.compile(_fold(rx.pattern), rx.flags)

# ── HARD: bloqueia o export/entrega ──────────────────────────────────────────
HARD = [
    (re.compile(r'—'),
     'EM-DASH (U+2014) banido zero-tolerancia; troque por ponto ou hifen comum. En-dash de faixa numerica (10-20) nao conta.'),
    (re.compile(
        r'\b(trava|travar|travas|travam|travou|travaram|travando|travado|'
        r'travada|travados|travadas|travamento|destrava|destravar|destravam|'
        r'destravou|destravado|destravando)\b', re.I),
     'familia "travar" (anti-voz Soft; use emperrar/empacar/parar/freio/amarra; '
     'excecao so em citacao literal do cliente entre aspas)'),
    # Dupla negação paralela de IA: "Não é X. Não é Y." / "Não é falta de A. Não é falta de B."
    (re.compile(
        r'n[aã]o\s+(?:é|foi|era)\s+[^.!?\n]{1,90}[.!?]\s+'
        r'n[aã]o\s+(?:é|foi|era)\b',
        re.I),
     'dupla "Nao e X. Nao e Y." (antitese paralela classica de IA; diga o que E, sem empilhar negacao)'),
    # "Não é." pelado + virada ("Não é. Falta…" / "Não é. É…")
    (re.compile(r'n[aã]o\s+é\.\s+(?:É|Falta|Faltou|Sobrou)\b', re.I),
     '"Nao e." pelado + virada (molde de IA; complete a frase sem o truque)'),
    # Antítese-nominal telegráfica → HARD (antes era WARN). Mesma régua: polos de 1 palavra,
    # clause-anchored. Fala real do dono com sujeito/verbo ou cauda de +1 palavra escapa.
    (re.compile(
        r'(?:(?<=[.!?])\s+|^)\s*(?:isso\s+)?'
        r'(?:n[aã]o\s+(?:é|foi)\s+[\wáéíóúâêôãõç]+\s*,\s*(?:é|foi)\s+[\wáéíóúâêôãõç]+'
        r'|é\s+[\wáéíóúâêôãõç]+\s*,\s*n[aã]o\s+[\wáéíóúâêôãõç]+)\s*[.!?]',
        re.I | re.M),
     'antitese-nominal telegrafica ("Nao e X, e Y" / "Isso e conta, nao sorte"), banida; '
     'reescreva com sujeito/cena (ex.: "vender nao e convencer, e conduzir" passa)'),
    # "não é X. É Y." com polos curtos (1–3 palavras) colados
    (re.compile(
        r'n[aã]o\s+(?:é|foi)\s+[\wáéíóúâêôãõç]+(?:\s+[\wáéíóúâêôãõç]+){0,2}\s*[.]\s*'
        r'(?:É|Foi)\s+[\wáéíóúâêôãõç]+(?:\s+[\wáéíóúâêôãõç]+){0,2}\s*[.!?]',
        re.I),
     'molde "Nao e X. E Y." (nao e isso, e aquilo), banido; afirme o que e sem o espelho'),
    (re.compile(r'n[aã]o\s+é\s+sobre\s+.{1,40}?[,.]?\s*é\s+sobre\b', re.I),
     'molde "nao e sobre X, e sobre Y" (fechamento generico de coach/IA)'),
    # Muleta de carrossel: empurra o sentido pro "próximo slide" (a seta já existe)
    (re.compile(
        r'(?:'
        r'(?:aparece|continua|segue|vem|explica|revela|mostra|entende|descobre)'
        r'\s+(?:no|na|o|a)\s+pr[oó]xim[oa]\b'
        r'|pr[oó]xim[oa]\s+slide\b'
        r'|no\s+pr[oó]ximo\s*(?:[.]|$)'
        r'|veja\s+(?:a\s+seguir|mais\s+abaixo|o\s+pr[oó]ximo)'
        r'|arrasta(?:r)?\s+(?:pro|para\s+o|pro)\s+lado'
        r'|desliza(?:r)?\s+(?:pro|para\s+o)'
        r'|\bswipe\b'
        r'|o\s+motivo\s+n[aã]o\s+é\s+o\s+que\s+parece'
        r'|n[aã]o\s+é\s+o\s+que\s+parece'
        r')',
        re.I),
     'muleta de swipe/proximo-slide (contexto fora do slide; a seta ja basta, feche a tensao AQUI)'),
    # Personificação Soft Soft (regra de 13/jul): caixa/renda/algoritmo/mês/janela com verbo de humano
    (re.compile(
        r'(?:'
        r'(?:o\s+)?caixa\s+(?:ainda\s+)?'
        r'(?:pergunta|pede|sente|exige|seca|errou)'
        r'|(?:o\s+)?caixa\s+(?:voltar\s+a\s+andar|some\s+com\s+voc[eê]|anda\s+sozinho)'
        r'|\brenda\s+pede\b'
        r'|\balgoritmo\s+come\b'
        r'|\bfeed\s+(?:come|comem)\b'
        r'|\bm[eê]s\s+(?:errou|erra)\b'
        r'|\bjanela\s+(?:errou|erra)\b'
        r')',
        re.I),
     'personificacao Soft Soft (caixa/renda/algoritmo/feed/mes/janela com verbo de humano; '
     'troque por entrada/extrato/alcance/voce)'),
    (re.compile(
        r'(?:influencer|personagem)\s+d[ae]\s+(?:sua\s+|minha\s+|tua\s+)?pr[oó]pria\s+vida',
        re.I),
     'figura-muleta "influencer/personagem da propria vida" (banida pelo dono 15/jul: abstracao '
     'que nao vira cena + reciclada no lote; use a CENA concreta: "gravar story todo dia", '
     '"aparecer o tempo inteiro", "misturar familia e trabalho no feed")'),
]

# ── WARN: revisar (cada um vale no máx 1x/peça) ───────────────────────────────
WARN = [
    (re.compile(r'\b(outrossim|ademais|por conseguinte|vale ressaltar|'
                r'convém notar|sem mais delongas|em suma)\b', re.I),
     'conectivo formal de IA'),
    (re.compile(r'(a verdade é que|o segredo está em|o que ninguém te conta|'
                r'a questão é a seguinte|vou te contar uma coisa|aqui vai o detalhe)', re.I),
     'frase-emoldura de revelação'),
    (re.compile(r'\b(revolucion\w+|redefin\w+|desbloqu\w+|potencializ\w+|'
                r'alavanc\w+|amplific\w+|maximiz\w+|transcend\w+)\b', re.I),
     'verbo de transformação genérico (use concreto: resolve/tira/muda/faz)'),
    (re.compile(r'(pulo do gato|muda o jogo|aqui mora o segredo|isso muda tudo|'
                r'game ?changer)', re.I),
     'frase dramática clichê'),
    (re.compile(r'(imagine só|você já parou pra pensar|já se perguntou|'
                r'e se eu te dissesse)', re.I),
     'abertura banida'),
    (re.compile(r'(espero que tenha ajudado|compartilhe se concorda|comenta aí|'
                r'marca aquele amigo|bora pra cima)', re.I),
     'fechamento que implora engajamento'),
    (re.compile(r'[✨\U0001F680\U0001F4AF\U0001F3AF\U0001F525]'),
     'emoji decorativo (✨🚀💯🎯🔥)'),
]

# ── COUNT: warn quando excede o limite por peça ───────────────────────────────
COUNT = [
    (re.compile(r'\bliteralmente\b', re.I), 1, '"literalmente"'),
    (re.compile(r'\babsolutamente\b', re.I), 1, '"absolutamente"'),
    (re.compile(r'\bverdadeir[oa]s?\b', re.I), 1, '"verdadeiro/a"'),
]


HARD_FOLDED = [(_fold_pattern(rx), label) for rx, label in HARD]


_FENCE_RE = re.compile(r'^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$', re.M | re.S)


def strip_code_blocks(text):
    """Apaga o conteudo de todo bloco de codigo cercado, preservando as linhas.

    Um veredito de critica CITA o trecho reprovado, e a citacao carrega o termo
    banido, entao o lint do proprio veredito pegava a citacao. A regra manda
    citar dentro de bloco de codigo cercado; esta funcao e o outro lado dessa
    regra. So o conteudo do bloco sai: o texto do dono, fora do bloco, continua
    lintado igual. A numeracao de linha se mantem, pro contador de molde nao
    deslocar o '<arquivo>:<linha>'.
    """
    def _blank(m):
        return '\n' * m.group(0).count('\n')
    return _FENCE_RE.sub(_blank, text)


def lint(text):
    """Retorna (hard, warn): listas de (label, trecho)."""
    hard, warn = [], []
    folded_text = _fold(text)
    for (rx, label), (frx, _) in zip(HARD, HARD_FOLDED):
        hits = rx.findall(text)
        if not hits:
            hits = frx.findall(folded_text)
        if hits:
            ex = hits[0] if isinstance(hits[0], str) else hits[0][0]
            hard.append((label, f'{len(hits)}x (ex: "{ex}")'))
    for rx, label in WARN:
        seen = set()
        for m in rx.finditer(text):
            g = m.group(0).lower()
            if g not in seen:
                seen.add(g)
                warn.append((label, m.group(0)))
    for rx, lim, label in COUNT:
        n = len(rx.findall(text))
        if n > lim:
            warn.append((label, f'{n}x (máx {lim})'))
    return hard, warn


# ── MOLDE DE ANTÍTESE: o contador que a régua de títulos (R5) usa como AUTORIDADE ──
# A cota é 1 por peça. A régua manda contar; aqui a contagem sai do arquivo, com o
# número da linha de cada ocorrência, pra ninguém escrever o número de cabeça.
#
# O padrão conta SÓ a negação-espelho: a negação e a afirmação são a mesma frase
# com o polo trocado ("Não é sorte, é conta." / "Não é preguiça. É carga errada.").
# A ordem inversa ("é X, não Y") NÃO entra na cota: em prosa analítica ela é
# aposto comum ("a ancoragem abre pelo custo invisível, não por soma de stack"),
# e contá-la junto inflava o número. Numa peça com 4 moldes reais o contador
# antigo acusava 11, e contador que erra por 7 ensina o motor a ignorar o número.
# Ela continua sendo medida, na linha separada de CONTRASTE_INVERTIDO, fora da cota.
MOLDE_ANTITESE = re.compile(
    r'(?:n[aã]o\s+(?:é|foi|era|seria)\s+[^.!?\n]{1,60}[.,]\s*(?:É|é|Foi|foi|Era|era|Seria|seria)\b'
    r'|n[aã]o\s+é\s+sobre\s+[^.!?\n]{1,40}[,.]?\s*é\s+sobre\b)',
    re.I)

# Fora da cota: contraste em ordem inversa. Medido e relatado, nunca somado ao teto.
CONTRASTE_INVERTIDO = re.compile(
    r'(?:é|foi)\s+[^.!?\n]{1,60},\s*n[aã]o\s+[^.!?\n]{1,40}[.!?]',
    re.I)

# A versão sem acento do molde: a peça às vezes exporta em ASCII ("nao e sorte, e
# conta") e o número não pode mudar com o encoding. O "e" desacentuado é também a
# conjunção mais comum do português, então a forma folded só vale ANCORADA na
# negação inicial: sem essa âncora ela transformava qualquer aposto em molde.
MOLDE_ANTITESE_FOLDED = _fold_pattern(MOLDE_ANTITESE)


def molde_antitese(text, origem='<peça>'):
    """Devolve a lista de '<arquivo>:<linha>: <trecho>' de cada ocorrência do molde.

    Conta com e sem acento: peça exportada em ASCII ('nao e sorte, e conta')
    tem que somar igual à acentuada, senão o número muda com o encoding. O
    padrão sem acento só entra quando o acentuado não pegou nada na linha, pra
    a mesma ocorrência não contar duas vezes.
    """
    return _varre(MOLDE_ANTITESE, MOLDE_ANTITESE_FOLDED, text, origem)


def contraste_invertido(text, origem='<peça>'):
    """Contraste em ordem inversa ("é X, não Y"). FORA da cota de R5.

    Sai numa linha própria pra quem escreve ver o que o molde não conta, sem
    que o número entre no teto: em prosa analítica esta forma é aposto, não
    molde de IA.
    """
    return _varre(CONTRASTE_INVERTIDO, _fold_pattern(CONTRASTE_INVERTIDO), text, origem)


def _varre(rx, rx_folded, text, origem):
    achados = []
    for n, linha in enumerate(text.splitlines(), 1):
        achou = [m.group(0).strip() for m in rx.finditer(linha)]
        if not achou:
            achou = [m.group(0).strip() for m in rx_folded.finditer(_fold(linha))]
        for trecho in achou:
            achados.append(f'{origem}:{n}: {trecho}')
    return achados


def _run(text, origem='<peça>'):
    hard, warn = lint(text)
    for label, ex in warn:
        print(f'  ⚠ {label}: {ex}')
    moldes = molde_antitese(text, origem)
    print(f'molde de antítese: {len(moldes)} (teto 1)')
    for linha in moldes:
        print(f'  · {linha}')
    if len(moldes) > 1:
        print('  ↑ acima do teto: o lote volta pro passo de escrita. '
              'Este número é a autoridade; número declarado diferente reprova a peça.')
    invertidos = contraste_invertido(text, origem)
    print(f'contraste invertido ("é X, não Y"): {len(invertidos)} (fora da cota)')
    for linha in invertidos:
        print(f'  · {linha}')
    if hard:
        print(f'\n✗ COPY REPROVADA ({len(hard)} falha dura):')
        for label, ex in hard:
            print(f'  ✗ {label}: {ex}')
        print('\nReescreva e rode de novo.')
        return 1
    print(f'✓ copy passou no anti-IA em código (0 falhas duras, {len(warn)} aviso(s) pra revisar no olho).')
    return 0


def _self_test():
    dirty = 'O método destrava tudo — literalmente. Isso muda o jogo. ✨'  # em-dash proposital: o self-test precisa de um caso sujo
    h, w = lint(dirty)
    assert any('EM-DASH' in l for l, _ in h), 'devia pegar em-dash'
    assert any('travar' in l for l, _ in h), 'devia pegar destrava'
    assert any('dramática' in l for l, _ in w), 'devia avisar "muda o jogo"'
    clean = 'O lead certo chega já querendo. Você mostra numa aula e ele compra.'
    h2, w2 = lint(clean)
    assert not h2, 'copy limpa não devia ter falha dura'

    def _hard(txt, needle):
        hh, _ = lint(txt)
        return any(needle in l for l, _ in hh)

    # ── antítese / dupla negação: HARD ─────────────────────────────────────────
    assert _hard('Não é falta de talento. Não é falta de esforço.', 'dupla'), 'dupla nao-e'
    assert _hard('Não é. Falta a venda acontecer.', 'pelado'), 'Nao e. pelado'
    assert _hard('Cinco pessoas, três milhões. Isso é conta, não sorte.', 'antitese-nominal'), 'telegráfica'
    assert _hard('Não é sorte, é conta.', 'antitese-nominal'), 'Nao e X, e Y'
    assert _hard('A boa notícia: conduzir não é dom. É estrutura.', 'Nao e X. E Y'), 'Nao e X. E Y'
    assert _hard('E não é sobre o preço, é sobre profundidade.', 'nao e sobre'), 'sobre X/Y'
    assert _hard('Tem colega pior. O motivo aparece no próximo.', 'muleta'), 'proximo-slide'
    assert _hard('O motivo não é o que parece.', 'muleta'), 'nao e o que parece'
    assert _hard('Veja a seguir o mecanismo.', 'muleta'), 'veja a seguir'
    assert _hard('Em julho o caixa ainda pergunta se você vai aparecer.', 'personificacao'), 'caixa pergunta'
    assert _hard('Enquanto a renda pede câmera todo dia, você não tem folga.', 'personificacao'), 'renda pede'
    assert _hard('O algoritmo come. O mês não fecha.', 'personificacao'), 'algoritmo come'

    # ── falas REAIS do dono: NÃO podem ser HARD de antítese ────────────────────
    reais = [
        'vender não é convencer, é conduzir',
        'educar não vende',
        'eu gerenciei dezenas de milhões, não faturei',
        'O vilão não é você, é a fama que o funil ganhou.',
        'Porque vender não é ensinar, é fazer decidir.',
        'Funil que só vende pra seguidor não é funil, é plateia.',
        'Prospectar 200 pessoas no direct pra marcar 1 reunião não é negócio, é desgaste no dedo.',
        'Não foi convencimento, foi ensino em sequência.',
        'Não é uma fase corrida de trabalho, é o modelo inteiro.',
        'Se a venda para no dia que você para, isso não é negócio, é plantão.',
    ]
    for r in reais:
        hh, _ = lint(r)
        ant = [l for l, _ in hh if 'antitese' in l or 'dupla' in l or 'pelado' in l
               or 'Nao e X' in l or 'nao e sobre' in l]
        assert not ant, f'FALSO-POSITIVO HARD em fala real: {r!r} -> {ant}'

    # ── mesmos padroes, texto SEM ACENTO (peca as vezes exporta em ASCII) ──────
    assert _hard('Isso nao e sorte, e pilotagem.', 'antitese-nominal'), 'ASCII: Nao e X, e Y'
    assert _hard('Nao e sorte. E pilotagem.', 'Nao e X. E Y'), 'ASCII: Nao e X. E Y'
    assert _hard('Nao e sobre o preco, e sobre profundidade.', 'nao e sobre'), 'ASCII: nao e sobre'
    for r in [_fold(x) for x in reais]:
        hh, _ = lint(r)
        ant = [l for l, _ in hh if 'antitese' in l or 'dupla' in l or 'pelado' in l
               or 'Nao e X' in l or 'nao e sobre' in l]
        assert not ant, f'FALSO-POSITIVO HARD em fala real SEM ACENTO: {r!r} -> {ant}'

    # ── contador de molde: sai do arquivo, com numero de linha ─────────────────
    assert len(molde_antitese('linha limpa\nnao e sorte, e conta.\n')) == 1, 'contador de molde'
    assert molde_antitese('nao e sorte, e conta.', 'p.md')[0].startswith('p.md:1:'), 'origem:linha'

    # ── --ignore-code-blocks apaga so o conteudo do bloco, sem mover a linha ───
    com_bloco = 'texto limpo\n```\nnao e sorte, e conta.\n```\nfim\n'
    assert molde_antitese(strip_code_blocks(com_bloco)) == [], 'fence devia zerar o molde citado'
    assert len(strip_code_blocks(com_bloco).splitlines()) == len(com_bloco.splitlines()), 'fence nao pode mover linha'
    assert molde_antitese(com_bloco), 'sem a flag, a citacao continua contando'

    _selftest_molde()

    print('lint_copy.py self-test OK: HARD (em-dash, travar, dupla nao-e, antitese, '
          'nao-e-sobre, muleta, personificacao) + falas REAIS do dono passam limpas.')
    print('uso: python3 scripts/lint_copy.py peca.txt   |   echo "..." | python3 scripts/lint_copy.py -')


def _selftest():
    """Entrada nomeada do self-test (`--selftest`, `--self-test`, `--test`).

    Roda a bateria inteira: os padroes HARD, as falas reais do dono que nao
    podem reprovar, e os 3 casos de molde-vs-prosa de `_selftest_molde`.
    """
    return _self_test()


def _selftest_molde():
    """Os 3 casos que separam MOLDE de PROSA (o defeito que errava por 7).

    1. molde de verdade: negacao-espelho, entra na cota.
    2. prosa que PARECE molde: aposto em ordem inversa, fica FORA da cota.
    3. bloco de codigo: a citacao do molde some com --ignore-code-blocks.
    """
    # 1. molde verdadeiro: a negacao e a afirmacao sao a mesma frase com o polo trocado
    for verdadeiro in [
        'Nao e sorte, e conta.',
        'Não é preguiça. É carga errada.',
        'Não é sobre o preço, é sobre profundidade.',
    ]:
        assert len(molde_antitese(verdadeiro)) == 1, f'molde verdadeiro nao contado: {verdadeiro!r}'
        assert contraste_invertido(verdadeiro) == [], f'molde nao e contraste invertido: {verdadeiro!r}'

    # 2. prosa analitica que PARECE molde: aposto em ordem inversa, fora da cota
    prosa = [
        'a ancoragem abre pelo custo invisivel (P5), nao por soma de stack.',
        'É pedido de UMA oferta, não da esteira inteira.',
        'e a progressao segue o ritmo do seu corpo, nao o do calendario.',
    ]
    for p in prosa:
        assert molde_antitese(p) == [], f'FALSO-POSITIVO de molde em prosa: {p!r}'
    assert len(contraste_invertido(prosa[0])) == 1, 'o aposto tem que sair na linha fora da cota'

    # a peca inteira: 4 moldes de verdade e a prosa toda fora da cota
    peca = '\n'.join(['Nao e sorte, e conta.', 'Não é preguiça. É carga errada.'] + prosa)
    assert len(molde_antitese(peca, 'peca.md')) == 2, 'contagem da peca mista'
    assert len(contraste_invertido(peca, 'peca.md')) == 3, 'contagem invertida da peca mista'

    # 3. bloco de codigo: a citacao do molde nao conta com a flag, conta sem ela
    doc = 'antes\n```\nNao e sorte, e conta.\n```\ndepois\n'
    assert len(molde_antitese(doc)) == 1, 'sem a flag, a citacao no bloco conta'
    assert molde_antitese(strip_code_blocks(doc)) == [], 'com a flag, o bloco nao conta'

    # o formato <arquivo>:<linha> nao muda
    assert molde_antitese('Nao e sorte, e conta.', 'p.md')[0].startswith('p.md:1:'), 'origem:linha'


USO_TEXTO = """lint_copy.py, gate de COPY em codigo (anti-IA / anti-voz).

uso:
  python3 scripts/lint_copy.py peca.md                        linta um arquivo (exit 1 se HARD)
  python3 scripts/lint_copy.py peca.md --ignore-code-blocks   ignora o conteudo dos blocos ``` (pra veredito que CITA o trecho reprovado)
  echo "texto..." | python3 scripts/lint_copy.py -            linta stdin
  python3 scripts/lint_copy.py --selftest                     roda o self-test (--self-test e --test valem igual)
  python3 scripts/lint_copy.py --help                         mostra esta ajuda

saida: a linha "molde de antitese: N (teto 1)" e a AUTORIDADE da contagem.
Numero declarado diferente do numero do script reprova a peca.
A linha "contraste invertido" ("e X, nao Y") sai LOGO ABAIXO e fica FORA da cota:
em prosa analitica essa forma e aposto comum, e somar as duas inflava o numero."""


def _cli(argv):
    if '--help' in argv or '-h' in argv:
        print(USO_TEXTO)
        return 0
    skip_fences = False
    restantes = []
    for a in argv:
        if a in ('--ignore-code-blocks', '--ignore-fences'):
            skip_fences = True
        else:
            restantes.append(a)
    if not restantes or restantes[0] in ('--self-test', '--selftest', '--test'):
        _selftest()
        return 0
    arg = restantes[0]
    if arg.startswith('--'):
        print(f'opcao desconhecida: {arg}\n')
        print(USO_TEXTO)
        return 2
    try:
        txt = sys.stdin.read() if arg == '-' else open(arg, encoding='utf-8').read()
    except FileNotFoundError:
        print(f'arquivo nao encontrado: {arg}\n')
        print(USO_TEXTO)
        return 2
    if skip_fences:
        txt = strip_code_blocks(txt)
    # entidade HTML do travessao (&mdash; &#8212; &#x2014;) passava reto pelo gate:
    # decodifica ANTES de lintar, senao o em-dash entra escapado e nao e visto.
    import html as _html
    txt = _html.unescape(txt)
    return _run(txt, 'stdin' if arg == '-' else arg)


if __name__ == '__main__':
    sys.exit(_cli(sys.argv[1:]))
