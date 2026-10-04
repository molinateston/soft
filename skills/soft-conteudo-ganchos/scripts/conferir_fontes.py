#!/usr/bin/env python3
"""conferir_fontes.py, a conferência de fonte do gancho entregue.

Regra em prosa não segura número inventado. Este script lê o gancho entregue e confere,
em código, que cada número, cada nome próprio e cada trecho entre aspas que o público lê
aparece nos insumos do dono. Também reprova lacuna de molde que sobrou na frase.

Número de posição na peça (slide 2, lâmina 3) não é dado e fica de fora.

O que entra na conferência (o que o público lê): o título `# `, os títulos `## ` (o CTA),
as linhas da tabela FALAR | MOSTRAR | TEXTO NA TELA, e na ficha só as linhas "Fala do cliente"
e "Prova na linha". Ficam de fora: cabeçalho e separador de tabela, bloco de código e as
outras linhas da ficha (formato, molde, selo, próximo passo), que são bastidor.

Uso:
    python3 scripts/conferir_fontes.py --gancho <pasta de saída ou ganchos-<slug>.md> --insumos <pasta de insumos do dono>
    python3 scripts/conferir_fontes.py --selftest

Exit 0: tudo com fonte. Exit 1: número, nome ou aspa sem fonte, ou lacuna sobrando. Exit 2: uso errado.
Sem dependência externa.
"""
import argparse
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

EXTENSO = {'dois': 2, 'duas': 2, 'três': 3, 'tres': 3, 'quatro': 4, 'cinco': 5, 'seis': 6, 'sete': 7, 'oito': 8,
           'nove': 9, 'dez': 10, 'onze': 11, 'doze': 12, 'treze': 13, 'quatorze': 14, 'catorze': 14, 'quinze': 15,
           'vinte': 20, 'trinta': 30, 'quarenta': 40, 'cinquenta': 50, 'sessenta': 60, 'setenta': 70, 'oitenta': 80,
           'noventa': 90, 'cem': 100, 'duzentos': 200, 'trezentos': 300, 'quinhentos': 500}
NOME_COMUM = {'instagram', 'whatsapp', 'pix', 'youtube', 'tiktok', 'reels', 'reel', 'google', 'linkedin',
              'facebook', 'direct', 'stories', 'story'}
FICHA_PUBLICA = ('fala do cliente', 'prova na linha')
EXT_INSUMO = {'.md', '.txt', '.csv', '.json', '.tsv'}
PULAR_PASTA = {'conferencia', '.git', '__pycache__', 'node_modules'}
RX_NUM = re.compile(r'(?:R\$\s?)?\d+(?:[.,]\d+)*(?:\s?mil\b)?\s?%?', re.I)
RX_LACUNA = re.compile(r'\[[^\]]*\]')
RX_ESTRUTURAL = re.compile(r'\b(?:slides?|l[aâ]minas?|frames?)\s+\d+', re.I)  # posição na peça, nunca dado


def sem_acento(t):
    return ''.join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn').lower()


def valor(token):
    t = token.strip().lower().replace('r$', '').replace('%', '').strip()
    mil = t.endswith('mil')
    t = t.replace('mil', '').strip()
    if re.fullmatch(r'\d{1,3}(\.\d{3})+(,\d+)?', t):
        t = t.replace('.', '')
    t = t.replace(',', '.')
    try:
        v = float(t)
    except ValueError:
        return None
    return v * 1000 if mil else v


def numeros(texto):
    achados = []
    limpo = RX_ESTRUTURAL.sub(' ', RX_LACUNA.sub(' ', texto))
    for m in RX_NUM.finditer(limpo):
        v = valor(m.group(0))
        if v is not None:
            achados.append((m.group(0).strip(), v))
    for palavra in re.findall(r'[\wáéíóúâêôãõç]+', limpo.lower()):
        if palavra in EXTENSO:
            achados.append((palavra, float(EXTENSO[palavra])))
    return achados


def linhas_publicas(md):
    out = []
    em_codigo = False
    for ln in md.splitlines():
        s = ln.strip()
        if s.startswith('```'):
            em_codigo = not em_codigo
            continue
        if em_codigo or not s:
            continue
        if s.startswith('#'):
            out.append(s.lstrip('#').strip())
            continue
        if s.startswith('|'):
            cel = [c.strip() for c in s.strip('|').split('|')]
            if all(re.fullmatch(r':?-+:?', c or '-') for c in cel):
                continue
            rotulo = sem_acento(cel[0])
            if rotulo in ('falar', 'ficha do gancho'):
                continue  # cabeçalho
            if len(cel) == 2:
                if rotulo in FICHA_PUBLICA:
                    out.append(cel[1])
                continue
            out.extend(cel)
    return out


def nomes(frase):
    achados = []
    limpo = RX_LACUNA.sub(' ', frase)
    for parte in re.split(r'[.!?:;"“”]\s*', limpo):
        palavras = parte.split()
        for i, p in enumerate(palavras):
            w = p.strip(',()\'')
            if i == 0 or not w or not w[0].isupper() or w.isupper() and len(w) <= 6:
                continue
            if sem_acento(w) in NOME_COMUM:
                continue
            achados.append(w)
    return achados


def aspas(frase):
    return [a.strip() for a in re.findall(r'["“]([^"”]{3,})["”]', frase)]


def texto_insumos(pasta):
    partes, n = [], 0
    for f in sorted(Path(pasta).rglob('*')):
        if not f.is_file() or f.suffix.lower() not in EXT_INSUMO:
            continue
        if any(p in PULAR_PASTA for p in f.parts) or f.name.startswith('ganchos-'):
            continue
        partes.append(f.read_text(encoding='utf-8', errors='replace'))
        n += 1
    return '\n'.join(partes), n


def achar_gancho(alvo):
    p = Path(alvo)
    if p.is_file():
        return p
    cands = sorted(p.glob('ganchos-*.md'))
    return cands[0] if cands else None


def conferir(gancho, pasta_insumos, saida=print):
    md = gancho.read_text(encoding='utf-8')
    insumo, n_arq = texto_insumos(pasta_insumos)
    ins_norm = sem_acento(re.sub(r'\s+', ' ', insumo))
    ins_valores = {v for _, v in numeros(insumo)}
    falhas = 0
    publicas = linhas_publicas(md)
    saida(f'gancho: {gancho}')
    saida(f'insumos: {pasta_insumos} ({n_arq} arquivos lidos)')
    lac = [l for l in publicas if RX_LACUNA.search(l)]
    saida(f'lacunas sobrando no gancho: {len(lac)}')
    for l in lac:
        saida(f'  REPROVA lacuna: {l}')
    falhas += len(lac)
    nums = [(tok, v, l) for l in publicas for tok, v in numeros(l)]
    sem = [(tok, l) for tok, v, l in nums if v not in ins_valores]
    saida(f'números no gancho: {len(nums)} · com fonte: {len(nums) - len(sem)} · sem fonte: {len(sem)}')
    for tok, l in sem:
        saida(f'  REPROVA número sem fonte: "{tok}" em: {l}')
    falhas += len(sem)
    nms = [(w, l) for l in publicas for w in nomes(l)]
    nsem = [(w, l) for w, l in nms if sem_acento(w) not in ins_norm]
    saida(f'nomes próprios no gancho: {len(nms)} · com fonte: {len(nms) - len(nsem)} · sem fonte: {len(nsem)}')
    for w, l in nsem:
        saida(f'  REPROVA nome sem fonte: "{w}" em: {l}')
    falhas += len(nsem)
    asp = [(a, l) for l in publicas for a in aspas(l)]
    asem = [(a, l) for a, l in asp if sem_acento(re.sub(r'\s+', ' ', a)) not in ins_norm]
    saida(f'aspas no gancho: {len(asp)} · literais no insumo: {len(asp) - len(asem)} · sem fonte: {len(asem)}')
    for a, l in asem:
        saida(f'  REPROVA aspa sem fonte: "{a}"')
    falhas += len(asem)
    rc = 1 if falhas else 0
    saida(f'conferir_fontes: exit {rc}' + ('' if rc else ' · todo número, nome e aspa do gancho tem fonte no insumo'))
    return rc


def selftest():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / 'insumos').mkdir()
        (d / 'insumos' / 'perfil.md').write_text(
            '- Prova: 11 anos de confeitaria, 380 bolos por mês\n- Fala de cliente: "no fim do mês não sobra nada" · autorizado\n',
            encoding='utf-8')
        bom = d / 'ganchos-bom.md'
        bom.write_text('# 11 anos de bolo: cobre pelo custo da fatia\n\n| Ficha do gancho | |\n|---|---|\n'
                       '| Formato | capa, 9 palavras |\n| Prova na linha | 11 anos |\n', encoding='utf-8')
        ruim = d / 'ganchos-ruim.md'
        ruim.write_text('# 15 anos de bolo com a Marta: "sobra tudo" [SEU NÚMERO]\n', encoding='utf-8')
        mudo = lambda *a: None  # noqa: E731
        assert conferir(bom, d / 'insumos', mudo) == 0, 'o gancho com fonte devia passar'
        assert conferir(ruim, d / 'insumos', mudo) == 1, 'o gancho sem fonte devia reprovar'
        linhas = []
        conferir(ruim, d / 'insumos', linhas.append)
        txt = '\n'.join(linhas)
        for esperado in ('número sem fonte: "15"', 'nome sem fonte: "Marta"', 'aspa sem fonte', 'lacuna'):
            assert esperado in txt, esperado
    print('selftest: ok (passa com fonte; reprova número, nome, aspa e lacuna sem fonte)')
    return 0


def main():
    ap = argparse.ArgumentParser(description='Confere que número, nome e aspa do gancho têm fonte no insumo do dono.')
    ap.add_argument('--gancho', help='pasta de saída ganchos-<slug>/ ou o arquivo ganchos-<slug>.md')
    ap.add_argument('--insumos', help='pasta de insumos do dono (a que contém o perfil)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.gancho or not a.insumos:
        ap.print_help()
        return 2
    g = achar_gancho(a.gancho)
    if not g or not Path(a.insumos).is_dir():
        print('uso: --gancho aponta pra ganchos-<slug>.md (ou a pasta dele) e --insumos pra uma pasta que existe')
        return 2
    return conferir(g, a.insumos)


if __name__ == '__main__':
    sys.exit(main())
