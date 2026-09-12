#!/usr/bin/env python3
"""
checar_entrega.py, o fecho da entrega de vídeo em código.

Duas regras da skill viveram em prosa e foram ignoradas duas rodadas seguidas
pelo mesmo motor. Aqui elas viram comando com exit 1:

1. Zero verbos em `feito` sem PEDIDO-DE-GRAVACAO na pasta é entrega incompleta.
   O dono recebe o bruto reencodado e nenhuma instrução do que gravar.
2. Legenda queimada com mais palavras do que a transcrição devolveu é fala
   inventada no pixel. O MP4 não carrega o relato junto: quem publica, publica
   palavras que ninguém disse.

USO:
    python3 scripts/checar_entrega.py <pasta de saída>
    python3 scripts/checar_entrega.py --help
    python3 scripts/checar_entrega.py --selftest

Só stdlib. Exit 1 reprova a entrega; exit 2 é erro de uso.
"""
import json
import re
import sys
from pathlib import Path

# nome de arquivo de transcrição que o pipeline escreve
GLOBS_TRANSCRICAO = ('*.words.json', 'work/*.words.json')
# marcador que a transcrição devolve quando não há fala. Casa o marcador inteiro
# ([Música]) e também o pedaço solto, porque o whisper devolve "[", "Música", "]"
# como três "palavras" e nenhuma delas é fala.
RX_MARCADOR_FALA = re.compile(r'^\s*(?:\[[^\]]*\]|[\[\]]|'
                              r'[Mm]úsica|[Mm]usica|[Aa]plausos|[Rr]isos|[Ss]ilêncio)\s*$')
PISO_FALA = 5


def _palavras(obj):
    """As palavras de um words.json, em qualquer das formas que o pipeline usa."""
    if isinstance(obj, dict):
        for chave in ('words', 'speech_words', 'segments', 'tokens'):
            if chave in obj:
                return _palavras(obj[chave])
        return []
    if not isinstance(obj, list):
        return []
    saida = []
    for item in obj:
        if isinstance(item, str):
            saida.append(item)
        elif isinstance(item, dict):
            for chave in ('word', 'text', 'palavra'):
                if chave in item and isinstance(item[chave], str):
                    saida.append(item[chave])
                    break
    return saida


def palavras_de_fala(palavras):
    """Palavra de FALA: descarta marcador ([Música], [Aplausos]) e vazio."""
    return [w for w in palavras
            if w.strip() and not RX_MARCADOR_FALA.match(w.strip())]


def ler_json(f):
    try:
        return json.loads(f.read_text(encoding='utf-8', errors='replace'))
    except (OSError, ValueError):
        return None


def achar_words(base):
    """Todo words.json da pasta, separando o que o pipeline transcreveu do que
    foi escrito à mão (o sufixo demo/manual/fake denuncia a origem)."""
    achados = []
    for padrao in GLOBS_TRANSCRICAO:
        achados.extend(base.glob(padrao))
    achados.extend(f for f in base.rglob('*words*.json') if f not in achados)
    reais, mao = [], []
    for f in sorted(set(achados)):
        nome = f.name.lower()
        (mao if re.search(r'demo|manual|fake|sintetic|inventad', nome) else reais).append(f)
    return reais, mao


# (b)7 · `feito` só conta com diferença MEDIDA entre fonte e final. Um reencode
# 1080x1920 → 1080x1920 marcado como "editar feito" deixa a entrega tecnicamente
# conforme e materialmente vazia, e ainda impede o PEDIDO-DE-GRAVACAO de ser
# exigido, porque o contador de `feito` nunca chega a zero.
RX_DIFERENCA = re.compile(r'diferença\s*:\s*(?P<v>[^·|\n]+)', re.I)
# "editar" não é verbo próprio: é a soma dos outros, e marcá-lo infla o placar
VERBO_GUARDA_CHUVA = {'editar', 'edicao', 'edição', 'editar video', 'editar vídeo'}


def diferenca_medida(item):
    """O item traz `diferença: <o quê>` com valor diferente de `nenhuma`?"""
    campos = ' · '.join(str(item.get(k, '')) for k in
                        ('motivo_medido', 'diferenca', 'diferença', 'medida', 'motivo'))
    m = RX_DIFERENCA.search(campos)
    if not m:
        return False, 'sem `diferença:` na linha'
    valor = m.group('v').strip().lower().rstrip('.')
    if valor in ('nenhuma', 'nenhum', 'zero', '0', 'nada'):
        return False, f'diferença: {valor}'
    return True, m.group('v').strip()


def verbos_em_feito(base):
    """Quantos verbos do pedido saíram em `feito` COM diferença medida, e de qual
    arquivo saiu o número. Devolve (n, origem, total, [motivos de recusa])."""
    for padrao in ('verbos-pedido.json', 'audit/verbos*.json', 'audit/veredito.json'):
        for f in sorted(base.glob(padrao)):
            d = ler_json(f)
            if d is None:
                continue
            v = d if isinstance(d, list) else d.get('verbos', [])
            if not isinstance(v, list):
                continue
            n, recusados = 0, []
            for x in v:
                if not isinstance(x, dict) or x.get('estado') != 'feito':
                    continue
                nome = str(x.get('verbo', '')).strip().lower()
                if nome in VERBO_GUARDA_CHUVA:
                    recusados.append(f'{nome}: não é verbo próprio, é a soma dos outros')
                    continue
                ok, porque = diferenca_medida(x)
                if ok:
                    n += 1
                else:
                    recusados.append(f'{nome}: {porque}')
            return n, f.name, len(v), recusados
    return None, None, 0, []


def checar(pasta):
    base = Path(pasta)
    if not base.is_dir():
        print(f'pasta de saída não encontrada: {base}', file=sys.stderr)
        return 2
    falhas = []

    # 1 · verbos em `feito` e o PEDIDO-DE-GRAVACAO
    n_feito, origem, n_verbos, recusados = verbos_em_feito(base)
    pedidos = sorted(base.glob('PEDIDO-DE-GRAVACAO*'))
    if n_feito is None:
        print('verbos em feito: nenhum arquivo de verbos na pasta '
              '(verbos-pedido.json, audit/verbos*.json ou audit/veredito.json)')
        falhas.append('sem arquivo de verbos: o pedido não foi respondido verbo a verbo')
    else:
        print(f'verbos em feito COM diferença medida: {n_feito} de {n_verbos} | {origem}')
        for r in recusados:
            print(f'  fora da conta de `feito`: {r}')
        if recusados:
            falhas.append(
                f'{len(recusados)} verbo(s) marcado(s) `feito` sem diferença medida entre '
                f'fonte e final; a linha sai como `<verbo> | fonte: <medida> · final: '
                f'<medida> · diferença: <o quê>`, e `diferença: nenhuma` obriga '
                f'`nao_aplicavel`')
    print(f'PEDIDO-DE-GRAVACAO na pasta: {len(pedidos)} | ls {base} | grep PEDIDO-DE-GRAVACAO')
    for f in pedidos:
        print(f'  {f.name}')
    if n_feito == 0 and not pedidos:
        falhas.append('zero verbos em feito e nenhum PEDIDO-DE-GRAVACAO: '
                      'a entrega sai marcada PARCIAL e o pedido é escrito ANTES de mostrar')

    # 2 · a legenda queimada nunca tem mais palavras que a transcrição
    reais, mao = achar_words(base)
    n_fala = 0
    for f in reais:
        d = ler_json(f)
        if d is None:
            continue
        n_fala = max(n_fala, len(palavras_de_fala(_palavras(d))))
    n_queimada = 0
    for f in mao:
        d = ler_json(f)
        if d is None:
            continue
        n_queimada = max(n_queimada, len(palavras_de_fala(_palavras(d))))
    print(f'palavras na transcrição: {n_fala} · palavras na legenda queimada: {n_queimada}')
    for f in reais:
        print(f'  transcrição: {f.relative_to(base)}')
    for f in mao:
        print(f'  escrito à mão: {f.relative_to(base)}')
        falhas.append(f'words.json escrito à mão: {f.relative_to(base)} '
                      f'(é PROIBIDO, mesmo declarando que é demonstração)')
    if n_queimada > n_fala:
        falhas.append(f'legenda queimada com {n_queimada} palavras sobre uma transcrição '
                      f'de {n_fala}: fala inventada no pixel')
    if reais and n_fala < PISO_FALA:
        print(f'legendar: nao_aplicavel (transcrição com {n_fala} palavras de fala, '
              f'piso {PISO_FALA}); nenhuma legenda pode ser queimada')

    if falhas:
        print('\nREPROVA, e a entrega não sai:')
        for f in falhas:
            print(f'  x {f}')
        return 1
    print('\nentrega ok: os verbos foram respondidos e nenhuma palavra foi inventada.')
    return 0


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)

        # caso 1: transcrição só com marcador + words.json à mão reprova
        (d / 'work').mkdir()
        (d / 'work' / 'v.words.json').write_text(
            json.dumps([{'word': '['}, {'word': 'Música'}, {'word': ']'}]), encoding='utf-8')
        (d / 'work' / 'v.words.demo.json').write_text(
            json.dumps([{'word': w} for w in
                        'Este e um teste de talking head sintetico'.split()]),
            encoding='utf-8')
        (d / 'verbos-pedido.json').write_text(
            json.dumps([{'verbo': 'legendar', 'estado': 'feito',
                         'motivo_medido': 'fonte: 0 legenda · final: 128 palavras '
                                          '· diferença: legenda queimada'}]), encoding='utf-8')
        assert checar(str(d)) == 1, 'legenda inventada tinha que reprovar'

        # caso 2: zero verbos em feito e sem PEDIDO-DE-GRAVACAO reprova
        (d / 'work' / 'v.words.demo.json').unlink()
        (d / 'verbos-pedido.json').write_text(
            json.dumps([{'verbo': 'legendar', 'estado': 'nao_aplicavel',
                         'motivo_medido': 'speech_words vazio'}]), encoding='utf-8')
        assert checar(str(d)) == 1, 'zero feito sem pedido de gravação tinha que reprovar'

        # caso 3: com o PEDIDO-DE-GRAVACAO na pasta, passa
        (d / 'PEDIDO-DE-GRAVACAO-teste.md').write_text('# Pedido\n', encoding='utf-8')
        assert checar(str(d)) == 0, 'com o pedido de gravação tinha que passar'

        # caso 4: legenda dentro do que a transcrição devolveu passa
        (d / 'work' / 'v.words.json').write_text(
            json.dumps([{'word': w} for w in
                        'hoje eu vou te mostrar as tres fases'.split()]), encoding='utf-8')
        (d / 'verbos-pedido.json').write_text(
            json.dumps([{'verbo': 'legendar', 'estado': 'feito',
                         'motivo_medido': 'fonte: 0 legenda · final: 128 palavras '
                                          '· diferença: legenda queimada'}]), encoding='utf-8')
        assert checar(str(d)) == 0, 'legenda vinda da transcrição tinha que passar'

        # caso 6 · (b)7: `feito` sem diferença medida sai da conta, e a entrega
        # cai no mesmo lugar de zero feito. Reencode 1080x1920 → 1080x1920 é
        # conformidade medida, não efeito medido.
        (d / 'PEDIDO-DE-GRAVACAO-teste.md').unlink()
        (d / 'verbos-pedido.json').write_text(
            json.dumps([{'verbo': 'verticalizar', 'estado': 'feito',
                         'motivo_medido': 'fonte: 1080x1920 · final: 1080x1920 '
                                          '· diferença: nenhuma'}]), encoding='utf-8')
        assert checar(str(d)) == 1, '`feito` com diferença nenhuma tinha que reprovar'

        # "editar" não é verbo próprio: é a soma dos outros
        (d / 'verbos-pedido.json').write_text(
            json.dumps([{'verbo': 'editar', 'estado': 'feito',
                         'motivo_medido': 'fonte: 60s · final: 44s · diferença: 16s'}]),
            encoding='utf-8')
        assert checar(str(d)) == 1, '`editar` como verbo próprio tinha que reprovar'

        # com diferença real e verbo próprio, passa
        (d / 'verbos-pedido.json').write_text(
            json.dumps([{'verbo': 'cortar', 'estado': 'feito',
                         'motivo_medido': 'fonte: 60s · final: 44s · diferença: 16s de '
                                          'pausa removidos'}]), encoding='utf-8')
        assert checar(str(d)) == 0, 'verbo próprio com diferença medida tinha que passar'

        # caso 5: marcador não conta como palavra de fala
        # o whisper devolve "[", "Música", "]": três tokens, zero palavra de fala
        assert palavras_de_fala(['[', 'Música', ']']) == [], 'marcador em pedaços'
        assert palavras_de_fala(['[Música]', 'oi']) == ['oi'], 'marcador fechado sai'
        assert palavras_de_fala(['hoje', 'eu']) == ['hoje', 'eu'], 'fala real fica'

    print('checar_entrega.py self-test OK: words.json à mão reprova, legenda maior que a '
          'transcrição reprova, zero verbos em feito sem PEDIDO-DE-GRAVACAO reprova, '
          '`feito` sem diferença medida entre fonte e final sai da conta, `editar` '
          'não conta como verbo próprio, e a entrega legítima passa.')
    return 0


USO = __doc__


def main(argv):
    argv = list(argv)
    if '--help' in argv or '-h' in argv:
        print(USO)
        return 0
    if '--selftest' in argv or '--self-test' in argv or '--test' in argv:
        return selftest()
    if not argv:
        print('uso: python3 scripts/checar_entrega.py <pasta de saída>', file=sys.stderr)
        return 2
    return checar(argv[0])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
