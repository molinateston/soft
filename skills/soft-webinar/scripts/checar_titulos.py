#!/usr/bin/env python3
"""
checar_titulos.py, o fecho da régua de títulos em código.

O defeito que este script existe pra matar: número declarado sem comando por
trás. O motor conta de cabeça, recorta o universo pra uma seção, esquece linhas
da lista FECHADA e escreve um fecho que parece checagem e não é. Aqui cada
número sai de um comando, e o comando sai impresso ao lado do número.

O script NÃO julga conteúdo. Ele imprime o bloco de fecho da régua já preenchido
com o que dá pra contar, e deixa `<preencher>` nas linhas de julgamento humano.
O agente cola a saída INTEIRA em checagem-titulos.md e substitui cada
`<preencher>`, e nada mais. `<preencher>` sobrando reprova; número escrito à mão
diferente do impresso reprova.

USO (caminhos relativos à pasta da skill):
    python3 scripts/checar_titulos.py \\
        --peca headlines-x.md --titulos titulos.txt \\
        --teses teses.txt --insumos ../insumos --perfil ../dono.md \\
        --ressalva "Avaliação individual antes de começar." \\
        --nomes nomes.txt

    python3 scripts/checar_titulos.py --help
    python3 scripts/checar_titulos.py --selftest

DOIS PASSOS. O passo 1 (acima) imprime o bloco pra você colar e preencher. O
passo 2 relê o que você preencheu e confere:

    python3 scripts/checar_titulos.py --conferir <pasta de saída>

O --conferir exige checagem-titulos.md na raiz da pasta, reprova `<preencher>`
sobrando, conta os títulos das peças da pasta contra o lote declarado, e roda o
lint em TODO .md e .json da pasta, RELATO incluso. O universo de títulos soma
.md, .html e .pptx: peça que não é markdown continua sendo peça, e zero por
ausência de varredura sai como `sem peça varrível: <motivo>`, nunca como número.
O .pptx é lido de volta antes de fechar, com lint no texto extraído e a contagem
de acentos comparada com a do .md de mesmo nome-base. A primeira linha da saída
é o comando literal com os caminhos absolutos, pra colar no RELATO, e o exit do
RELATO.md sai por último, em linha própria.

A varredura de nome roda sobre a PEÇA PÚBLICA: linha de bastidor dentro de
arquivo de planejamento (candidato, descarte, proibição, comando de grep) e
bloco cercado de código ficam de fora, porque documentar o descarte é
cumprimento da régua, nunca a infração dela. O universo de títulos é de título
de COPY: cabeçalho markdown de documento operacional não entra, e a linha
`universo:` declara quais arquivos foram contados. Os números do inventário são
recontados sobre a tabela da pasta, e cada `<arquivo>: N bytes` declarado no
relato é conferido contra `wc -c`, com tolerância 0.

R13, o crivo do dono: o bastidor (titulos.txt, teses.txt, nomes.txt,
checagem-titulos.md, conferir.txt) mora em `conferencia/`, e a raiz da pasta
fica com o entregável e o handoff. O relato abre com `Pronto:`, `Abra
primeiro:` e `Falta você responder:` e fecha com `Perguntas pra você`. Título
em caixa alta, comando entregue ao dono e jargão interno sem glosa saem por
exit 1. Nome de pessoa fica no arquivo interno que o dono usa.

EXIT 1 quando: molde acima do teto, ressalva acima de 1 no lote inteiro,
marcador no miolo de frase, marcador com mais de 6 palavras dentro dos colchetes,
palavra-chave de CTA sem origem literal nos insumos, lint da peça com exit
diferente de 0, nome de pessoa sem autorização no insumo, nome vindo de conversa
privada sem autorização (o script acha o candidato sozinho, sem --nomes), número
de terceiro sem a tripla `trecho | url | consultado em`, afirmação de verificação
sem a saída crua colada abaixo, número do inventário diferente do que a tabela
devolve (`inventário redigitado`), tamanho em bytes diferente do `wc -c`
(`bytes redigitados`), ou marcador no HTML de render (--render). Exit 0
é a última coisa que acontece: rode depois de tudo escrito.
"""
import argparse
import io
import os
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# ── marcador de pendência ────────────────────────────────────────────────────
RX_MARCADOR = re.compile(r'\[(?:A CONFIRMAR|DADO|CONFIRMAR)[^\]]*\]')
# linha de tabela markdown
RX_CELULA = re.compile(r'^\s*\|')
# item de lista markdown (-, *, +, 1.)
RX_ITEM = re.compile(r'^\s*(?:[-*+]|\d+[.)])\s+')
# cabeçalho de bloco onde marcador é campo por natureza
RX_BLOCO_CAMPO = re.compile(r'dados fornecidos|furos|handoff', re.I)
# palavra-chave de CTA: o mesmo alvo que a régua manda grepar nos insumos
RX_CTA = re.compile(r'manda |comenta |envia |digita |palavra |chama ', re.I)
# a palavra que a seguidora vai DIGITAR: caixa alta, 3+ letras, número opcional
RX_CAIXA_ALTA = re.compile(r'\b[A-ZÀ-Þ][A-ZÀ-Þ0-9]{2,}\b')
# sigla comum que aparece em CTA e não é palavra-chave de automação
SIGLAS_COMUNS = {
    'CTA', 'PDF', 'URL', 'DM', 'IG', 'WHATSAPP', 'WPP', 'LINK', 'BIO', 'HTML',
    'CSV', 'JSON', 'PNG', 'JPG', 'MP4', 'API', 'FAQ', 'VSL', 'SDR', 'CRM',
    'REELS', 'STORIES', 'FEED', 'DIRECT', 'SIM', 'NAO', 'NÃO', 'OK', 'ATENCAO',
    'ATENÇÃO', 'IMPORTANTE', 'OBS', 'PS', 'CEP', 'CPF', 'CNPJ', 'HOJE', 'AGORA',
}
# ── aspa atribuída a pessoa: verbatim tem que ter lastro no insumo ────────────
# O modelo INVENTA a fala do dono ou do cliente e depois CARIMBA a prova de que
# não inventou ("verbatim literal de mensagem real"). Nenhuma regra segura isso,
# porque o modelo desobedece e mente sobre ter obedecido. Só o script, cego ao
# que o modelo alega, lê a aspa contra o insumo: fala entre aspas atribuída a
# alguém tem que ser substring literal (normalizada) de algum arquivo de insumo,
# ou é verbatim potencialmente fabricado e reprova.
# A aspa: texto entre "reta", “curva”, ou «guillemet». Aspa simples de uma
# palavra fica de fora (o piso de tamanho abaixo), pra não pegar ênfase.
RX_ASPA = re.compile(r'"([^"\n]+)"|“([^”\n]+)”|«([^»\n]+)»')
TAM_MIN_ASPA = 15  # abaixo disso é ênfase de 1-2 palavras, não citação de fala
# marcador de que a aspa é FALA de uma pessoa (depoimento, verbatim, "disse"),
# não a headline ou a tese da própria peça, que o dono escreve sem citar ninguém
RX_MARCADOR_CITACAO = re.compile(
    r'\b(disse|falou|escreveu|relatou|contou|perguntou|comentou|respondeu|'
    r'desabafou|mandou|mensagem|mensagens|depoimento|depoimentos|verbatim|'
    r'coment[áa]rio|dm\b|direct|whatsapp|print|caixa de entrada|palavras dela|'
    r'palavras dele|nas palavras|me escreveu|me mandou|me disse|me falou|'
    r'cliente|aluna|aluno|alunas|alunos|seguidora|seguidor|paciente|lead|'
    r'uma mulher|uma pessoa|relato)\b', re.I)
# nome de pessoa seguido de idade ou dois-pontos: "Simone, 51" ou "Fernanda:" na
# própria linha da aspa também marca citação (o padrão de depoimento do método)
RX_PESSOA_ANTES_ASPA = re.compile(
    r'\b[A-ZÀ-Þ][a-zà-ÿ]{2,}\s*(?:,\s*\d{1,3}\b|:)')
# ── R13 · headline em caixa alta ─────────────────────────────────────────────
# Pedido do dono, e vale nas 47: ênfase é por palavra, nunca por tecla. Título,
# headline, capa, assunto e CTA com 8 ou mais letras e 80% ou mais delas em
# maiúscula saem por exit 1. Escapam a sigla de até 6 letras e a palavra-chave
# de CTA que existe literal nos insumos, porque essa a seguidora digita.
CAIXA_ALTA_MIN_LETRAS = 8
CAIXA_ALTA_PROPORCAO = 0.8
RX_LETRA = re.compile(r'[A-Za-zÀ-ÿ]')
RX_LETRA_MAIUSCULA = re.compile(r'[A-ZÀ-Þ]')
RX_PALAVRA_LETRAS = re.compile(r'[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9]*')


def caixa_alta_demais(linha, palavras_chave=()):
    """A linha grita? Devolve a proporção quando grita, senão None.

    Conta só letra: número, pontuação e emoji ficam de fora, porque `3 TREINOS`
    grita pelas letras e não pelo algarismo. Retira antes as siglas de até 6
    letras e as palavras-chave de CTA achadas nos insumos: elas moram em
    maiúscula por função.
    """
    texto = re.sub(r'^\s*#{1,6}\s*', '', str(linha)).strip()
    texto = texto.strip('*_`> ').strip()
    if not texto:
        return None
    isentas = {str(p).upper() for p in palavras_chave if str(p).strip()}
    letras = maiusculas = 0
    for m in RX_PALAVRA_LETRAS.finditer(texto):
        palavra = m.group(0)
        so_letras = ''.join(RX_LETRA.findall(palavra))
        if not so_letras:
            continue
        # sigla curta e palavra-chave de CTA moram em maiúscula por função
        if so_letras.upper() == so_letras and (len(so_letras) <= 6
                                               or palavra.upper() in isentas):
            continue
        letras += len(so_letras)
        maiusculas += len(RX_LETRA_MAIUSCULA.findall(so_letras))
    if letras < CAIXA_ALTA_MIN_LETRAS:
        return None
    proporcao = maiusculas / letras
    return proporcao if proporcao >= CAIXA_ALTA_PROPORCAO else None


# título da peça: markdown de 1 a 4, "**Slide N", "Slide N", "Frame N"
RX_TITULO_PECA = re.compile(r'^(?:#{1,4} |\*\*Slide|Slide [0-9]|Frame [0-9])')
# rótulo de seção estrutural: a régua (R2) o mantém FORA da tabela, porque ele
# nunca disputou a atenção do leitor. Contá-lo infla o universo com linha que a
# régua não cobre, e reprova a entrega por um título que não existe.
RX_ROTULO_SECAO = re.compile(
    r'^#{1,4}\s*(?:\**\s*)?(?:bloco|se[çc][ãa]o|parte|etapa|passo|m[óo]dulo|'
    r'anexo|ap[êe]ndice|[íi]ndice|sum[áa]rio|bio|faq|perguntas frequentes|'
    r'para quem [ée]|sobre|o argumento|handoff|relato|checagem)\b', re.I)
# marcador queimável dentro de HTML de render
RX_MARCADOR_HTML = re.compile(r'\[(?:A CONFIRMAR|DADO|CONFIRMAR)')
# duas orações separadas por ponto final, a segunda completando a primeira.
# É o "quase-antítese" que o lint não pega e que a régua manda contar para mais.
RX_DUAS_ORACOES = re.compile(
    r'^\s*(?P<a>[^.!?\n]{6,}?[a-zà-ÿ0-9)"\'])\.\s+(?P<b>[A-ZÀ-Þ0-9][^.!?\n]{4,})[.!?]?\s*$'
)
# molde de antítese numa oração só, separado por VÍRGULA + negação: "X, não Y",
# "X, nunca Y", "X, e não Y" (a segunda metade NEGA/inverte a primeira). É o mesmo
# contraste que "A. B." carrega, e a régua manda contar igual. O gancho é a vírgula
# seguida da negação de contraste — "não"/"nunca" logo após a vírgula, precedida de
# uma metade A com corpo. Não pega "não" no meio de oração normal (sem vírgula antes
# dele): "O treino que não machuca", "3 erros que você não sabe" ficam de fora.
RX_ANTITESE_VIRGULA = re.compile(
    r'[a-zà-ÿ0-9)"\']{3,}\s*,\s*(?:e\s+)?(?:n[ãa]o|nunca)\s+\S', re.I)
# abreviação comum que produz ponto sem fim de oração
RX_ABREV = re.compile(r'\b(sr|sra|dr|dra|prof|ex|etc|vs|min|seg|kg|km|art|n[ºo])\.\s*$', re.I)
RX_AUTORIZ = re.compile(r'autorizad', re.I)
# C1(a)1 e (a)2 · cabeçalho de peça pública com padrão de RÓTULO. A isenção
# estrutural virou porta de saída: três pastas renomearam os títulos internos
# pra caírem nela, e uma declarou a manobra no relato. Daqui pra frente só
# FAQ, Bio, Índice, Sumário, Referências e Anexo (mais o documento operacional)
# ficam de fora; `Etapa`, `Passo`, `Seção`, `Bloco`, `P3`, `Parte`, `Checagem` e
# `Frase que sobrevive` entram no universo e reprovam como rótulo no miolo.
RX_ROTULO_NO_MIOLO = re.compile(
    r'^#{1,4}\s*(?:\**\s*)?(?:etapa|passo|se[çc][ãa]o(?:\s+de\s+fecho)?|bloco|'
    r'parte|checagem|invent[áa]rio|r[ée]gua|frase que sobrevive|p\s*[0-9])\b', re.I)
# a isenção que sobrou: rótulo que nunca disputou a atenção do leitor
RX_ROTULO_ISENTO = re.compile(
    r'^#{1,4}\s*(?:\**\s*)?(?:faq|perguntas frequentes|bio|[íi]ndice|sum[áa]rio|'
    r'refer[êe]ncias|anexo|ap[êe]ndice)\b', re.I)
# C1(b)1 · arquivo que o próprio gate escreve: o tamanho dele descreve a rodada
# anterior, então declarar `wc -c` sobre ele é impossível de acertar
RX_ARQUIVO_DO_GATE = re.compile(
    r'^(?:conferir[\w.\-]*\.txt|checar-passo1[\w.\-]*\.txt|checagem-raw[\w.\-]*\.txt)$',
    re.I)
# B(b)2 · a conclusão que nega a saída colada na mesma checagem
RX_CHAVE_NENHUMA = re.compile(
    r'palavra[- ]chave\s*(?:de CTA)?\s*:\s*nenhuma', re.I)
RX_CHAVE_ACHADA = re.compile(
    r'(?:trecho de CTA encontrado|palavra[- ]chave\s*(?:de CTA)?\s*:\s*'
    r'(?!nenhuma)[A-Z0-9])', re.I)
RX_DESCARTE_NAO_CONSTA = re.compile(r'descartad\w*\s+porque\s+n[ãa]o consta', re.I)
# C1(b)3 · a versão morta que a R7 cobra
RX_REESCRITO_DE = re.compile(r'reescrito de\s*:', re.I)
# B(a)1 · número que no perfil mora na mesma linha de um marcador
RX_NUM_NA_LINHA = re.compile(r'(?<![\w,.])(\d{1,3}(?:[.,]\d+)?)(?![\w])')
# B(a)1 / PENDENTE-r14 · o número só é "não confirmado" quando carrega a unidade
# ou o substantivo que o perfil lhe dá (`6 semanas`, `52 anos`, `R$ 63`). Dígito
# solto de 1 a 2 casas (o `2` de uma série, o `6` de uma faixa) nunca reprova: o
# gate estava ensinando o motor a escrever `dois` na tabela pra passar. Captura o
# número COM a unidade colada, antes ou depois, e ignora o dígito órfão.
RX_NUM_COM_UNIDADE = re.compile(
    r'(?<![\w,.])'
    r'(?:(?P<pre>R\$\s*))?'
    r'(?P<num>\d{1,3}(?:[.,]\d+)?)'
    r'\s*(?P<pos>%|anos?|meses|mês|semanas?|dias?|horas?|minutos?|min|kg|km|reais|'
    r'mil|k\b|clientes?|alunos?|alunas?|pessoas?|vezes|x\b)?',
    re.I)
# conserto extenso · o grep do gate só vê o algarismo. O motor que quer driblar
# escreve o dado marcado [A CONFIRMAR] POR EXTENSO ("seis semanas" no lugar de
# "6 semanas") e a peça passa. Aqui mapeio extenso->dígito pra 1..12, e quando o
# perfil marca um dígito COM unidade de tempo/quantidade, também caço a forma por
# extenso desse mesmo dígito perto da MESMA unidade na peça pública. Só cai o que
# o perfil marcou [A CONFIRMAR: número que tem lastro literal no dono.md (ex "três
# fases") nunca é número marcado, então nunca é alvo — sem falso positivo.
EXTENSO_PARA_DIGITO = {
    'um': '1', 'uma': '1', 'dois': '2', 'duas': '2', 'tres': '3', 'três': '3',
    'quatro': '4', 'cinco': '5', 'seis': '6', 'sete': '7', 'oito': '8',
    'nove': '9', 'dez': '10', 'onze': '11', 'doze': '12',
}
DIGITO_PARA_EXTENSO = {}
for _ext, _dig in EXTENSO_PARA_DIGITO.items():
    DIGITO_PARA_EXTENSO.setdefault(_dig, []).append(_ext)
# unidade de tempo/quantidade que dá corpo ao número por extenso (o mesmo universo
# do RX_NUM_COM_UNIDADE, sem % nem moeda, que não se escrevem colados a extenso).
RX_UNIDADE_EXTENSO = (r'anos?|meses|mês|semanas?|dias?|horas?|minutos?|min|kg|km|'
                      r'clientes?|alunos?|alunas?|pessoas?|vezes|vagas?')

# ── candidato a nome de pessoa ───────────────────────────────────────────────
# Palavra capitalizada de 3+ letras (acento conta). O filtro de verdade não é a
# forma, é o contexto: a mesma palavra tem que aparecer nos insumos em linha de
# pessoa, e nunca em minúscula em lugar nenhum.
RX_CAPITALIZADA = re.compile(r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ][a-záàâãéêíóôõúüç]{2,}\b')
# (a)1 · rótulo de estrutura não é título: ele não aparece pro público
RX_ROTULO_ESTRUTURA = re.compile(r'^\s*[`*]*(Frame|Slide|Dia|Peça|Peca|Bloco)\s*[0-9]',
                                 re.I)
# arquivo cujo nome diz que o conteúdo é conversa privada
RX_ARQUIVO_PRIVADO = re.compile(r'caixa|inbox|direct|whatsapp|mensag|call|conversa', re.I)
# vocativo de abertura: "Simone, tudo bem?", "Oi, Fernanda.", "Olá Cláudia"
RX_VOCATIVO = re.compile(
    r'(?:^|[>*\s])(?:(?:[Oo]i|[Oo]l[áa]|[Bb]om dia|[Bb]oa tarde|[Bb]oa noite|[Ff]ala)[,!]?\s+)?'
    r'(?P<nome>[A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ][a-záàâãéêíóôõúüç]{2,})\s*,\s*'
    r'(?=[Tt]udo bem|[Tt]udo certo|[Bb]om dia|[Bb]oa tarde|[Bb]oa noite|vi |eu vi|'
    r'voc[êe]|te |aqui )')
# linha do perfil que carrega o nome do próprio dono ou do negócio dele
RX_LINHA_DONO = re.compile(
    r'^\s*-\s*(nome|negóci|negoci|marca|empresa|dono|dona|quem|autor|especialista)', re.I)
# palavra capitalizada que nunca é nome de pessoa
STOPLIST_NOME = {
    'Janeiro', 'Fevereiro', 'Março', 'Marco', 'Abril', 'Maio', 'Junho', 'Julho',
    'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Segunda', 'Terça',
    'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Sabado', 'Domingo',
    'Studio', 'Base', 'Whatsapp', 'Instagram', 'Reels', 'Stories', 'Direct',
    'Feed', 'Facebook', 'Youtube', 'Tiktok', 'Linkedin', 'Google', 'Gmail',
    'Zoom', 'Drive', 'Notion', 'Canva', 'Pilates', 'Protocolo', 'Programa',
    'Turma', 'Fase', 'Garantia', 'Grupo', 'Bônus', 'Bonus', 'Oferta', 'Prova',
    'Cliente', 'Aluna', 'Aluno', 'Lead', 'Dono', 'Dona', 'Nome', 'Data',
    'Antes', 'Depois', 'Hoje', 'Ontem', 'Agora', 'Talvez', 'Ela', 'Ele',
    'Você', 'Voce', 'Como', 'Quem', 'Onde', 'Isso', 'Este', 'Esta', 'Uma',
    'Duas', 'Três', 'Tres', 'Cinco', 'Cada', 'Todo', 'Toda', 'Sem', 'Com',
    'Nos', 'Nessa', 'Aqui', 'Existe', 'Manda', 'Parou', 'Perguntou', 'Foi',
    'Não', 'Nao', 'Sua', 'Seu', 'Pra', 'Para', 'Segunda',
}
# contexto de pessoa na linha do insumo, sempre ancorado no PRÓPRIO nome
CTX_PESSOA = (
    r'{n}\s*,\s*\d',                                  # "Simone, 51"
    r'{n}\s*,?\s*\d{{1,3}}\s*anos',                   # "Simone 51 anos"
    r'^\s*(?:\d+[.)]\s*)?{n}\s*(?:\([^)]*\))?\s*:',   # "3. Cláudia (aluna):"
    r'{n}\s*:',                                       # "Fernanda: preço?"
    r'@\s*{n}',
    r'{n}\b[^.\n]{{0,40}}\b(?:escreveu|perguntou|mandou|disse|respondeu)',
    r'\b(?:aluna|aluno|cliente|lead|com|de|da|do)\s+{n}\b',
)

# Bastidor: o arquivo que existe pra REGISTRAR a checagem, não pra ser lido pelo
# destinatário. A lista de nomes privados, o porquê de cada pendência e a decisão
# de escopo moram aqui por regra, então cobrar deles o gate da peça pública
# reprovaria justamente a entrega que fez a checagem certa. O RELATO.md entra
# aqui: a régua manda colar nele a saída crua da extração de nomes, e cobrar
# dessa saída o gate da peça pública reprova quem obedeceu.
RX_BASTIDOR = re.compile(r'^(checagem-titulos\.md|RELATO|HANDOFF|handoff|CONSENTIMENTO|'
                         r'NOTAS-DE-ENTREGA|notas-|VEREDITO|LICOES|FUROS|inventario|'
                         r'INVENTARIO)', re.I)

# ── R13 · bastidor mora em conferencia/ ──────────────────────────────────────
# A dona abre a pasta e conta o que não é dela: titulos.txt, teses.txt, um
# nomes.txt de 0 byte, um checagem-titulos.md de 49 KB maior que a entrega
# inteira. Nada disso é entregável, e nada disso responde pergunta dela. A
# partir daqui o bastidor mora numa subpasta com nome próprio, e a raiz fica
# com o entregável e o handoff.
SUBPASTA_BASTIDOR = 'conferencia'
RX_BASTIDOR_DE_ARQUIVO = re.compile(
    r'^(?:titulos\.txt|teses\.txt|nomes\.txt|matriz-pares[\w.\-]*|'
    r'checar-passo1[\w.\-]*|checagem-raw[\w.\-]*|conferir[\w.\-]*\.txt|'
    r'passo1[\w.\-]*|teste-[\w.\-]*|extracted[\w.\-]*|copy-em-analise[\w.\-]*|'
    r'checagem-titulos\.md)$', re.I)
# lixo de execução que nunca tem lugar na pasta do dono, nem em conferencia/
RX_LIXO_DE_MAQUINA = re.compile(r'^(?:[\w.\-]+\.log|__pycache__)$', re.I)


# ── R13 · o resumo que abre o relato ─────────────────────────────────────────
# "O relato tem que começar pelo que eu recebi e o que eu faço agora." Hoje ele
# abre com a lista de arquivos que a skill leu, com head -5 e md5. As três
# primeiras linhas passam a ser do dono.
RX_RESUMO_PRONTO = re.compile(r'^\s*[*_`>#\-\s]*Pronto\s*:\s*\S', re.I)
RX_RESUMO_ABRA = re.compile(r'^\s*[*_`>#\-\s]*Abra primeiro\s*:\s*\S', re.I)
RX_RESUMO_FALTA = re.compile(r'^\s*[*_`>#\-\s]*Falta voc[êe] responder\s*:\s*\S', re.I)
# a última seção do relato, com as pendências escritas como pergunta
RX_SECAO_PERGUNTAS = re.compile(r'^\s*#{1,6}\s*\**\s*Perguntas pra voc[êe]\b', re.I)
RX_TEM_PERGUNTA = re.compile(r'\?')
# ── R13 · comando entregue ao dono ───────────────────────────────────────────
# "Nunca me mandar rodar comando." Ou a skill executa, ou ela diz o que pedir e
# pra quem. Fora de bloco cercado, a linha que manda o dono rodar sai por exit.
RX_COMANDO_PRO_DONO = re.compile(
    r'\b(?:rode|execute|no terminal)\b|(?:^|[\s`(])(?:npx |python3 |bash |gog |wrangler)',
    re.I)
RX_CERCA_SIMPLES = re.compile(r'^\s*(?:```|~~~)')
# ── R13 · jargão interno sem tradução ────────────────────────────────────────
# Lista fechada do que a dona leu e não entendeu. Cada ocorrência num texto que
# ela lê pede a glosa de até 4 palavras ao lado, entre parênteses, travessão de
# hífen ou vírgula. Sem glosa, o termo sai do texto dela.
RX_JARGAO = re.compile(
    r'\b(?:Fase [0-9]|Tipo [0-9]|Ação [0-9]|Acao [0-9]|molde de antítese|'
    r'molde de antitese|RASTREIO QUEBRADO|camada C[0-9]|crivo clínico|'
    r'crivo clinico|read-caption|gatilho R[0-9]|R[1-7]\b|PUV|touchstone)')
# a glosa: até 4 palavras logo ao lado do termo, entre parênteses ou após vírgula
RX_GLOSA = re.compile(r'^\s*[(,:]\s*[^()\n]{1,60}?\)?')


def tem_glosa(linha, fim):
    """Depois do termo vem uma glosa de até 4 palavras? Só isso o dono lê."""
    resto = linha[fim:]
    m = RX_GLOSA.match(resto)
    if not m:
        return False
    dentro = m.group(0).strip(' (),:').strip()
    if not dentro:
        return False
    return 1 <= len(dentro.split()) <= 4


def caminho_de_bastidor(base, nome):
    """O arquivo de bastidor mora em `conferencia/`; a raiz vale por compatibilidade.

    Grava sempre na subpasta. Lê da subpasta primeiro e cai pra raiz quando a
    entrega é de antes desta regra, avisando onde achou.
    """
    base = Path(base)
    novo = base / SUBPASTA_BASTIDOR / nome
    if novo.exists():
        return novo
    velho = base / nome
    if velho.exists():
        return velho
    return novo


def bastidor_na_raiz(base):
    """Os arquivos de bastidor que ainda moram na raiz da pasta do dono."""
    base = Path(base)
    return sorted(f.name for f in base.iterdir()
                  if f.is_file() and RX_BASTIDOR_DE_ARQUIVO.match(f.name))


def lixo_na_raiz(base):
    """Log e cache de execução na raiz: o dono abre a pasta e vê 2 MB de assombro."""
    base = Path(base)
    return sorted(f.name for f in base.iterdir() if RX_LIXO_DE_MAQUINA.match(f.name))


def garantir_conferencia(base):
    """Cria `conferencia/` na pasta de saída e devolve o caminho."""
    alvo = Path(base) / SUBPASTA_BASTIDOR
    alvo.mkdir(parents=True, exist_ok=True)
    return alvo


def md_da_entrega(base):
    """Todo .md da entrega: a raiz que o dono lê mais o bastidor em conferencia/."""
    base = Path(base)
    return sorted(base.glob('*.md')) + sorted((base / SUBPASTA_BASTIDOR).glob('*.md'))


def relatos_da_pasta(base):
    """O RELATO.md e todo HANDOFF* da raiz: os arquivos que o dono lê primeiro."""
    base = Path(base)
    achados = []
    for f in sorted(base.glob('*.md')):
        nome = f.name
        if nome == 'RELATO.md' or re.match(r'^HANDOFF', nome, re.I):
            achados.append(f)
    return achados


def resumo_pro_dono(arquivo):
    """As 3 linhas do dono abrem o relato, antes de qualquer outra coisa?

    Devolve (tem_resumo, motivo). Cabeçalho de título e linha em branco passam;
    qualquer outra linha de conteúdo antes das três reprova, porque o dono lê a
    primeira coisa que aparece e é ela que precisa responder o que ele recebeu.
    """
    linhas = linhas_de(arquivo)
    vistas = []
    for l in linhas:
        crua = l.strip()
        if not crua:
            continue
        if crua.startswith('#') and not (RX_RESUMO_PRONTO.match(l)
                                         or RX_RESUMO_ABRA.match(l)
                                         or RX_RESUMO_FALTA.match(l)):
            # o H1 do documento pode abrir; qualquer outro cabeçalho já é seção
            if len(vistas) == 0 and crua.startswith('# '):
                continue
            return False, 'o relato entra em seção antes das 3 linhas do dono'
        if RX_RESUMO_PRONTO.match(l):
            vistas.append('Pronto')
        elif RX_RESUMO_ABRA.match(l):
            vistas.append('Abra primeiro')
        elif RX_RESUMO_FALTA.match(l):
            vistas.append('Falta você responder')
        else:
            faltam = [x for x in ('Pronto', 'Abra primeiro', 'Falta você responder')
                      if x not in vistas]
            return False, f'faltam as linhas: {", ".join(faltam)}'
        if len(vistas) == 3:
            return True, ''
    faltam = [x for x in ('Pronto', 'Abra primeiro', 'Falta você responder')
              if x not in vistas]
    return False, f'faltam as linhas: {", ".join(faltam)}'


def secao_de_perguntas(arquivo):
    """A última seção se chama `Perguntas pra você` e traz pergunta escrita?

    Devolve (achou, perguntas), com as perguntas de dentro dela.
    """
    linhas = linhas_de(arquivo)
    inicio = None
    for i, l in enumerate(linhas):
        if RX_SECAO_PERGUNTAS.match(l):
            inicio = i
    if inicio is None:
        return False, []
    nivel = len(re.match(r'^\s*(#{1,6})', linhas[inicio]).group(1))
    perguntas = []
    for l in linhas[inicio + 1:]:
        m = re.match(r'^\s*(#{1,6})\s', l)
        if m and len(m.group(1)) <= nivel:
            break
        if RX_TEM_PERGUNTA.search(l):
            perguntas.append(l.strip()[:120])
    return True, perguntas


def comandos_pro_dono(arquivo):
    """Linha que manda o dono rodar comando, fora de bloco cercado."""
    achados, dentro = [], False
    for n, l in enumerate(linhas_de(arquivo), 1):
        if RX_CERCA_SIMPLES.match(l):
            dentro = not dentro
            continue
        if dentro:
            continue
        if RX_COMANDO_PRO_DONO.search(l):
            achados.append((n, l.strip()[:140]))
    return achados


# PENDENTE-r14 · PEDIDO-PARA-QUEM-PUBLICA*.md é endereçado a um terceiro técnico
# (quem publica, quem tem acesso), não ao dono. Comando DENTRO dele é o passo que
# essa pessoa executa, e fica isento do gate "comando entregue ao dono" DESDE QUE
# o arquivo abra com 3 linhas pro dono (o que é · pra quem mandar · o que essa
# pessoa vai fazer) e o RELATO não contenha comando.
RX_ARQUIVO_PARA_TERCEIRO = re.compile(r'PEDIDO-PARA-QUEM-PUBLICA', re.I)
RX_CAB_PARA_TERCEIRO = (
    re.compile(r'o que [ée] este arquivo', re.I),
    re.compile(r'pra quem (mandar|enviar)', re.I),
    re.compile(r'o que essa pessoa vai fazer', re.I),
)


def pedido_para_terceiro_valido(arquivo):
    """True quando o arquivo é um PEDIDO-PARA-QUEM-PUBLICA que abre com as 3
    linhas pro dono. Só aí os comandos DENTRO dele são isentos."""
    if not RX_ARQUIVO_PARA_TERCEIRO.search(Path(arquivo).name):
        return False
    cabecalho = '\n'.join(linhas_de(arquivo)[:15])
    return all(rx.search(cabecalho) for rx in RX_CAB_PARA_TERCEIRO)


def jargao_sem_glosa(arquivo):
    """Termo interno da lista fechada sem a glosa de até 4 palavras ao lado."""
    achados, dentro = [], False
    for n, l in enumerate(linhas_de(arquivo), 1):
        if RX_CERCA_SIMPLES.match(l):
            dentro = not dentro
            continue
        if dentro:
            continue
        for m in RX_JARGAO.finditer(l):
            if not tem_glosa(l, m.end()):
                achados.append((n, m.group(0), l.strip()[:140]))
    return achados


# ── R13 · arquivo INTERNO do dono, onde o nome fica ──────────────────────────
# "Nome de pessoa fica no arquivo que eu vou usar." A triagem trocou as leads
# por `contato 1` e `contato A`, e pra responder no WhatsApp a dona teve que
# abrir um segundo arquivo e cruzar número com nome. A anonimização é da peça
# PÚBLICA (post, carta, landing, anúncio, stories, reel, e-mail em massa); a
# fila do dia, o dossiê da call, a lista de prospecção, o caso de reclamação e o
# relatório são ferramenta de trabalho e levam o nome.
RX_ARQUIVO_INTERNO = re.compile(
    r'fila|dossi[êe]|prospec|triagem|relat[óo]rio|relatorio|'
    r'diagn[óo]stico|diagnostico|lista-de|call-prep|call_prep|briefing|'
    r'atendimento|pipeline|crm|agenda|checklist|plano-de|plano_de|'
    r'preparo|resumo-de|contatos?|casos-|casos_', re.I)
# a peça PÚBLICA por nome de arquivo: é dela que a régua de nome cobra
RX_ARQUIVO_PUBLICO = re.compile(
    r'post|carrossel|carta|landing|pagina|página|anuncio|anúncio|stories|story|'
    r'reel|reels|email|e-mail|newsletter|legenda|caption|headline|capa|'
    r'isca|vsl|webinar|slide|deck|apostila|artigo|blog', re.I)
# a seção que declara o uso interno dentro de um arquivo misto
RX_SECAO_INTERNA = re.compile(
    r'^\s*#{1,6}\s*\**\s*(?:fila|dossi[êe]|uso interno|bastidor|'
    r'prospec\w*|triagem|para o dono|notas do dono)\b', re.I)


def arquivo_interno_do_dono(caminho):
    """O arquivo é ferramenta do dono, e não peça que vai ao público?

    A classificação sai do nome do arquivo, e a peça pública ganha do interno
    quando os dois padrões batem: `post-para-fila.md` publica.
    """
    nome = Path(caminho).name
    if RX_ARQUIVO_PUBLICO.search(nome):
        return False
    return bool(RX_ARQUIVO_INTERNO.search(nome))


def publicas(pecas):
    """As peças que o destinatário lê. Bastidor fica de fora dos gates públicos.

    R13 · o arquivo INTERNO do dono também: nele o nome mora por função, e
    apagá-lo obriga o dono a cruzar dois arquivos numa manhã corrida.
    """
    return [f for f in pecas
            if not RX_BASTIDOR.match(Path(f).name)
            and not arquivo_interno_do_dono(f)]


def bastidor_na_peca_publica(pecas):
    """consertos 4, 5, r14b-1 · o bastidor que vazou pro arquivo que o dono abre.

    A tabela de destino de dado, a tabela de veredito do gate, a contagem
    desdobrada `dados no perfil` e o diário `saída literal:` são auto-avaliação
    da máquina e diário de trabalho: moram em conferencia/, nunca na peça que o
    dono lê. Roda só sobre a peça pública (não bastidor, não documento
    operacional, não arquivo interno): num handoff a tabela de destino é a
    ferramenta de trabalho e fica.
    """
    achados = []
    for f in pecas:
        nome = Path(f).name
        if (RX_BASTIDOR.match(nome) or RX_ARQUIVO_OPERACIONAL.search(nome)
                or arquivo_interno_do_dono(f)):
            continue
        dentro = False
        for n, l in enumerate(linhas_de(f), 1):
            if RX_CERCA.match(l):
                dentro = not dentro
                continue
            if dentro:
                continue
            if RX_LINHA_INVENT_DESTINO.match(l):
                achados.append((nome, n, 'tabela de destino de dados', l.strip()[:100]))
            elif RX_LINHA_VEREDITO.search(l):
                achados.append((nome, n, 'tabela de veredito do gate', l.strip()[:100]))
            elif RX_LINHA_DADOS_NO_PERFIL.search(l):
                achados.append((nome, n, 'contagem de dados do gate', l.strip()[:100]))
            elif RX_LINHA_PREFLIGHT.search(l):
                achados.append((nome, n, 'diário de trabalho (saída literal)', l.strip()[:100]))
    return achados


# ── (b)3 · a prova de cumprimento não é a infração ───────────────────────────
# O gate de nome reprovou uma entrega por `Fernanda` num arquivo onde o CSV
# público devolve `grep -c` zero: o nome só existia na lista de candidatos que
# o motor extraiu e DESCARTOU, e no inventário como item descartado. Punir a
# documentação do descarte ensina o motor a não documentar. Daqui pra frente a
# linha de bastidor dentro de um arquivo de planejamento sai do universo do
# gate público, do mesmo modo que o arquivo de bastidor inteiro já saía.
RX_LINHA_BASTIDOR = re.compile(
    r'candidat|descartad|proibid|não usar|nao usar|lista de nomes|nomes\.txt|grep -', re.I)
# arquivo de planejamento e documento operacional: o nome do arquivo já diz que
# ele registra a decisão, não a copy que o lead lê
RX_ARQUIVO_OPERACIONAL = re.compile(
    r'operacao|operação|prompt|relatorio|relatório|wiki|planejamento|HANDOFF|'
    r'checagem|notas|inventario|inventário|FUROS|spec|PROVA|'
    r'PEDIDO-PARA-QUEM-PUBLICA|PEDIDO-DE-IMAGEM', re.I)
# consertos 4, 5 e r14b-1 · bastidor que vazou pro arquivo que o dono ABRE.
# A tabela de destino de dado ("Dados fornecidos" com colunas usado/descartado),
# a tabela de veredito do gate, a linha `dados no perfil: N · usados · descartados`
# fora da forma curta, e o diário "Pré-flight de CTA, saída literal:" são
# auto-avaliação e diário de trabalho, nunca a peça. Moram em conferencia/.
RX_LINHA_INVENT_DESTINO = re.compile(
    r'^\s*\|.*\|\s*(?:usado|descartado)', re.I)
RX_LINHA_VEREDITO = re.compile(r'\bVEREDITO\b', re.I)
RX_LINHA_DADOS_NO_PERFIL = re.compile(
    r'dados no perfil\s*:\s*\d+\s*[·|].*(?:usad|descartad)', re.I)
RX_LINHA_PREFLIGHT = re.compile(
    r'(?:pr[ée][- ]?flight|saída literal|saida literal)\b.*:', re.I)


def linhas_publicas_do_arquivo(arquivo):
    """(b)3 · o texto do arquivo sem as linhas de bastidor e sem bloco de código.

    Devolve {número da linha: texto}. Só as linhas que o destinatário lê.
    Num arquivo de planejamento, a linha de bastidor (candidato, descarte,
    proibição, comando de grep) sai do universo. Bloco cercado de código sai em
    todo arquivo: comando colado é prova, não é copy.
    """
    operacional = bool(RX_ARQUIVO_OPERACIONAL.search(Path(arquivo).name))
    vivas, dentro_de_cerca, dentro_de_secao_interna = {}, False, False
    for n, linha in enumerate(linhas_de(arquivo), 1):
        if RX_CERCA.match(linha):
            dentro_de_cerca = not dentro_de_cerca
            continue
        if dentro_de_cerca:
            continue
        # R13 · seção declarada de uso interno (fila, dossiê, prospecção) dentro
        # de um arquivo misto: lá o nome mora por função, e sai da régua pública
        if re.match(r'^\s*#{1,6}\s', linha):
            dentro_de_secao_interna = bool(RX_SECAO_INTERNA.match(linha))
        if dentro_de_secao_interna:
            continue
        if operacional and RX_LINHA_BASTIDOR.search(linha):
            continue
        vivas[n] = linha
    return vivas


def texto_publico(arquivo):
    """(b)3 · o arquivo como o destinatário o lê, uma linha por linha viva."""
    return '\n'.join(linhas_publicas_do_arquivo(arquivo).values())


# ── (b)7 · peça que não é markdown ───────────────────────────────────────────
# Zero impresso por ausência de varredura é a pior saída possível: o motor lê
# `títulos na peça: 0` e conclui que a peça não tem título, quando o script é
# que olhou pro lugar errado. Duas pastas de soft-sistema fecharam assim, com
# H1 e H2 reais dentro do .html. Daqui pra frente o universo soma .md, .html e
# .pptx, e a ausência dos três sai escrita, nunca como zero.
RX_H_HTML = re.compile(r'<h[123][^>]*>(.*?)</h[123]>', re.I | re.S)
RX_TITLE_HTML = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
RX_TAG = re.compile(r'<[^>]+>')
RX_SLIDE_XML = re.compile(r'^ppt/slides/slide\d+\.xml$')
RX_ACENTO = re.compile(r'[áéíóúâêôãõçÁÉÍÓÚÂÊÔÃÕÇàÀ]')


def _texto_limpo(bruto):
    return RX_TAG.sub(' ', bruto).replace('&nbsp;', ' ').strip()


def titulos_de_html(arquivo):
    """<title>, <h1>, <h2> e <h3> do arquivo, na ordem em que aparecem."""
    txt = ler(arquivo)
    achados = []
    for m in RX_TITLE_HTML.finditer(txt):
        t = _texto_limpo(m.group(1))
        if t:
            achados.append(t)
    for m in RX_H_HTML.finditer(txt):
        t = _texto_limpo(m.group(1))
        if t:
            achados.append(t)
    return achados


def slides_do_pptx(arquivo):
    """Os slides do .pptx, cada um como (título, texto inteiro).

    O título é o primeiro `<a:t>` do primeiro shape do slide, que é onde o
    layout põe a manchete com ou sem placeholder de título declarado. O texto
    inteiro serve pro lint e pra contagem de acentos.
    """
    import zipfile
    slides = []
    try:
        z = zipfile.ZipFile(str(arquivo))
    except (OSError, zipfile.BadZipFile):
        return slides
    with z:
        for nome in sorted(z.namelist(),
                           key=lambda n: (len(n), n)):
            if not RX_SLIDE_XML.match(nome):
                continue
            try:
                xml = z.read(nome).decode('utf-8', errors='replace')
            except OSError:
                continue
            shapes = re.split(r'<p:sp>', xml)[1:]
            titulo = ''
            for sh in shapes:
                ts = [_texto_limpo(t) for t in re.findall(r'<a:t>(.*?)</a:t>', sh, re.S)]
                ts = [t for t in ts if t]
                if ts:
                    titulo = ts[0]
                    break
            corpo = ' '.join(_texto_limpo(t)
                             for t in re.findall(r'<a:t>(.*?)</a:t>', xml, re.S))
            slides.append((titulo, corpo.strip()))
    return slides


def texto_do_pptx(arquivo):
    """Todo o texto do deck, um slide por linha."""
    return '\n'.join(corpo for _, corpo in slides_do_pptx(arquivo) if corpo)


RX_COL_TEXTO_TELA = re.compile(r'texto\s+na\s+tela', re.I)
RX_CELULA_VAZIA_TELA = re.compile(r'^\(?\s*(?:nada|vazio|sem texto|-|—)?\s*\)?$', re.I)


def texto_na_tela_do_roteiro(arquivo):
    """conserto 4 (r14a) · as células da coluna TEXTO NA TELA de um roteiro de reel.

    A tabela do reel tem colunas Tempo/Espinha/FALAR/MOSTRAR/TEXTO NA TELA. O que
    aparece na tela é título que o público lê, e entra no universo da régua sem
    virar cabeçalho `##`. Célula vazia ("(nada)") não conta.
    """
    linhas = linhas_de(arquivo)
    achados, col = [], None
    for l in linhas:
        if not RX_LINHA_TABELA.match(l) or RX_SEPARADOR_TABELA.match(l):
            continue
        celulas = [c.strip() for c in l.strip().strip('|').split('|')]
        if col is None:
            for i, c in enumerate(celulas):
                if RX_COL_TEXTO_TELA.search(c):
                    col = i
                    break
            continue  # a linha do cabeçalho não é título
        if col < len(celulas):
            val = celulas[col]
            if val and not RX_CELULA_VAZIA_TELA.match(val):
                achados.append(val)
    # a legenda de publicação também é texto que o público lê, e entra no
    # universo do reel do mesmo modo (a régua lista TEXTO NA TELA e a legenda)
    if col is not None:
        for l in linhas:
            m = re.match(r'^\s*\**\s*Legenda\s*:\s*\**\s*(\S.*)$', l, re.I)
            if m:
                achados.append(m.group(1).strip())
    return achados


def titulos_de_md(arquivo):
    cabecalhos = [l for l in linhas_de(arquivo)
                  if RX_TITULO_PECA.match(l) and not RX_ROTULO_SECAO.match(l)]
    # conserto 4 (r14a) · no reel o universo de título mora na coluna TEXTO NA
    # TELA do roteiro, não em cabeçalhos `##` soltos. Depois de tirar o bastidor,
    # o reel fica com 1 H1 e a tabela; a régua conta o H1 mais cada célula de
    # texto na tela, que é o que o público lê na tela.
    return cabecalhos + texto_na_tela_do_roteiro(arquivo)


def rotulos_no_miolo(pecas, texto_fonte=None):
    """C1(a)1 e (a)2 · cabeçalho de peça pública que é rótulo, não tese.

    A isenção de rótulo estrutural virou a porta de saída do gate: renomear a
    etapa pra `## P3` troca a qualidade da peça pela facilidade da régua. Aqui
    o cabeçalho com padrão de rótulo entra no universo e sai impresso, um por
    linha. Só FAQ, Bio, Índice, Sumário, Referências e Anexo continuam isentos,
    e documento operacional inteiro fica de fora pelo nome do arquivo.

    conserto 7 (r14a) · quando a skill converte uma peça de outra skill e passa
    `--fonte`, o cabeçalho cujo texto veio idêntico da fonte não é rótulo
    introduzido por esta conversão: sai como `achado na fonte`, igual o marcador
    longo, o nome e o número de terceiro já saem. Um H1 herdado (`# Régua de
    nutrição ...`) não vira reprova de quem só mudou o formato.
    """
    achados = []
    for f in pecas:
        if RX_ARQUIVO_OPERACIONAL.search(Path(f).name) or RX_BASTIDOR.match(Path(f).name):
            continue
        dentro = False
        for n, l in enumerate(linhas_de(f), 1):
            if RX_CERCA.match(l):
                dentro = not dentro
                continue
            if dentro or not l.startswith('#'):
                continue
            if RX_ROTULO_ISENTO.match(l):
                continue
            if RX_ROTULO_NO_MIOLO.match(l):
                miolo = l.lstrip('#').strip()
                if texto_fonte and miolo and miolo in texto_fonte:
                    achados.append((Path(f).name, n, l.strip()[:160], True))
                else:
                    achados.append((Path(f).name, n, l.strip()[:160], False))
    return achados


def sem_h1(pecas):
    """C1(b)4 · `.md` de peça pública sem nenhuma linha `^# `.

    O conserto anterior mandou trocar o H1 rótulo por tese, e o motor removeu o
    H1. Remover não é alternativa a escrever bem: a peça sem H1 reprova.
    """
    faltando = []
    for f in pecas:
        if RX_ARQUIVO_OPERACIONAL.search(Path(f).name) or RX_BASTIDOR.match(Path(f).name):
            continue
        if not any(l.startswith('# ') for l in linhas_de(f)):
            faltando.append(Path(f).name)
    return faltando


def numeros_marcados_no_perfil(perfil):
    """B(a)1 · os números que no perfil moram na mesma linha de um marcador.

    Dois motores publicaram `seis semanas` sobre um dado que o perfil marca
    `[A CONFIRMAR: número exato]`, um com a ressalva ao lado e outro sem. A
    ressalva não conserta o número: o leitor lê o número primeiro.
    """
    if not perfil or not Path(perfil).exists():
        return []
    marcados = []
    for n, l in enumerate(linhas_de(perfil), 1):
        if not RX_MARCADOR.search(l):
            continue
        # conserto (r14a) · o marcador qualifica só o número da SUA cláusula, não
        # todo número da linha. `63 alunas em 2 anos; ... em 6 semanas [A CONFIRMAR]`
        # marca "6 semanas", não "63 alunas" nem "2 anos", que são fatos
        # confirmados na mesma linha. Recorta a cláusula do marcador entre `;`, `·`
        # ou `.`; sem separador, a linha inteira vale, como antes.
        segmentos = re.split(r'\s*[;·]\s*|\.\s+', l)
        clausula = next((s for s in segmentos if RX_MARCADOR.search(s)), l)
        fora = RX_MARCADOR.sub(' ', clausula)
        for m in RX_NUM_COM_UNIDADE.finditer(fora):
            valor = m.group('num')
            if len(valor.strip('0')) == 0:
                continue
            unidade = (m.group('pos') or '').strip()
            moeda = (m.group('pre') or '').strip()
            # PENDENTE-r14: dígito solto de 1 a 2 casas, sem unidade nem moeda,
            # nunca conta. Só o número COM o contexto que o perfil lhe dá reprova.
            if not unidade and not moeda:
                if len(valor.replace('.', '').replace(',', '')) <= 2:
                    continue
            # token que o consumidor vai procurar na peça, com a unidade colada
            if moeda:
                token = f'{moeda} {valor}'.strip()
            elif unidade:
                token = f'{valor} {unidade}'
            else:
                token = valor
            marcados.append((token, valor, unidade, moeda, n, l.strip()[:140]))
    return marcados


def universo_de_titulos(base, pecas_md):
    """(b)7 · o universo somado das três formas de peça, com a fonte de cada um.

    Devolve (total, detalhe, motivo). `motivo` só vem preenchido quando não há
    nenhuma peça varrível, e nesse caso o chamador imprime a ausência em vez de
    imprimir zero.
    """
    base = Path(base)
    pecas_md = list(pecas_md)
    # (b)6 · o universo é de título de COPY. Cabeçalho markdown de documento
    # operacional (planejamento, prompt, relatório, wiki, spec, notas) é
    # estrutura de trabalho: dois exit 1 de uma rodada só vieram do script
    # somando esses cabeçalhos ao lote de títulos que a régua cobre. A exceção
    # é a pasta que SÓ tem documento operacional em markdown: aí eles são a
    # peça que a skill entrega, e tirá-los trocaria um número inflado por zero.
    operacionais = [f for f in pecas_md if RX_ARQUIVO_OPERACIONAL.search(f.name)]
    fora = operacionais if len(operacionais) < len(pecas_md) else []
    detalhe, total = [], 0
    for f in pecas_md:
        if f in fora:
            detalhe.append((f.name, 'documento operacional (fora do universo)', 0))
            continue
        n = len(titulos_de_md(f))
        detalhe.append((f.name, 'md', n))
        total += n
    htmls = sorted(f for f in base.glob('*.html') if not RX_BASTIDOR.match(f.name))
    for f in htmls:
        n = len(titulos_de_html(f))
        detalhe.append((f.name, 'html', n))
        total += n
    pptxs = sorted(f for f in base.glob('*.pptx') if not RX_BASTIDOR.match(f.name))
    for f in pptxs:
        n = sum(1 for t, _ in slides_do_pptx(f) if t)
        detalhe.append((f.name, 'pptx', n))
        total += n
    motivo = ''
    if not (list(pecas_md) or htmls or pptxs):
        motivo = 'nenhum .md de peça, nenhum .html e nenhum .pptx na pasta'
    return total, detalhe, motivo


# conserto 6 (r14a) · quando a peça sai em 2 temas (claro/escuro, light/dark), o
# mesmo card é renderizado uma vez por tema. O universo de copy é UM por card, não
# um por PNG: um `slide-03.png` em claro/ e outro em escuro/ são a mesma copy. O
# segmento de tema sai da identidade do card, e temas paralelos contam uma vez.
RX_TEMA = re.compile(r'^(?:claro|escuro|light|dark|tema-[\w-]+)$', re.I)


def _card_id(rel):
    """A identidade do card, sem o segmento de tema, pra colapsar claro/escuro."""
    partes = [p for p in Path(rel).parts if not RX_TEMA.match(p)]
    return '/'.join(partes)


def peca_sai_em_temas(base):
    """conserto 6 (r14a) · a pasta tem o mesmo card renderizado em 2+ temas?

    Só aí o universo nasce do titulos.txt (um por card): a peça em tema único
    com uma copy .md legível segue medindo o universo pela peça, como sempre.
    """
    base = Path(base)
    temas = set()
    for padrao in ('**/slide-*.png', '**/card-*.png'):
        for f in base.glob(padrao):
            if f.name.startswith('_'):
                continue
            for parte in f.relative_to(base).parts:
                if RX_TEMA.match(parte):
                    temas.add(parte.lower())
    return len(temas) >= 2


def renders_na_pasta(base):
    """R12C2(b)5 · os CARDS renderizados da pasta, subpasta inclusa, um por card.

    O `--conferir` varre o topo da pasta, e a peça publicada costuma morar em
    `<slug>/_fonte/*.html` ou `<slug>/slide-NN.png`. Cada card aqui é uma tela
    que vai ao público e que o universo de títulos tem que cobrir. Quando a peça
    sai em 2 temas, o mesmo card em claro/ e em escuro/ conta uma vez só: o
    universo é de COPY, e a copy não dobra com o tema.
    """
    base = Path(base)
    por_card = {}
    for padrao in ('**/slide-*.png', '**/card-*.png', '**/*.pptx'):
        for f in sorted(base.glob(padrao)):
            if RX_BASTIDOR.match(f.name) or f.name.startswith('_'):
                continue
            rel = str(f.relative_to(base))
            por_card.setdefault(_card_id(rel), rel)
    if not por_card:
        for f in sorted(base.glob('*/**/*.html')):
            if RX_BASTIDOR.match(f.name) or f.name.startswith('_'):
                continue
            rel = str(f.relative_to(base))
            por_card.setdefault(_card_id(rel), rel)
    return [por_card[k] for k in sorted(por_card)]


def titulos_da_copy_fonte(base):
    """R12C2(b)5 · o universo nasce do arquivo de copy, nunca da lembrança.

    Quando a pasta tem copy ou manifesto, os títulos saem dele por comando e
    viram as linhas de `titulos.txt`, uma por peça, na ordem dos arquivos.
    """
    base = Path(base)
    extraidos = []
    for f in sorted(base.glob('*.md')):
        if RX_BASTIDOR.match(f.name):
            continue
        extraidos += titulos_de_md(f)
    if extraidos:
        return extraidos
    # a copy da peça renderizada costuma morar no HTML da subpasta: o conserto
    # é apontar o gate pra ela, nunca reduzir o universo ao topo da pasta
    for f in sorted(base.glob('**/*.html')):
        if f.name.startswith('_'):
            continue
        extraidos += titulos_de_html(f) or copy_do_card(f)
    return extraidos


def copy_do_card(arquivo):
    """R12C2(b)5 · a copy que virou pixel, extraída do HTML do card.

    O card renderizado não tem <h1>: a linha que o leitor lê mora no bloco de
    corpo. Ela é o título daquele card pro universo da régua.
    """
    try:
        bruto = ler(arquivo)
    except OSError:
        return []
    achados = []
    for m in re.finditer(r'<div[^>]*class="[^"]*\bcorpo\b[^"]*"[^>]*>(.*?)</div>',
                         bruto, re.S | re.I):
        txt = _texto_limpo(m.group(1))
        if txt:
            achados.append(txt[:160])
    return achados


def linha_do_universo(detalhe):
    """(b)6 · o universo declarado: o que foi contado e o que ficou de fora.

    A linha existe pra que o dono leia, sem abrir o terminal, QUAIS arquivos
    produziram o número de títulos. Documento operacional aparece marcado, e
    não soma: o universo da régua é de título de copy.
    """
    contados = [n for n, tipo, _ in detalhe if 'documento operacional' not in tipo]
    fora = [n for n, tipo, _ in detalhe if 'documento operacional' in tipo]
    txt = f'universo: {", ".join(contados) if contados else "nenhum arquivo de copy"}'
    if fora:
        txt += f' · fora do universo (documento operacional): {", ".join(fora)}'
    return txt


# ── marcador tem tamanho ─────────────────────────────────────────────────────
TETO_PALAVRAS_MARCADOR = 6
# (b)9 · manchete acima disto sai como alerta ao dono, jamais como falha
TETO_ALTURA_MANCHETE = 45

# ── número de terceiro ───────────────────────────────────────────────────────
RX_VALOR = re.compile(r'R\$|%')
RX_TERCEIRO = re.compile(r'concorrente|mercado|referência|referencia|cobra|'
                         r'preço de|preco de|média de|media de', re.I)
RX_URL_COMPLETA = re.compile(r'url:\s*https://', re.I)
RX_CONSULTADO = re.compile(r'consultado em\s*:', re.I)
RX_TRECHO_LITERAL = re.compile(r'trecho\s*:\s*["“]')

# ── afirmação de verificação sem saída crua ──────────────────────────────────
RX_AFIRMA_VERIF = re.compile(r'\b(confirmei|checado|medi|confere|verificado|conferido)\b', re.I)
RX_CERCA = re.compile(r'^\s*```')

PLACEHOLDER = '<preencher>'
# (b)6 · mensagem de ajuda do próprio script no lugar do número. A ajuda ensina
# a rodar; ela nunca é o resultado de ter rodado, então o campo conta como não
# preenchido e o --conferir sai com exit 1.
RX_AJUDA_NO_FECHO = re.compile(
    r'^(?:sem\s+--|<preencher>|rode de novo|salve\s)'
    r'|\brode de novo\b|\bnão informad|\bnao informad',
    re.IGNORECASE)
# R12C2(b)9 · a lista de saídas PRÓPRIAS do gate: o texto que o script imprime
# por falta de flag. Ele nunca conta como campo com instrução no lugar do
# número, porque quem colou a saída do gate anterior obedeceu a régua da época.
# Cada linha aqui reprova pelo motivo REAL (arquivo ausente, flag que o gate
# de nome exige), no ponto do --conferir que cuida daquele número.
RX_SAIDA_PROPRIA_DO_GATE = re.compile(
    r'^\s*[-*•]?\s*[`*]*(?:'
    r'ressalvas na peça\s*:\s*não informada'
    r'|teses distintas\s*:\s*0\s*\(teses\.txt ausente\)'
    r'|teses distintas\s*:\s*sem\s+--teses'
    r'|campos no perfil\s*:\s*sem\s+--perfil'
    r'|nomes candidatos achados pelo script\s*:\s*sem\s+--insumos'
    r'|automação declarada no perfil\s*:\s*sem\s+--perfil'
    r'|palavra-chave\s*:\s*sem\s+--insumos'
    r'|verifica[çc][ãa]o de aspa\s*:\s*sem\s+--insumos'
    r')', re.IGNORECASE)
# R12C2(b)9 · o gate novo nunca reprova a linha que o gate velho imprime. Sem
# --ressalva o script deixava `ressalvas na peça: não informada (rode com ...)`,
# e o --conferir batia nessa própria saída como campo com instrução. Agora ele
# detecta a ressalva sozinho e imprime SEMPRE um número.
RX_RESSALVA_NA_PECA = re.compile(
    r'consulte|profissional de sa[úu]de|m[ée]dic|avalia[çc][ãa]o individual|'
    r'n[ãa]o substitui|orienta[çc][ãa]o|acompanhamento profissional', re.I)
# R12C2(b)6 · declarar que o ambiente não tem uma capacidade é uma afirmação
# sobre o mundo, e ela se prova por comando, igual a qualquer outro furo.
RX_AUSENCIA_DE_CAPACIDADE = re.compile(
    r'sem acesso|sem busca|ambiente sem|n[ãa]o tenho acesso|indispon[íi]vel', re.I)
# R12C2(a)2 · a fala que o dono vai gravar é peça pública: o que está na lista
# de falas vira áudio no ar, e o vídeo não tem onde carregar a ressalva.
RX_PECA_DE_GRAVACAO = re.compile(r'^(PEDIDO-DE-GRAVACAO|PEDIDO-DE-GRAVAÇÃO|roteiro|fala)',
                                 re.I)
# universo vazio dispensa a tabela, nunca o fecho: a linha sai com 0 e o motivo
MOTIVO_SEM_TITULO = ' (motivo: a entrega não tem título que dispute a atenção)'


# ── utilidades ───────────────────────────────────────────────────────────────
def ler(p):
    return Path(p).read_text(encoding='utf-8', errors='replace')


def linhas_de(p):
    return ler(p).splitlines()


def carregar_lint(caminho_lint):
    """Importa lint_copy.py do caminho dado, sem depender de estar no sys.path.

    Sem escrever .pyc: um __pycache__ dentro da pasta da skill suja o repo, viaja
    no pacote e ainda faz o md5 do gate divergir de skill pra skill.
    """
    import importlib.util
    anterior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec = importlib.util.spec_from_file_location('lint_copy_local', str(caminho_lint))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = anterior
    return mod


def rodar_lint(mod, texto, origem):
    """Roda o _run do lint capturando a saída. Devolve (exit, saída, n_moldes)."""
    buf = io.StringIO()
    antigo = sys.stdout
    sys.stdout = buf
    try:
        code = mod._run(texto, origem)
    finally:
        sys.stdout = antigo
    saida = buf.getvalue()
    n = len(mod.molde_antitese(texto, origem))
    return code, saida, n


def duas_oracoes(linha):
    """A linha tem duas orações separadas por ponto, a segunda completando a
    primeira? Mecânico: o ponto separa, a segunda abre em maiúscula, e nenhuma
    das duas é abreviação. É o molde que o lint não pega e a régua manda somar."""
    t = linha.strip()
    if not t or t.startswith('|') or t.startswith('#') or t.startswith('```'):
        return False
    t = re.sub(r'^\s*(?:[-*+]|\d+[.)])\s+', '', t)
    t = re.sub(r'^★\s*', '', t)
    m = RX_DUAS_ORACOES.match(t)
    if not m:
        return False
    if RX_ABREV.search(m.group('a') + '.'):
        return False
    return True


def antitese_virgula(linha):
    """A linha é um molde de antítese numa oração só, separado por VÍRGULA +
    negação? "X, não Y" / "X, nunca Y" / "X, e não Y" — a segunda metade nega a
    primeira. É o MESMO contraste do molde "A. B." (ponto), só que com vírgula, e
    a régua manda contar igual. O "não" tem que vir logo depois da vírgula
    (contraste), não no meio de uma oração normal."""
    t = linha.strip()
    if not t or t.startswith('|') or t.startswith('#') or t.startswith('```'):
        return False
    t = re.sub(r'^\s*(?:[-*+]|\d+[.)])\s+', '', t)
    t = re.sub(r'^★\s*', '', t)
    return bool(RX_ANTITESE_VIRGULA.search(t))


def grep_c(padrao, arquivo):
    """grep -c literal, em python (mesmo número, sem depender do binário)."""
    n = 0
    for linha in linhas_de(arquivo):
        if padrao in linha:
            n += 1
    return n


# pasta que não é insumo do dono: saída de rodada, cache, repositório, ambiente.
# Sem esse filtro o grep dos insumos varre a própria entrega e devolve a peça de
# volta como se fosse origem, que é o defeito que o comando existe pra evitar.
IGNORAR_DIR = re.compile(
    r'(^|/)(\.git|__pycache__|node_modules|\.venv|venv|out|out-r\d+|'
    r'dist|build|\.cache|vps-fake)(/|$)')
# extensão que não é texto de insumo
IGNORAR_EXT = {'.mp4', '.mov', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip',
               '.gz', '.tar', '.webp', '.mp3', '.wav', '.ico', '.woff', '.woff2',
               '.pyc', '.so', '.bin'}
LIMITE_ACHADOS = 40


def grep_rn(rx, pasta, limite=LIMITE_ACHADOS):
    """grep -rn de um regex numa pasta de insumos. Devolve [(arquivo, linha, texto)].

    Pula saída de rodada, cache e binário: insumo é o que o dono deu, não o que a
    própria entrega escreveu. O limite existe pra a saída caber no fecho colável.
    """
    achados = []
    base = Path(pasta)
    if not base.exists():
        return achados
    alvos = sorted(base.rglob('*')) if base.is_dir() else [base]
    for f in alvos:
        if not f.is_file():
            continue
        rel = f.relative_to(base).as_posix() if base.is_dir() else f.name
        if IGNORAR_DIR.search('/' + rel) or f.suffix.lower() in IGNORAR_EXT:
            continue
        try:
            conteudo = f.read_text(encoding='utf-8', errors='replace')
        except (OSError, UnicodeError):
            continue
        if '\0' in conteudo[:1024]:
            continue
        for n, linha in enumerate(conteudo.splitlines(), 1):
            if rx.search(linha):
                achados.append((str(f), n, linha.strip()[:300]))
                if len(achados) >= limite:
                    return achados
    return achados


def palavras_de_cta(pecas):
    """As palavras em CAIXA ALTA que aparecem nas linhas de CTA das peças.

    É a palavra que a seguidora vai DIGITAR. Ela tem que existir literal nos
    insumos: quem digita a grafia errada cai em lugar nenhum. Sigla comum
    (CTA, PDF, WhatsApp) fica de fora porque ninguém a digita como gatilho.
    Devolve {palavra: (arquivo, linha, texto)}.
    """
    achadas = {}
    for f in pecas:
        for n, linha in enumerate(linhas_de(f), 1):
            if not RX_CTA.search(linha):
                continue
            for w in RX_CAIXA_ALTA.findall(linha):
                if w.upper() in SIGLAS_COMUNS:
                    continue
                achadas.setdefault(w, (f.name, n, linha.strip()[:200]))
    return achadas


def _norma(s):
    """Normaliza pra comparar aspa com insumo: minúsculas e espaços colapsados.

    O acento fica (o objetivo é substring EXATO, só formatação é perdoada). Aspa
    interna some pra a citação aninhada não quebrar o casamento. Assim uma
    paráfrase que trocou UMA palavra continua reprovando, mas quebra de linha,
    espaço duplo ou maiúscula não geram falso positivo.
    """
    s = s.replace('"', ' ').replace('“', ' ').replace('”', ' ')
    s = s.replace('«', ' ').replace('»', ' ').replace('‘', ' ').replace('’', ' ')
    return re.sub(r'\s+', ' ', s).strip().lower()


def aspas_de_citacao(pecas):
    """As falas ENTRE ASPAS que a peça atribui a uma pessoa (depoimento, verbatim).

    Só a aspa de 15+ caracteres que aparece numa linha com marcador de citação
    ('disse', 'cliente', 'mensagem', nome com idade) ou numa linha logo abaixo
    dele. A headline e a tese da PRÓPRIA peça, que o dono escreve sem citar
    ninguém, ficam de fora: o alvo é a fala apresentada como de outra pessoa.
    Devolve [(arquivo, número da linha, trecho da aspa)].
    """
    achados = []
    for f in publicas(pecas):
        linhas = list(linhas_publicas_do_arquivo(f).items())
        contexto_antes = False
        for idx, (n, linha) in enumerate(linhas):
            aspas = [g for m in RX_ASPA.finditer(linha)
                     for g in m.groups() if g and len(g.strip()) >= TAM_MIN_ASPA]
            marcador_aqui = bool(RX_MARCADOR_CITACAO.search(linha)
                                 or RX_PESSOA_ANTES_ASPA.search(linha))
            if aspas and (marcador_aqui or contexto_antes):
                for trecho in aspas:
                    achados.append((f.name, n, trecho.strip()))
            # um marcador de citação numa linha vale pra ela e pra próxima: o
            # padrão "Ela me mandou isto:" + aspa na linha de baixo é comum
            contexto_antes = marcador_aqui and not aspas
    return achados


def aspa_tem_lastro(trecho, texto_insumos_norma):
    """A aspa é substring literal (normalizada) do texto concatenado dos insumos?"""
    return _norma(trecho) in texto_insumos_norma


def texto_insumos_normalizado(pasta):
    """O texto de todos os arquivos de insumo, concatenado e normalizado uma vez.

    Concatenar antes de normalizar evita reprovar aspa que existe idêntica no
    insumo só porque lá ela está quebrada em duas linhas; a normalização colapsa
    a quebra em espaço, e a busca por substring passa a atravessá-la.
    """
    partes = []
    for f in arquivos_de_insumo(pasta):
        try:
            partes.append(ler(f))
        except OSError:
            continue
    return _norma('\n'.join(partes))


def grep_nwF(nome, arquivo):
    """grep -nwF: palavra inteira, casamento literal."""
    rx = re.compile(r'(?<![0-9A-Za-zÀ-ÿ_])' + re.escape(nome) + r'(?![0-9A-Za-zÀ-ÿ_])')
    return [(n, l.strip()) for n, l in enumerate(linhas_de(arquivo), 1) if rx.search(l)]


def grep_nome_publico(nome, arquivo):
    """(b)2 e (b)3 · o nome na PEÇA PÚBLICA, por nome contido.

    grep -inE "(^|[^a-zà-ú])<nome>([^a-zà-ú]|$)", que é o que a régua manda
    rodar: o teste por string inteira deixou `Paula J.` no elenco passar ao
    lado de `Ana Paula, 40` na caixa de entrada. As linhas de bastidor de um
    arquivo de planejamento e os blocos de código ficam de fora.
    """
    rx = re.compile(r'(^|[^a-zà-ú])' + re.escape(nome) + r'([^a-zà-ú]|$)', re.I)
    return [(n, l.strip()) for n, l in linhas_publicas_do_arquivo(arquivo).items()
            if rx.search(l)]


def variantes_do_nome(nome):
    """(b)2 · o nome e a primeira palavra dele, pra colisão por nome contido.

    `Paula J.` colide com `Ana Paula` porque a primeira palavra é a mesma, e
    quem lê o chat lê o mesmo nome. A primeira palavra entra na busca junto do
    nome inteiro, sem repetir quando o nome tem uma palavra só.
    """
    partes = [p for p in re.split(r'[^0-9A-Za-zÀ-ÿ]+', nome) if len(p) > 2]
    saida = [nome]
    if partes and partes[0] != nome:
        saida.append(partes[0])
    return saida


def posicao_do_marcador(linhas, idx, trecho):
    """Campo ou miolo? Campo = a linha começa com o marcador, ou o marcador é o
    valor inteiro de uma célula de tabela ou de um item de lista, ou a linha mora
    dentro de bloco 'Dados fornecidos' / 'Furos' / 'HANDOFF'. O resto é miolo."""
    linha = linhas[idx]
    nu = linha.strip()
    if nu.startswith(trecho):
        return 'campo'
    if RX_CELULA.match(linha):
        for celula in linha.strip().strip('|').split('|'):
            if celula.strip() == trecho:
                return 'campo'
    if RX_ITEM.match(linha):
        resto = RX_ITEM.sub('', linha).strip()
        if resto == trecho:
            return 'campo'
        # "Campo: [A CONFIRMAR]" ainda é campo: rótulo curto e o marcador no fim
        if resto.endswith(trecho) and ':' in resto[:len(resto) - len(trecho)]:
            rotulo = resto[:len(resto) - len(trecho)].rstrip()
            if rotulo.endswith(':') and len(rotulo.split()) <= 6:
                return 'campo'
    # "Rótulo: [marcador]" em linha solta
    if nu.endswith(trecho) and ':' in nu[:len(nu) - len(trecho)]:
        rotulo = nu[:len(nu) - len(trecho)].rstrip()
        if rotulo.endswith(':') and len(rotulo.split()) <= 6:
            return 'campo'
    # bloco: sobe até o cabeçalho mais próximo
    for j in range(idx, -1, -1):
        anterior = linhas[j]
        if anterior.lstrip().startswith('#') or re.match(r'^\s*\*\*[^*]+\*\*\s*:?\s*$', anterior):
            return 'campo' if RX_BLOCO_CAMPO.search(anterior) else 'miolo'
    return 'miolo'


# ── candidatos a nome de pessoa, sem lista declarada ─────────────────────────
def arquivos_de_insumo(pasta):
    """Os arquivos de texto da pasta de insumos, com o mesmo filtro do grep_rn."""
    base = Path(pasta)
    if not base.exists():
        return []
    if base.is_file():
        return [base]
    achados = []
    for f in sorted(base.rglob('*')):
        if not f.is_file() or f.suffix.lower() in IGNORAR_EXT:
            continue
        if IGNORAR_DIR.search('/' + f.relative_to(base).as_posix()):
            continue
        achados.append(f)
    return achados


def nomes_do_dono(perfil):
    """Os nomes próprios das linhas de identidade do perfil: o dono e o negócio
    dele não são terceiro citado, e citar o próprio dono nunca pede autorização."""
    if not perfil or not Path(perfil).exists():
        return set()
    proprios = set()
    for linha in linhas_de(perfil):
        if RX_LINHA_DONO.match(linha):
            proprios |= set(RX_CAPITALIZADA.findall(linha))
    return proprios


def contexto_de_pessoa(nome, linha):
    """A linha do insumo trata este nome como pessoa? O teste é ancorado no
    próprio nome: 'Simone, 51' e 'Fernanda:' contam, 'perguntar: cardápio' não."""
    n = re.escape(nome)
    return any(re.search(p.format(n=n), linha) for p in CTX_PESSOA)


def destinatarios(pecas):
    """O primeiro nome no vocativo de cada mensagem: 'Simone, tudo bem?', 'Oi,
    Fernanda.', 'Olá Cláudia'. Manter o nome do destinatário é decisão legítima,
    e por isso ele entra na contagem com a marca em vez de sumir dela."""
    achados = set()
    for f in publicas(pecas):
        for linha in linhas_de(f):
            for m in RX_VOCATIVO.finditer(linha):
                nome = m.group('nome')
                if nome and nome not in STOPLIST_NOME:
                    achados.add(nome)
    return achados


def candidatos_a_nome(pecas, pasta_insumos, perfil):
    """Nomes de pessoa que a peça publica sem ninguém ter declarado nomes.txt.

    Candidato é a palavra capitalizada de 3+ letras que aparece na PEÇA e também
    nos insumos em linha de pessoa. Some quem aparece em minúscula em qualquer
    lugar (palavra comum no começo de frase), o dono e o negócio dele, e a
    stoplist. Devolve {nome: {'peca': [...], 'insumo': [...], 'privado': bool,
    'autorizado': bool}}.
    """
    arquivos = arquivos_de_insumo(pasta_insumos)
    texto_insumos = {}
    for f in arquivos:
        try:
            conteudo = f.read_text(encoding='utf-8', errors='replace')
        except (OSError, UnicodeError):
            continue
        if '\0' in conteudo[:1024]:
            continue
        texto_insumos[f] = conteudo

    pecas = publicas(pecas)
    # (b)3 · a varredura roda sobre a PEÇA PÚBLICA: linha de bastidor dentro de
    # arquivo de planejamento e bloco cercado de código ficam de fora, porque
    # são a prova do descarte, nunca a publicação do nome.
    texto_peca = '\n'.join(texto_publico(f) for f in pecas)
    tudo = texto_peca + '\n' + '\n'.join(texto_insumos.values())
    proprios = nomes_do_dono(perfil)

    achados = {}
    for cand in sorted(set(RX_CAPITALIZADA.findall(texto_peca))):
        if cand in STOPLIST_NOME or cand in proprios:
            continue
        minusculo = cand[0].lower() + cand[1:]
        if re.search(r'(?<![0-9A-Za-zÀ-ÿ_])' + re.escape(minusculo)
                     + r'(?![0-9A-Za-zÀ-ÿ_])', tudo):
            continue
        # (b)2 · a colisão se testa por nome contido, e o nome composto também
        # pela primeira palavra: `Paula J.` na peça encosta em `Ana Paula, 40`
        # no insumo, e o teste por string inteira declarou `coincidências: 0`.
        variantes = variantes_do_nome(cand)
        rx = re.compile('|'.join(r'(^|[^a-zà-ú])' + re.escape(v) + r'([^a-zà-ú]|$)'
                                 for v in variantes), re.I)
        no_insumo, privado, autorizado = [], False, False
        for f, conteudo in texto_insumos.items():
            linhas = conteudo.splitlines()
            for i, linha in enumerate(linhas, 1):
                if not (rx.search(linha)
                        and any(contexto_de_pessoa(v, linha) for v in variantes)):
                    continue
                no_insumo.append((str(f), i, linha.strip()[:200]))
                if RX_ARQUIVO_PRIVADO.search(f.name):
                    privado = True
                if any(RX_AUTORIZ.search(x) for x in linhas[max(0, i - 1):i + 3]):
                    autorizado = True
        if not no_insumo:
            continue
        na_peca = []
        for f in pecas:
            na_peca += [(f.name, n, txt) for n, txt in grep_nome_publico(cand, f)]
        # (b)3 · nome que só existe em bastidor não está na peça pública
        if not na_peca:
            continue
        achados[cand] = {'peca': na_peca, 'insumo': no_insumo,
                         'privado': privado, 'autorizado': autorizado}
    return achados


# ── número de terceiro, marcador longo, afirmação sem saída ──────────────────
def marcadores_longos(pecas):
    """Marcador de pendência com mais de 6 palavras dentro dos colchetes. O campo
    registra o dado que falta; o porquê da pendência vai pro handoff."""
    longos = []
    for f in publicas(pecas):
        for i, linha in enumerate(linhas_de(f), 1):
            for m in RX_MARCADOR.finditer(linha):
                dentro = m.group(0)[1:-1]
                n = len(dentro.split())
                if n > TETO_PALAVRAS_MARCADOR:
                    longos.append((f.name, i, n, dentro.strip()[:160]))
    return longos


def numeros_de_terceiro(pecas):
    """Linha com R$ ou % ao lado de nome de terceiro ou concorrente. A tripla
    completa (número, trecho literal, url, consultado em) cabe na linha ou na
    linha seguinte: sem URL o dono não abre a fonte no navegador dele."""
    achados = []
    for f in publicas(pecas):
        linhas = linhas_de(f)
        for i, linha in enumerate(linhas):
            if not (RX_VALOR.search(linha) and RX_TERCEIRO.search(linha)):
                continue
            janela = linha + '\n' + (linhas[i + 1] if i + 1 < len(linhas) else '')
            achados.append({
                'arquivo': f.name, 'linha': i + 1, 'texto': linha.strip()[:200],
                'trecho': bool(RX_TRECHO_LITERAL.search(janela)),
                'url': bool(RX_URL_COMPLETA.search(janela)),
                'data': bool(RX_CONSULTADO.search(janela)),
            })
    return achados


def ultimas_frases_de_bloco(pecas):
    """(a)3 · A última frase de prosa antes de cada título é a que fica com o
    leitor, e é onde o fecho de manual se instala. Devolve (arquivo, linha,
    frase), uma por bloco, mais a última do arquivo."""
    achados = []
    for f in publicas(pecas):
        linhas = linhas_de(f)
        blocos, atual = [], None
        for i, l in enumerate(linhas, 1):
            if RX_TITULO_PECA.match(l):
                if atual:
                    blocos.append(atual)
                atual = None
                continue
            texto = l.strip()
            if (not texto or texto.startswith(('|', '>', '```', '<'))
                    or RX_CERCA.match(l) or len(texto.split()) < 4):
                continue
            atual = (i, texto)
        if atual:
            blocos.append(atual)
        for i, texto in blocos:
            frase = texto.split('. ')[-1].strip()
            achados.append((f.name, i, (frase or texto)[:160]))
    return achados


def afirmacoes_sem_saida(pecas):
    """Frase que afirma um resultado de comando sem a saída literal colada. O
    dono não confere essa linha sem abrir o terminal, então ela sai da entrega."""
    # vale na peça pública. O bastidor (RELATO, handoff, checagem) registra a
    # saída crua que a régua mandou colar, e cobrar dele o gate público reprova
    # justamente a entrega que colou a prova pedida. O lint continua rodando
    # sobre o RELATO no --conferir.
    alvos = publicas(pecas)
    soltas = []
    for f in alvos:
        linhas = linhas_de(f)
        dentro = False
        for i, linha in enumerate(linhas):
            if RX_CERCA.match(linha):
                dentro = not dentro
                continue
            if dentro or not RX_AFIRMA_VERIF.search(linha):
                continue
            if any(RX_CERCA.match(x) for x in linhas[i + 1:i + 4]):
                continue
            soltas.append((f.name, i + 1, linha.strip()[:200]))
    return soltas


# ── o bloco de fecho ─────────────────────────────────────────────────────────
def montar(args, out):
    falhas = []
    p = out.append

    pecas = [Path(x) for x in args.peca]
    for f in pecas:
        if not f.exists():
            print(f'peça não encontrada: {f}', file=sys.stderr)
            return 2, falhas
    # caminho errado não pode virar "sem --perfil": isso apaga o gate em silêncio
    for rotulo, valor in (('--insumos', args.insumos), ('--perfil', args.perfil),
                          ('--titulos', args.titulos), ('--teses', args.teses),
                          ('--nomes', args.nomes)):
        if valor and not Path(valor).exists():
            print(f'{rotulo} não encontrado: {valor}', file=sys.stderr)
            return 2, falhas

    lint_path = Path(args.lint) if args.lint else AQUI / 'lint_copy.py'
    if not lint_path.exists():
        print(f'lint_copy.py não encontrado: {lint_path}', file=sys.stderr)
        return 2, falhas
    lintmod = carregar_lint(lint_path)

    p('```')
    p('# fecho da régua de títulos, saída de scripts/checar_titulos.py')
    p('# cole este bloco INTEIRO em checagem-titulos.md e substitua cada <preencher>, nada mais.')
    # (b)9 · a versão do gate que produziu este bloco viaja com ele
    p(f'script md5: {md5_do_script()}')
    p('')

    # 1 · títulos no lote
    titulos = []
    if args.titulos:
        titulos = [l.strip() for l in linhas_de(args.titulos) if l.strip()]
    n_tit = len(titulos)
    fonte_tit = args.titulos if args.titulos else 'sem --titulos'
    p(f'títulos no lote: {n_tit} | grep -c . {fonte_tit}')

    # (a)1 · o universo de títulos é o que o PÚBLICO lê, e rótulo de estrutura
    # não é isso. Uma entrega auditou 24 `Frame 1, Dia 2` em 29 linhas, com as
    # contagens fechando: o gate passou sobre a lista errada.
    rotulos = [(n, l) for n, l in enumerate(titulos, 1) if RX_ROTULO_ESTRUTURA.match(l)]
    if titulos:
        p(f'rótulos de estrutura em {os.path.basename(str(fonte_tit))}: {len(rotulos)} de '
          f'{n_tit} | grep -cE \'^(Frame|Slide|Dia|Peça|Bloco) *[0-9]\' {fonte_tit}')
        for n, l in rotulos:
            p(f'  rótulo de estrutura, não título: {os.path.basename(str(fonte_tit))}:{n}: {l}')
        if len(rotulos) * 3 > n_tit:
            falhas.append(
                f'rótulo de estrutura no lugar do título: {len(rotulos)} de {n_tit} linhas de '
                f'titulos.txt são rótulo de frame, slide ou dia; o universo é o texto que o '
                f'público lê, não o nome da estrutura')

    # 2 · molde de antítese nos títulos
    if args.titulos:
        _, saida_lint_tit, n_molde_lint = rodar_lint(
            lintmod, ler(args.titulos), os.path.basename(args.titulos))
        extras = []
        for n, linha in enumerate(titulos, 1):
            # o lint (molde com ponto) já pegou esta linha? então não soma de novo.
            if lintmod.molde_antitese(linha, 'x'):
                continue
            # molde de antítese que o lint não pega: duas orações por PONTO, ou
            # a mesma inversão por VÍRGULA + negação ("X, não Y"). Um título conta
            # no máximo uma vez, mesmo que as duas formas casem.
            if duas_oracoes(linha) or antitese_virgula(linha):
                extras.append((n, linha))
        n_molde = n_molde_lint + len(extras)
    else:
        saida_lint_tit, n_molde_lint, extras, n_molde = '', 0, [], 0
    p(f'molde de antítese nos títulos: {n_molde} (teto 1) | fonte: lint_copy.py sobre '
      f'{fonte_tit} ({n_molde_lint} do lint + {len(extras)} de duas orações que o lint não pega)')
    for linha in saida_lint_tit.splitlines():
        if linha.strip():
            p(f'  lint: {linha.rstrip()}')
    for n, linha in extras:
        p(f'  duas orações: {os.path.basename(str(fonte_tit))}:{n}: {linha}')
    if n_molde > 1:
        falhas.append(f'molde de antítese nos títulos: {n_molde} acima do teto 1')

    # 3 · exit do lint por arquivo entregável (a ÚLTIMA coisa que acontece)
    for f in pecas:
        code, saida, _ = rodar_lint(lintmod, ler(f), f.name)
        p(f'arquivo: {f.name} · exit: {code}')
        if code != 0:
            for linha in saida.splitlines():
                if linha.strip().startswith('✗'):
                    p(f'  {linha.strip()}')
            falhas.append(f'lint reprovou {f.name} (exit {code})')

    # 4 · ressalvas na peça
    if args.ressalva:
        total = sum(grep_c(args.ressalva, f) for f in pecas)
        p(f'ressalvas na peça: {total} (teto 1, soma sobre as {len(pecas)} peças do lote: '
          f'num lote a ressalva entra uma vez no conjunto) | grep -c \'{args.ressalva}\' '
          + ' '.join(f.name for f in pecas))
        if total > 1:
            falhas.append(f'ressalvas na peça: {total} acima do teto 1 no lote inteiro')
    else:
        # R12C2(b)9 · sem a flag, o script acha a ressalva sozinho e imprime um
        # NÚMERO. A instrução no lugar do número virava campo não preenchido no
        # --conferir, e o gate passava a reprovar a própria saída padrão dele.
        achadas = []
        for f in publicas(pecas):
            for n, l in enumerate(linhas_de(f), 1):
                if RX_RESSALVA_NA_PECA.search(l):
                    achadas.append(f'{f.name}:{n}: {l.strip()[:80]}')
        trechos = '; '.join(achadas[:3]) if achadas else 'nenhuma'
        p(f'ressalvas na peça: {len(achadas)} (detectadas: {trechos}) (teto 1, sem --ressalva: '
          f'o script grepa as frases de ressalva nas peças públicas) | grep -nEi '
          f'\'{RX_RESSALVA_NA_PECA.pattern}\' ' + ' '.join(f.name for f in publicas(pecas)))
        if len(achadas) > 1:
            falhas.append(f'ressalvas na peça: {len(achadas)} acima do teto 1 no lote inteiro')

    # 5 · marcadores
    total_m = campo = miolo = 0
    linhas_miolo = []
    for f in pecas:
        linhas = linhas_de(f)
        for i, linha in enumerate(linhas):
            for m in RX_MARCADOR.finditer(linha):
                total_m += 1
                if posicao_do_marcador(linhas, i, m.group(0)) == 'campo':
                    campo += 1
                else:
                    miolo += 1
                    linhas_miolo.append(f'{f.name}:{i + 1}: {linha.strip()}')
    p(f'marcadores na peça: {total_m} · em posição de campo: {campo} · no miolo de frase: {miolo}'
      f' | grep -nE \'\\[(A CONFIRMAR|DADO|CONFIRMAR)\' ' + ' '.join(f.name for f in pecas))
    for l in linhas_miolo:
        p(f'  miolo: {l}')
    if miolo:
        falhas.append(f'marcador no miolo de frase: {miolo}')

    # 5b · o marcador é campo, e campo tem tamanho. Marcador de mais de 6
    # palavras não registra o dado que falta: explica a pendência dentro da peça.
    longos = marcadores_longos(pecas)
    p(f'marcadores acima de {TETO_PALAVRAS_MARCADOR} palavras: {len(longos)} (teto 0) | '
      f'grep -oE \'\\[A CONFIRMAR[^]]*\\]\' <peça> | awk \'{{print NF, $0}}\'')
    for arq, n, npal, dentro in longos:
        p(f'  marcador longo ({npal} palavras): {arq}:{n}: [{dentro}]')
        falhas.append(f'marcador longo ({npal} palavras): {arq}:{n}')

    # 6 · palavra-chave de CTA: a palavra que a seguidora DIGITA tem que existir
    # literal nos insumos. Palavra inventada manda a lead pra lugar nenhum.
    palavras_cta = palavras_de_cta(pecas)
    if args.insumos:
        achados = grep_rn(RX_CTA, args.insumos)
        origem_de = {}
        for arq, n, txt in achados:
            for w in RX_CAIXA_ALTA.findall(txt):
                origem_de.setdefault(w, f'{arq}:{n}')
        if not palavras_cta:
            p('palavra-chave: nenhuma (CTA sem palavra)')
        for w, (arqp, np_, linha) in sorted(palavras_cta.items()):
            if w in origem_de:
                p(f'palavra-chave: {w} | origem: {origem_de[w]}')
            else:
                p(f'palavra-chave inventada: {w} | na peça {arqp}:{np_}: {linha}')
                falhas.append(f'palavra-chave inventada: {w}')
        for arq, n, txt in achados:
            p(f'  linha de CTA no insumo: {arq}:{n}: {txt}')
        if len(achados) >= LIMITE_ACHADOS:
            p(f'  (lista cortada em {LIMITE_ACHADOS}: aponte --insumos pra pasta de '
              f'insumos do dono, não pra uma árvore com saída de rodada dentro)')
        if not achados:
            p(f'  sem origem no disco: CTA sai sem palavra | '
              f'grep -rn -iE \'manda |comenta |envia |digita |palavra |chama \' {args.insumos}')
    elif palavras_cta:
        for w, (arqp, np_, linha) in sorted(palavras_cta.items()):
            p(f'palavra-chave inventada: {w} | na peça {arqp}:{np_}: {linha} '
              f'(sem --insumos não há como provar a origem)')
            falhas.append(f'palavra-chave inventada: {w}')
    else:
        p('palavra-chave: nenhuma (CTA sem palavra) | sem --insumos: rode o grep sobre a '
          'pasta de insumos do dono antes de escrever o CTA')

    # 6b · automação no perfil: palavra-chave só existe se a automação existir
    if palavras_cta:
        if args.perfil:
            n_auto = sum(1 for l in linhas_de(args.perfil) if 'automa' in l.lower())
            p(f'automação declarada no perfil: {"sim" if n_auto else "não"} | '
              f'grep -c \'automa\' {args.perfil} = {n_auto}')
            if not n_auto:
                falhas.append('palavra-chave no CTA sem automação declarada no perfil')
        else:
            p('automação declarada no perfil: sem --perfil (palavra-chave no CTA exige '
              'a automação declarada; rode com --perfil)')
            falhas.append('palavra-chave no CTA sem --perfil pra provar a automação')

    # 6d · aspa atribuída a pessoa tem que ter LASTRO no insumo. O modelo inventa
    # a fala e carimba a prova; só o script, cego ao carimbo, lê a aspa contra o
    # insumo. Cada fala entre aspas (15+ chars) apresentada como citação de alguém
    # tem que ser substring literal (normalizada) de algum arquivo de insumo, ou é
    # verbatim potencialmente fabricado e reprova. Só roda com --insumos.
    aspas = aspas_de_citacao(pecas)
    if args.insumos:
        insumo_norma = texto_insumos_normalizado(args.insumos)
        sem_lastro = [(arq, n, t) for arq, n, t in aspas
                      if not aspa_tem_lastro(t, insumo_norma)]
        p(f'aspas de citação verificadas contra o insumo: {len(aspas)} · sem lastro: '
          f'{len(sem_lastro)} (teto 0) | cada fala entre aspas atribuída a alguém tem que '
          f'ser substring literal de algum arquivo de {args.insumos}')
        for arq, n, t in sem_lastro:
            p(f'  aspa sem lastro no insumo: "{t}" | {arq}:{n}')
            falhas.append(f'aspa sem lastro no insumo: "{t[:80]}"')
    elif aspas:
        p(f'verificação de aspa: sem --insumos ({len(aspas)} aspa(s) de citação na peça '
          f'não conferidas; rode com --insumos pra provar o lastro de cada verbatim)')
    else:
        p('verificação de aspa: sem --insumos')

    # 6c · R13 · caixa alta no título. Pedido do dono, e vale nas 47: ênfase é
    # por palavra, nunca por tecla. Título, headline, capa, assunto e CTA com 8
    # ou mais letras e 80% ou mais em maiúscula saem por exit 1. A sigla de até
    # 6 letras e a palavra-chave de CTA achada nos insumos escapam, porque essa
    # a seguidora digita e a caixa alta é a função dela.
    isentas_cta = set(palavras_cta.keys()) | SIGLAS_COMUNS
    gritos = []
    for n, linha in enumerate(titulos, 1):
        prop = caixa_alta_demais(linha, isentas_cta)
        if prop is not None:
            gritos.append((os.path.basename(str(fonte_tit)), n, linha, prop))
    for f in publicas(pecas):
        for n, linha in enumerate(linhas_de(f), 1):
            if not RX_TITULO_PECA.match(linha):
                continue
            prop = caixa_alta_demais(linha, isentas_cta)
            if prop is not None:
                gritos.append((f.name, n, linha.strip(), prop))
    p(f'títulos em caixa alta: {len(gritos)} (teto 0) | 8+ letras e 80%+ em maiúscula, '
      f'sigla de até 6 letras e palavra-chave de CTA fora da conta')
    for arq, n, linha, prop in gritos:
        p(f'  título em caixa alta: {arq}:{n}: {linha} ({round(prop * 100)}% maiúscula)')
        falhas.append(f'título em caixa alta: {linha}')

    # 7 · campos no perfil
    if args.perfil:
        n_campos = grep_c('- ', args.perfil) if False else sum(
            1 for l in linhas_de(args.perfil) if l.startswith('- '))
        p(f'campos no perfil: {n_campos} | grep -c \'^- \' {args.perfil} (arquivo inteiro)')
    else:
        p('campos no perfil: sem --perfil: o piso sai de grep -c \'^- \' sobre o perfil INTEIRO')

    # 8 · teses distintas
    if args.teses:
        teses = [l.strip() for l in linhas_de(args.teses) if l.strip()]
        contagem = {}
        for t in teses:
            chave = t.lower()
            contagem[chave] = contagem.get(chave, 0) + 1
        distintas = len(contagem)
        p(f'teses distintas: {PLACEHOLDER} | de {len(teses)} no lote, '
          f'{distintas} literalmente diferentes (sort {args.teses} | uniq -c); '
          f'o número final é o total menos os pares marcados `conta como 1: sim`')
        for chave in sorted(contagem):
            p(f'  {contagem[chave]:>3} {chave}')
        # (b)9 · comparar string não basta: ninguém escreve duas teses idênticas,
        # e duas teses com o MESMO sujeito e o MESMO predicado contam como UMA.
        # A matriz de TODOS os pares sai impressa, uma linha por par, e é você
        # que responde olhando a tese. O --conferir refaz a conta.
        p(f'matriz de pares de teses: {len(teses) * (len(teses) - 1) // 2} pares '
          f'(responda cada linha; `teses distintas` = {len(teses)} menos os '
          f'`conta como 1: sim`)')
        for i in range(len(teses)):
            for j in range(i + 1, len(teses)):
                p(f'  {teses[i]} vs {teses[j]} | sujeito igual? {PLACEHOLDER} | '
                  f'predicado igual? {PLACEHOLDER} | conta como 1? {PLACEHOLDER}')
    else:
        # R12C2(b)9 · número, nunca instrução. O `teses.txt ausente` fica entre
        # parênteses como motivo, e é o --conferir que reprova o lote acima de 3.
        p('teses distintas: 0 (teses.txt ausente) | salve uma tese de 4 palavras por '
          'linha em teses.txt e rode com --teses')

    # 9 · nomes de pessoa. O número sai do grep, nunca da ausência de flag: o
    # motor que rodou sem --nomes colou `0` numa peça que cita a destinatária 12
    # vezes. Então a contagem soma o que foi declarado com o que o script acha
    # sozinho, e o destinatário entra na conta com a marca dele.
    cands = candidatos_a_nome(pecas, args.insumos, args.perfil) if args.insumos else {}
    declarados = [l.strip() for l in linhas_de(args.nomes) if l.strip()] if args.nomes else []

    presentes = {}
    for nome in declarados:
        ocorr = []
        for f in pecas:
            ocorr += [(f.name, n, txt) for n, txt in grep_nwF(nome, f)]
        autorizado = False
        no_insumo = []
        if args.insumos:
            rx = re.compile(r'(?<![0-9A-Za-zÀ-ÿ_])' + re.escape(nome)
                            + r'(?![0-9A-Za-zÀ-ÿ_])')
            for arq, n, txt in grep_rn(rx, args.insumos):
                no_insumo.append((arq, n, txt))
                try:
                    ctx = linhas_de(arq)
                except OSError:
                    ctx = []
                if any(RX_AUTORIZ.search(x) for x in ctx[max(0, n - 1):n + 3]):
                    autorizado = True
        presentes[nome] = {'peca': ocorr, 'insumo': no_insumo, 'autorizado': autorizado,
                           'privado': False, 'declarado': True}
    for nome, d in cands.items():
        alvo = presentes.setdefault(nome, {'peca': [], 'insumo': [], 'autorizado': False,
                                           'privado': False, 'declarado': False})
        alvo['peca'] = alvo['peca'] or d['peca']
        alvo['insumo'] = alvo['insumo'] or d['insumo']
        alvo['autorizado'] = alvo['autorizado'] or d['autorizado']
        alvo['privado'] = alvo['privado'] or d['privado']

    # o destinatário da mensagem é nome presente, e a decisão de mantê-lo é
    # legítima: ela aparece escrita, com a marca ao lado, e nunca some da conta
    dest = destinatarios(pecas)
    for nome in dest:
        presentes.setdefault(nome, {'peca': [], 'insumo': [], 'autorizado': False,
                                    'privado': False, 'declarado': False})
        if not presentes[nome]['peca']:
            presentes[nome]['peca'] = [(f.name, n, txt) for f in pecas
                                       for n, txt in grep_nwF(nome, f)]

    com_ocorrencia = {n: d for n, d in presentes.items() if d['peca']}
    if not args.insumos and not declarados:
        p('nomes de pessoa na peça: NÃO CONFERIDO | sem --insumos e sem --nomes não houve '
          'grep: zero é uma afirmação sobre a peça e só sai depois do grep -nwF por nome')
        falhas.append('nomes de pessoa na peça: NÃO CONFERIDO (rode com --insumos ou --nomes)')
    elif com_ocorrencia:
        p(f'nomes de pessoa na peça: {len(com_ocorrencia)} | grep -nwF por nome, na peça e '
          f'nos insumos')
    else:
        p('nomes de pessoa na peça: 0 (nenhuma palavra capitalizada da peça bate com pessoa '
          'nos insumos) | grep -nwF rodado por candidato')

    for nome in sorted(com_ocorrencia):
        d = com_ocorrencia[nome]
        marca = 'destinatário, uso interno' if nome in dest else 'terceiro citado'
        p(f'  {nome} · na peça: {len(d["peca"])} · nos insumos: {len(d["insumo"])} · '
          f'classificação: {marca} · autorização no insumo: '
          f'{"sim" if d["autorizado"] else "não"} · '
          f'mensagem privada: {"sim" if d["privado"] else "não"}')
        for arq, n, txt in d['peca'][:3]:
            p(f'    peça {arq}:{n}: {txt}')
        for arq, n, txt in d['insumo'][:3]:
            p(f'    insumo {arq}:{n}: {txt}')
        # a ordem importa: o destinatário é testado ANTES da origem privada.
        # Quem recebe a mensagem tem o nome vindo da caixa de entrada por
        # definição, e responder a ele chamando pelo nome é o uso correto. Com
        # o teste depois, o nome do destinatário reprovava sempre e a isenção
        # nunca era alcançada.
        if nome in dest:
            pass
        elif d['privado'] and not d['autorizado']:
            falhas.append(f'nome de conversa privada em peça pública: {nome}')
        elif d['declarado'] and not d['autorizado']:
            falhas.append(f'nome sem autorização no insumo: {nome}')

    # 9b · o script procura o nome que ninguém declarou: declarar nomes.txt
    # vazio era a saída fácil do gate anterior
    if args.insumos:
        p(f'nomes candidatos achados pelo script: {len(cands)} | palavra capitalizada na '
          f'peça que aparece nos insumos em linha de pessoa')
    else:
        p('nomes candidatos achados pelo script: sem --insumos (rode com a pasta de insumos '
          'do dono: sem ela não há como saber de onde o nome veio)')

    # 9c · número de terceiro sai com a tripla completa: sem URL o dono não abre
    # a fonte, e referência interna de ferramenta não abre no navegador dele.
    terceiros = numeros_de_terceiro(pecas)
    com_trecho = sum(1 for t in terceiros if t['trecho'])
    com_url = sum(1 for t in terceiros if t['url'] and t['data'])
    p(f'números de terceiro: {len(terceiros)} · com trecho literal: {com_trecho} · '
      f'com URL completa: {com_url} | os três iguais, e a linha traz '
      f'`trecho: "<literal>" | url: https://... | consultado em: <dd/mm/aaaa>`')
    for t in terceiros:
        if not (t['trecho'] and t['url'] and t['data']):
            faltando = [r for r, ok in (('trecho literal', t['trecho']),
                                        ('url: https://', t['url']),
                                        ('consultado em:', t['data'])) if not ok]
            p(f'  sem {" e sem ".join(faltando)}: {t["arquivo"]}:{t["linha"]}: {t["texto"]}')
    if not (len(terceiros) == com_trecho == com_url):
        falhas.append(f'números de terceiro: {len(terceiros)} · com trecho literal: '
                      f'{com_trecho} · com URL completa: {com_url} (os três têm que bater)')

    # 9d · afirmação de verificação sem a saída crua colada abaixo
    soltas = afirmacoes_sem_saida(pecas)
    p(f'afirmações de verificação sem saída colada: {len(soltas)} (teto 0) | '
      f'a saída literal do shell entra em bloco cercado logo abaixo da frase')
    for arq, n, txt in soltas:
        p(f'  afirmação de verificação sem saída colada: {arq}:{n}: {txt}')
        falhas.append(f'afirmação de verificação sem saída colada: {arq}:{n}')

    # 10 · (a)1 · teste do nicho trocado, UMA LINHA POR UNIDADE, com a frase
    # copiada inteira. O total sozinho é carimbo: três entregas declararam
    # `sim: 0` e a leitura achou dois, três e quatro casos. A unidade é o título
    # (slide, pauta, capítulo, headline) E a última frase de cada bloco, que é a
    # que fica com o leitor e onde a prosa de manual se instala.
    ultimas = ultimas_frases_de_bloco(pecas)
    p('teste do nicho trocado (troque o substantivo do nicho pelo de outro mercado; '
      'a frase que sobrevive não é do dono). Uma linha por unidade, com a frase '
      'copiada inteira e o substantivo que você trocou. Regra: `sim` acima de 1 '
      'reprova; linha sem `substantivo trocado: <original> → <outro mercado>` não '
      'conta como feita.')
    for i, t in enumerate(titulos, 1):
        p(f'  t{i} | {t} | substantivo trocado: {PLACEHOLDER} | sobrevive? {PLACEHOLDER}')
    for arq, n, frase in ultimas:
        p(f'  {arq}:{n} (última frase de bloco) | {frase} | '
          f'substantivo trocado: {PLACEHOLDER} | sobrevive? {PLACEHOLDER}')
    p(f'unidades no teste do nicho trocado: {len(titulos) + len(ultimas)} '
      f'({len(titulos)} título(s) + {len(ultimas)} última(s) frase(s) de bloco)')
    if not titulos:
        p(f'  sem --titulos: salve um título de abertura por linha em titulos.txt')

    # 11 a 14 · julgamento humano. Universo vazio dispensa a tabela e nunca o
    # fecho: as linhas de título saem com 0 e o motivo, as de inventário,
    # ressalva e consentimento saem com o número real.
    motivo = MOTIVO_SEM_TITULO if not titulos else ''
    p(f'gatilhos fora da lista fechada: {"0" + motivo if not titulos else PLACEHOLDER}')
    p(f'com inimigo ou inversão: {"0" + motivo if not titulos else PLACEHOLDER} de {n_tit}')
    p(f'falas de terceiro: {PLACEHOLDER}')
    p(f'títulos de abertura: {n_tit} · reescritos: '
      f'{"0" + motivo if not titulos else PLACEHOLDER}')
    if n_tit > 3:
        p(f'  (reescritos 0 num lote acima de 3 exige a linha '
          f'`nenhum reescrito porque: <motivo> · título mais fraco do lote: <literal>`)')
    p('```')
    return (1 if falhas else 0), falhas


# ── marcador em HTML de render ───────────────────────────────────────────────
def medir_manchete(png):
    """(b)9 · O --render confere marcador no HTML e ninguém confere o pixel, então
    manchete de 5 linhas passa igual à de 2. Heurística simples: no terço superior
    da arte, ache o maior bloco contíguo de linhas com pixel contrastante e devolva
    a altura dele em porcentagem da arte. Sem PIL, o script pula com aviso: medir
    é melhor que não medir, e não medir é melhor que inventar."""
    try:
        from PIL import Image
    except ImportError:
        return None, 'PIL ausente: medição da manchete pulada (pip install pillow)'
    try:
        with Image.open(png) as im:
            im = im.convert('L')
            larg, alt = im.size
            if not larg or not alt:
                return None, f'{png.name}: imagem vazia'
            px = im.load()
            topo = max(1, alt // 3)
            # a cor de fundo da arte é a moda da primeira linha de pixels
            fundo = max(set(px[x, 0] for x in range(0, larg, max(1, larg // 64))),
                        key=lambda v: sum(1 for x in range(0, larg, max(1, larg // 64))
                                          if px[x, 0] == v))
            cheias = []
            passo = max(1, larg // 128)
            for y in range(topo):
                n = sum(1 for x in range(0, larg, passo) if abs(px[x, y] - fundo) > 40)
                cheias.append(n > 0)
            melhor = atual = 0
            for c in cheias:
                atual = atual + 1 if c else 0
                melhor = max(melhor, atual)
            return round(100 * melhor / alt), None
    except (OSError, ValueError) as e:
        return None, f'{png.name}: não deu pra medir ({e})'


# PENDENTE-r14 · o gerador de render FORMATA e nunca reescreve a copy. Qualquer
# operação de texto sobre a copy-fonte (troca, regex, caixa) no .py do gerador é
# reescrita: o designer-codex trocou duas frases por str.replace() hardcoded e
# saiu com exit 0, enquanto o par que preservou a fonte saiu com exit 1. As duas
# únicas edições que a skill autoriza (tirar nome sem autorização, tirar marcador)
# não passam por essas chamadas.
RX_GERADOR_REESCREVE = re.compile(
    r'\.replace\s*\(|\bre\.sub\s*\(|\.upper\s*\(|\.title\s*\(|\.lower\s*\(|'
    r'\.capitalize\s*\(', re.I)
RX_SCRIPT_DO_GATE = re.compile(r'^(checar_titulos|lint_copy)\.py$', re.I)


def gerador_reescreve(base):
    """Devolve [(arquivo, linha, trecho)] das chamadas de reescrita de texto nos
    .py da pasta (o gerador do render), fora dos scripts do próprio gate."""
    base = Path(base)
    achados = []
    for f in sorted(base.glob('**/*.py')):
        if RX_SCRIPT_DO_GATE.match(f.name) or '__pycache__' in f.parts:
            continue
        for n, l in enumerate(linhas_de(f), 1):
            s = l.strip()
            if s.startswith('#'):
                continue
            m = RX_GERADOR_REESCREVE.search(l)
            if m:
                achados.append((str(f.relative_to(base)), n, s[:120]))
    return achados


def checar_render(caminho, perfil=None):
    """Marcador no HTML de render vira pixel no PNG, e PNG não se corrige por
    colagem. Então o marcador quebra o build, antes de exportar. E, quando existir
    PNG com o mesmo nome-base, a altura da manchete sai medida: alerta ao dono,
    nunca falha. PENDENTE-r14: com --perfil, nome de pessoa sem autorização no
    HTML reprova ANTES do render (o pixel não desfaz depois)."""
    f = Path(caminho)
    if not f.exists():
        print(f'html de render não encontrado: {f}', file=sys.stderr)
        return 2
    achados = [(n, l.strip()[:200]) for n, l in enumerate(linhas_de(f), 1)
               if RX_MARCADOR_HTML.search(l)]
    print(f'marcadores no html de render: {len(achados)} | '
          f'grep -cE \'\\[(A CONFIRMAR|DADO|CONFIRMAR)\' {f.name}')
    for n, l in achados:
        print(f'  {f.name}:{n}: {l}')

    # (b)9 · a medição do PNG, quando ele existir com o mesmo nome-base
    pngs = sorted(x for x in f.parent.glob(f.stem + '*.png') if x.is_file())
    if pngs:
        for i, png in enumerate(pngs, 1):
            pct, aviso = medir_manchete(png)
            if aviso:
                print(f'  aviso: {aviso}')
                continue
            marca = ' · alerta ao dono: a manchete ocupa mais de 45% da arte' \
                if pct > TETO_ALTURA_MANCHETE else ''
            print(f'slide {i} | altura da manchete: {pct}% da arte{marca}')
    else:
        print(f'PNG com o nome-base {f.stem}: nenhum na pasta, medição da manchete pulada')

    # PENDENTE-r14: nome de pessoa sem autorização no HTML reprova ANTES do
    # render. Perguntar num PNG já gerado não desfaz o PNG, e o dono que responde
    # `pode` não repara que já estava lá.
    nomes_sem_aut = []
    if perfil and Path(perfil).exists():
        cands = candidatos_a_nome([f], perfil, perfil)
        for nome, info in sorted(cands.items()):
            if not info['autorizado']:
                onde = info['peca'][0] if info['peca'] else (f.name, 0, '')
                nomes_sem_aut.append((nome, onde[1], onde[2][:120]))
        print(f'nomes de terceiro no HTML do render sem autorização: '
              f'{len(nomes_sem_aut)}')
        for nome, n, l in nomes_sem_aut:
            print(f'  nome sem autorização no render: {nome} · {f.name}:{n}: {l}')

    if achados:
        print('\nREPROVA, e o render não sai: marcador viraria pixel')
        return 1
    if nomes_sem_aut:
        print('\nREPROVA, e o render não sai: nome de terceiro sem autorização viraria pixel')
        return 1
    return 0


# ── modo --conferir ──────────────────────────────────────────────────────────
RX_INT = re.compile(r'\d+')
RX_LINHA_INVENT = re.compile(r'^\s*campos no perfil\s*:(.*)$', re.I)
RX_LINHA_LOTE = re.compile(r'^\s*títulos (?:no lote|produzidos)\s*:\s*(\d+)', re.I | re.M)
# (a)2 · a linha que a skill de auditoria cola sobre a peça externa
RX_LINHA_AUDITADOS = re.compile(r'^\s*títulos auditados\s*:\s*(\d+)', re.I | re.M)
RX_LINHA_NICHO = re.compile(r'sobrevive(?: à troca de nicho)?\?\s*(\S+)', re.I)
# (a)4 · a coluna do substantivo trocado: sem ela a linha do nicho não conta
RX_SUBST_TROCADO = re.compile(
    r'substantivo trocado\s*:\s*(?P<de>[^|<>]+?)\s*(?:→|->)\s*(?P<para>[^|<>]+?)\s*(?=\||$)',
    re.I)
# (a)3 · a linha de contagem que fecha a tabela do nicho
RX_CONTAGEM_NICHO = re.compile(
    r'sobrevive à troca de nicho,?\s*`?sim`?\s*:\s*(?P<n>\d+)(?P<resto>.*)$', re.I)
# (a)3 · a regra de contagem entre parênteses, na MESMA linha, quando o número
# de fecho não for a contagem literal da coluna que ele resume
RX_REGRA_CONTAGEM = re.compile(r'\([^)]{10,}\)')
# (b)1 · achado que já existia na fonte não é falha da conversão
RX_MARCADOR_QUALQUER = re.compile(r'\[(?:A CONFIRMAR|DADO|CONFIRMAR)[^\]]*\]')
RX_LINHA_REESC = re.compile(
    r'^\s*títulos de abertura\s*:\s*(\d+)\s*·\s*reescritos\s*:\s*(\d+)', re.I)
RX_MOTIVO_REESC = re.compile(r'nenhum reescrito porque\s*:', re.I)
RX_DESDOBRADOS = re.compile(r'valores desdobrados\s*:\s*(\d+)', re.I)
RX_CAMPOS_PERFIL = re.compile(r'campos no perfil\s*:\s*(\d+)', re.I)
# (b)7 · os números do inventário saem da própria tabela, nunca da cabeça
RX_LINHA_TABELA = re.compile(r'^\s*\|')
RX_SEPARADOR_TABELA = re.compile(r'^\s*\|[\s:|-]+\|\s*$')
# PENDENTE-r14 · número por extenso em campo numérico (tabela, valor monetário,
# fase numerada) reprova: o gate de número não confirmado premiava a corrupção
# (`| dois |`, `0 a dois`, `seis reais por dia`) e a pessoa lê a tabela entre
# séries. A dose e a leitura de máquina saem em algarismo, sempre.
RX_NUM_EXTENSO = re.compile(
    r'\b(dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|'
    r'quinze|vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa|'
    r'cem|cento|mil|milh[ãa]o|milh[õo]es)\b', re.I)
RX_VALOR_MONETARIO = re.compile(r'R\$|reais?\b|por dia\b|/dia\b', re.I)
# extenso que É o valor monetário: `doze reais`, `R$ doze`, `doze por dia`. Um
# extenso solto numa linha que só menciona um preço em algarismo é prosa.
_EXT = (r'(?:dois|duas|tr[êe]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|'
        r'quinze|vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa|'
        r'cem|cento|mil|milh[ãa]o|milh[õo]es)')
RX_EXTENSO_MONETARIO = re.compile(
    r'(?P<ext>\b' + _EXT + r')\s+(?:reais?|real\b|por dia|/dia)'
    r'|R\$\s*(?P<ext2>' + _EXT + r')\b', re.I)
RX_USADO = re.compile(r'usad', re.I)
RX_DESCARTADO = re.compile(r'descartad', re.I)
RX_DECLARA_USADOS = re.compile(r'usados\s*:\s*(\d+)', re.I)
RX_DECLARA_DESCARTADOS = re.compile(r'descartados(?:\s+com motivo)?\s*:\s*(\d+)', re.I)
# (b)4 · `<arquivo>: N bytes` declarado no RELATO
RX_BYTES_DECLARADO = re.compile(
    r'(?P<arq>[\w][\w.\- ]*\.\w{2,5})\D{0,12}?(?P<n>\d[\d.]*)\s*bytes', re.I)
# (b)10 · variação escrita e não publicada sai da contagem, marcada na linha
RX_DESCARTADA = re.compile(r'descartada,?\s*n[ãa]o publicada', re.I)
# (b)9 · a matriz de pares de teses. Uma linha por par, com as três respostas.
RX_LINHA_TESES = re.compile(r'^\s*teses distintas\s*:\s*(\d+)', re.I | re.M)
# R12C2(b)9 · a saída própria do gate quando não há teses.txt
RX_TESES_AUSENTE = re.compile(r'^\s*teses distintas\s*:\s*0\s*\(teses\.txt ausente\)',
                              re.I | re.M)
RX_PAR_TESES = re.compile(
    r'sujeito igual\?\s*(?P<s>\S+?)\s*\|\s*predicado igual\?\s*(?P<p>\S+?)\s*\|\s*'
    r'conta como 1\?\s*(?P<c>\S+)', re.I)
# (b)9 · qualquer forma da linha de inventário, em qualquer entregável
RX_LINHA_INVENT_QUALQUER = re.compile(
    r'(?:dados fornecidos|dados no perfil|campos no perfil|itens no perfil)\s*:\s*'
    r'(?P<n>\d+)', re.I)
# (b)10 · rótulo que o script imprime seguido de uma LISTA de achados. Duas
# listas diferentes sob o mesmo rótulo é a saída do script reescrita em prosa.
RX_ROTULO_DO_SCRIPT = re.compile(
    r'^\s*[`*]*(?P<rotulo>marcas de tempo|timestamps?|trechos citados|'
    r'linhas? de CTA no insumo|nomes nos insumos privados|'
    r'saída de grep -nwF na peça|títulos no lote|palavra-chave)[`*]*\s*:\s*'
    r'(?P<valor>[^|]*\d[^|]*)$', re.I)


def achados_da_fonte(fonte):
    """(b)1 · A exceção da fonte, pra skill que CONVERTE. Marcador, nome e número
    que já existiam literalmente no arquivo de origem não foram introduzidos pela
    conversão, e reprovar por eles obriga a skill a consertar o que a lei dela
    proíbe consertar. Devolve (texto da fonte, {trecho literal: 'arquivo:linha'})."""
    if not fonte:
        return None, {}
    f = Path(fonte)
    if not f.exists():
        return None, {}
    texto = ler(f)
    mapa = {}
    for i, linha in enumerate(texto.splitlines(), 1):
        for m in RX_MARCADOR_QUALQUER.finditer(linha):
            mapa.setdefault(m.group(0), f'{f.name}:{i}')
    return texto, mapa


def na_fonte(trecho, texto_fonte):
    """O trecho aparece literalmente na fonte?"""
    return bool(texto_fonte) and trecho in texto_fonte


def linha_de_comando(pasta, insumos=None, perfil=None, fonte=None, peca_externa=None):
    """(b)2 · o comando completo, com todo caminho resolvido em absoluto.

    Sai na primeira linha do --conferir pra ser colada no RELATO acima da saída.
    Comando colado diferente do comando da skill reprova a entrega antes da
    análise, e sem esta linha não há como comparar.
    """
    partes = ['python3', str(Path(__file__).resolve()),
              '--conferir', str(Path(pasta).resolve())]
    for rotulo, valor in (('--insumos', insumos), ('--perfil', perfil),
                          ('--fonte', fonte), ('--peca-externa', peca_externa)):
        if valor:
            partes += [rotulo, str(Path(valor).resolve())]
    return ' '.join(partes)


def md5_do_script():
    """(b)9 · os 8 primeiros hex do md5 deste arquivo.

    A entrega guarda a versão do gate que a validou. Dez de doze exit 1 de uma
    rodada vieram de gates que não existiam no commit em vigor: sem esta marca
    o avaliador não distingue defeito de entrega de artefato de versão.
    """
    import hashlib
    try:
        return hashlib.md5(Path(__file__).resolve().read_bytes()).hexdigest()[:8]
    except OSError:
        return 'sem md5'


RX_MD5_GRAVADO = re.compile(r'script md5\s*:\s*([0-9a-f]{8})', re.I)


def tabela_de_inventario(base):
    """(b)7 · a tabela de inventário da pasta, medida por comando.

    Uma entrega declarou `103 · 65 · 38` numa tabela que devolve `104 · 59 ·
    45`: a soma fechava por dentro, e esse é justamente o disfarce de linha
    escrita em vez de contada. A tabela é o bloco de linhas `| ... |` cujas
    células de destino falam de uso ou de descarte. Devolve
    (arquivo, linhas, usados, descartados) ou None quando não há tabela.
    """
    melhor = None
    for f in sorted(Path(base).glob('*.md')):
        linhas = linhas_de(f)
        bloco, atual = [], []
        for l in linhas:
            if RX_LINHA_TABELA.match(l):
                atual.append(l)
                continue
            if atual:
                bloco.append(atual)
                atual = []
        if atual:
            bloco.append(atual)
        for tabela in bloco:
            corpo = [l for l in tabela if not RX_SEPARADOR_TABELA.match(l)]
            if len(corpo) < 3:
                continue
            dados = corpo[1:]  # a primeira é o cabeçalho
            # a contagem é por COLUNA DE DESTINO (a última célula da linha),
            # nunca pela linha inteira: o motivo do descarte costuma repetir a
            # palavra do destino oposto e inflaria as duas contagens.
            destinos = [l.strip().strip('|').split('|')[-1] for l in dados]
            usados = sum(1 for c in destinos if RX_USADO.search(c))
            descartados = sum(1 for c in destinos if RX_DESCARTADO.search(c))
            # a tabela de inventário classifica QUASE toda linha, e classifica
            # dos dois lados: tabela que só tem um dos destinos é outra coisa
            # (um roteiro, uma régua de decisão) e não vale como inventário.
            if usados + descartados < len(dados) * 0.9:
                continue
            if not (usados and descartados):
                continue
            atual_tab = (f.name, len(dados), usados, descartados)
            # a maior tabela qualificada é o inventário: as pequenas são
            # recortes dela ou tabelas de outro assunto
            if melhor is None or len(dados) > melhor[1]:
                melhor = atual_tab
    return melhor


def bytes_declarados(base):
    """(b)4 · cada `<arquivo>: N bytes` do RELATO, com o wc -c ao lado.

    Devolve [(arquivo declarado, número declarado, número real ou None,
    origem)]. Tolerância zero: o RELATO é a única parte da entrega que o dono
    confere sem abrir o terminal, e número redigitado ali vale menos que nada.
    """
    base = Path(base)
    achados = []
    for f in md_da_entrega(base):
        if not RX_BASTIDOR.match(f.name):
            continue
        for n, linha in enumerate(linhas_de(f), 1):
            for m in RX_BYTES_DECLARADO.finditer(linha):
                nome = m.group('arq').strip()
                try:
                    declarado = int(m.group('n').replace('.', ''))
                except ValueError:
                    continue
                # C1(b)1 · o arquivo que o gate reescreve a cada execução não
                # tem tamanho declarável: qualquer wc -c sobre ele descreve a
                # rodada anterior, e a régua manda escrever `gerado pelo gate`
                if RX_ARQUIVO_DO_GATE.match(nome):
                    continue
                alvo = base / nome
                # arquivo que não mora na pasta de saída (o próprio script da
                # skill, um insumo do dono) não é entregável desta entrega, e
                # cobrar o wc -c dele reprovaria por um número correto
                if not alvo.exists():
                    continue
                achados.append((nome, declarado, alvo.stat().st_size, f'{f.name}:{n}'))
    return achados


def conferir(pasta, lint_path, insumos=None, perfil=None, fonte=None,
             peca_externa=None, exige=None, gravar=False):
    """(b)2 · O --conferir grava a PRÓPRIA saída na pasta, pra que o bloco do
    relato entre redirecionado e nunca redigitado à mão.

    C1(b)2 · A prova não mora no caminho que o gate escreve. Quando o
    `conferir.txt` já existe, ele é a prova de quem entregou, e a execução de
    quem confere sai em `conferir.ultimo.txt`: rodar o gate sobre 16 pastas
    apagava a prova das 16. `--gravar` força a sobrescrita, e quem entrega não
    precisa dela.
    """
    base = Path(pasta)
    # R13 · o bastidor mora em conferencia/. A prova de quem entregou continua
    # preservada, agora fora do olho do dono.
    alvo_txt = garantir_conferencia(base) / 'conferir.txt'
    anterior = ler(alvo_txt) if alvo_txt.exists() else None
    preservar = anterior is not None and not gravar
    destino_txt = (alvo_txt.parent / 'conferir.ultimo.txt') if preservar else alvo_txt

    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        # (b)2 · a primeira linha é o comando literal, com --insumos e --perfil
        # resolvidos em caminho absoluto: metade das divergências de uma rodada
        # é compatível com o motor ter apontado --insumos pra outra raiz, e sem
        # a linha colada no RELATO não dá pra saber qual pasta o gate mediu.
        # (b)9 · o md5 do gate na PRIMEIRA linha, junto do comando
        print(f'script md5: {md5_do_script()} · comando: '
              f'{linha_de_comando(pasta, insumos, perfil, fonte, peca_externa)}')
        # (b)9 · o md5 gravado no checagem-titulos.md diz com qual versão do
        # gate a entrega foi escrita. Divergência é AVISO, nunca reprova: o
        # motor não podia saber de gate que ainda não existia quando escreveu.
        alvo_check = caminho_de_bastidor(base, 'checagem-titulos.md')
        if alvo_check.exists():
            m_md5 = RX_MD5_GRAVADO.search(ler(alvo_check))
            if m_md5 and m_md5.group(1).lower() != md5_do_script():
                print(f'gates novos desde a checagem: o checagem-titulos.md foi escrito '
                      f'com o gate {m_md5.group(1)} e esta execução roda o '
                      f'{md5_do_script()}; a diferença é artefato de versão, não defeito '
                      f'da entrega')
        code = _conferir_corpo(pasta, lint_path, insumos, perfil, fonte,
                               peca_externa, exige)
    finally:
        sys.stdout = real
    saida = buf.getvalue()
    print(saida, end='')

    if anterior is not None and not preservar:
        nums_ant = RX_INT.findall(anterior.strip().splitlines()[-1]) if anterior.strip() else []
        nums_novo = RX_INT.findall(saida.strip().splitlines()[-1]) if saida.strip() else []
        if nums_ant != nums_novo:
            print(f'aviso: conferir.txt de execução anterior fecha com {nums_ant or "sem número"} '
                  f'e esta execução fecha com {nums_novo or "sem número"}; o arquivo foi '
                  f'sobrescrito com a saída de agora')
    try:
        destino_txt.write_text(saida, encoding='utf-8')
        if preservar:
            print(f'saída gravada em {destino_txt.name} · prova anterior preservada '
                  f'em conferir.txt')
        else:
            print(f'saída gravada em {destino_txt.name}')
    except OSError as e:
        print(f'aviso: não deu pra gravar {destino_txt.name} ({e})')
    return code


def _conferir_corpo(pasta, lint_path, insumos=None, perfil=None, fonte=None,
                    peca_externa=None, exige=None):
    """Passo 2: relê o checagem-titulos.md que o agente preencheu e confere.

    O passo 1 imprime; aqui o script cobra. Sem o arquivo não há entrega, e
    nenhum bloco é impresso: a ausência é a reprovação. Com --insumos, o
    consentimento roda de novo sobre as peças da pasta: o gate de nome não pode
    valer só no passo 1, porque a peça muda entre um passo e outro.
    """
    base = Path(pasta)
    alvo = caminho_de_bastidor(base, 'checagem-titulos.md')
    if not alvo.exists():
        print(f'checagem-titulos.md ausente em {base}/{SUBPASTA_BASTIDOR}/: '
              f'a entrega não existe.', file=sys.stderr)
        print(f'Rode o passo 1 com --gravar-checagem e volte aqui.', file=sys.stderr)
        return 1

    falhas = []
    texto = ler(alvo)
    linhas = texto.splitlines()
    print(f'checagem-titulos.md: presente | ls {alvo}')

    # R13 · o bastidor mora em conferencia/, e a raiz fica com o entregável e o
    # handoff. A dona abriu 9 arquivos numa pasta e não sabia se guardava ou
    # jogava fora; um deles tinha 49 KB, maior que a entrega somada.
    na_raiz = bastidor_na_raiz(base)
    print(f'bastidor na raiz da pasta do dono: {len(na_raiz)} (teto 0) | '
          f'ls {base} · o bastidor mora em {SUBPASTA_BASTIDOR}/')
    for nome in na_raiz:
        print(f'  aviso: bastidor na raiz, mova pra {SUBPASTA_BASTIDOR}/: {nome}')
    if na_raiz:
        falhas.append(
            f'pasta do dono com bastidor: {", ".join(na_raiz)}; mova pra '
            f'{SUBPASTA_BASTIDOR}/ e deixe na raiz só o entregável e o handoff')

    lixo = lixo_na_raiz(base)
    print(f'log e cache na raiz: {len(lixo)} (teto 0) | find {base} -maxdepth 1 '
          f'-name \'*.log\' -o -name __pycache__')
    for nome in lixo:
        print(f'  lixo de máquina na raiz: {nome}')
    if lixo:
        falhas.append(
            f'pasta do dono com lixo de máquina: {", ".join(lixo)}; log e cache de '
            f'execução saem da entrega')

    # R12C2(b)8 · o caminho de --insumos é a RAIZ que contém o perfil. Três
    # pastas colaram uma subpasta enquanto a régua roda com a raiz: mesmo exit
    # nos dois caminhos, e é por isso que o defeito sobreviveu duas rodadas. Um
    # gate que só vale quando o resultado muda ensina o motor a improvisar o
    # caminho, então a divergência de forma sai por exit.
    if insumos:
        p_ins = Path(insumos).resolve()
        print(f'insumos resolvido: {p_ins}')
        if perfil:
            p_perf = Path(perfil).resolve()
            dentro = p_perf.parent == p_ins or p_ins in p_perf.parents
            pai_tem = p_ins.parent == p_perf.parent or p_perf.parent in p_ins.parents
            if not dentro and pai_tem:
                print(f'insumos recortado: o perfil está fora da pasta de insumos '
                      f'({p_perf.parent} contém o perfil e é o pai de {p_ins})')
                falhas.append(
                    f'insumos recortado: o perfil está fora da pasta de insumos; passe '
                    f'--insumos {p_perf.parent}, a raiz que contém o perfil e os insumos')

    # B(b)1 · os arquivos que a AÇÃO exige. Uma pasta sem deck e sem página
    # recebeu `conferência ok: a entrega sai` num pedido de pacote, e o exit 0
    # foi o que permitiu o corte passar. A skill declara a lista por ação no
    # bloco de pronto; aqui ela vira exit.
    if exige:
        pedidos = [x.strip() for x in re.split(r'[,\s]+', exige) if x.strip()]
        presentes = 0
        for nome in pedidos:
            achado = sorted(base.glob(nome))
            if achado:
                presentes += 1
                print(f'  arquivo exigido pela ação: {nome} · presente '
                      f'({achado[0].name}) | ls {base}/{nome}')
            else:
                print(f'  arquivo exigido pela ação ausente: {nome} | '
                      f'ls {base}/{nome}')
                falhas.append(f'arquivo exigido pela ação ausente: {nome}')
        print(f'arquivos exigidos pela ação: {len(pedidos)} · presentes: {presentes}')

    # (b)1 · a exceção da fonte. Só a skill que converte passa --fonte, e só o
    # que a conversão INTRODUZIU reprova: o resto sai como `achado na fonte`.
    texto_fonte, mapa_fonte = achados_da_fonte(fonte)
    if fonte:
        if texto_fonte is None:
            print(f'--fonte não encontrado: {fonte}', file=sys.stderr)
            return 2
        print(f'fonte da conversão: {Path(fonte).name} | marcadores na fonte: '
              f'{len(mapa_fonte)} | grep -c \'\\[A CONFIRMAR\' {Path(fonte).name}')

    # 1 · nenhum <preencher> sobrando
    sobrando = [(n, l.strip()[:160]) for n, l in enumerate(linhas, 1) if PLACEHOLDER in l]
    print(f'<preencher> sobrando: {len(sobrando)} (teto 0)')
    for n, l in sobrando:
        print(f'  checagem-titulos.md:{n}: {l}')
    if sobrando:
        falhas.append(f'<preencher> sobrando: {len(sobrando)}')

    # PENDENTE-r14: <preencher> em QUALQUER arquivo da pasta (raiz e conferencia/,
    # inclusive teste-nicho-trocado.txt) conta como teste não feito. O webinar
    # entregou a tabela do nicho inteira em branco e os títulos saíram sem passar
    # pelo gate que decide se são do dono.
    sobrando_pasta = []
    vistos_pl = {alvo.resolve()}
    # conserto 8: os arquivos que o próprio gate grava carregam <preencher> nos
    # rótulos que ele imprime (o passo 1 é o template ANTES de o motor preencher
    # o checagem-titulos.md). Pega conferir.txt, conferir.ultimo.txt,
    # conferir.ultimo-check.txt, checar-passo1*.txt e checagem-raw*.txt.
    RX_CAPTURA_GATE = re.compile(
        r'^(?:conferir[\w.\-]*\.txt|checar-passo1[\w.\-]*\.txt|checagem-raw[\w.\-]*\.txt)$',
        re.I)
    for f in sorted(base.glob('*.md')) + sorted(base.glob('*.txt')) \
            + sorted((base / SUBPASTA_BASTIDOR).glob('*')):
        if not f.is_file() or f.resolve() in vistos_pl:
            continue
        vistos_pl.add(f.resolve())
        if f.suffix.lower() not in ('.md', '.txt', '.json'):
            continue
        # os arquivos que o próprio gate captura carregam <preencher> nos rótulos
        # que ele imprime: são saída, não teste em branco.
        if RX_CAPTURA_GATE.match(f.name):
            continue
        for n, l in enumerate(linhas_de(f), 1):
            if PLACEHOLDER in l:
                sobrando_pasta.append((f.name, n, l.strip()[:160]))
    print(f'<preencher> em outros arquivos da pasta: {len(sobrando_pasta)} (teto 0) | '
          f'grep -rn \'<preencher>\' {base}')
    for nome, n, l in sobrando_pasta:
        print(f'  {nome}:{n}: {l}')
    if sobrando_pasta:
        falhas.append(f'<preencher> em arquivo da pasta (teste não feito): '
                      f'{len(sobrando_pasta)}')

    # PENDENTE-r14 · o gerador de render formata e nunca reescreve a copy-fonte.
    reescritas = gerador_reescreve(base)
    if reescritas:
        print(f'chamadas de reescrita de texto no gerador: {len(reescritas)} (teto 0) | '
              f'grep -nE \'\\.replace\\(|re\\.sub\\(|\\.upper\\(|\\.title\\(\' nos .py')
        for arq, n, l in reescritas:
            print(f'  gerador reescreve a copy: {arq}:{n}: {l}')
            falhas.append(f'gerador reescreve a copy: {arq}:{n} ({l[:40]})')

    # 1b · (b)6 · campo do fecho cujo VALOR é uma mensagem de ajuda do próprio
    # script conta como NÃO PREENCHIDO. Um lote fechou `teses distintas: sem
    # --teses: salve uma tese ... e rode de novo` e a conferência passou com
    # exit 0: a mensagem que ensina a rodar não é o resultado de ter rodado.
    instruidos, proprias = [], []
    for n, l in enumerate(linhas, 1):
        crua = l.strip()
        if ':' not in crua or crua.startswith(('#', '>', '|', '`')):
            continue
        campo, _, valor = crua.partition(':')
        campo = campo.lstrip('-*• ').strip('* ').strip()
        valor = valor.strip().lower()
        if not campo or len(campo) > 60 or not valor:
            continue
        # R12C2(b)9 · a lista de saídas próprias do gate. Linha que o PRÓPRIO
        # script imprime por falta de flag nunca conta como campo com instrução:
        # o motor não tem como adivinhar uma flag que a versão anterior não
        # pedia, e punir a saída padrão reprova retroativamente a frota inteira.
        if RX_SAIDA_PROPRIA_DO_GATE.search(crua):
            proprias.append((n, campo))
            continue
        if RX_AJUDA_NO_FECHO.search(valor):
            instruidos.append((n, campo, crua[:160]))
    if proprias:
        print(f'saídas próprias do gate no fecho: {len(proprias)} (não contam como campo '
              f'com instrução: são o texto que o script imprime por falta de flag)')
        for n, campo in proprias:
            print(f'  saída do próprio gate: checagem-titulos.md:{n}: {campo}')
    print(f'campos do fecho com instrução no lugar do número: {len(instruidos)} (teto 0)')
    for n, campo, crua in instruidos:
        print(f'  checagem-titulos.md:{n}: {crua}')
        falhas.append(f'campo com instrução no lugar do número: {campo}')

    # 2 · nicho trocado: `sim` acima de 1 reprova. (a)4 · cada linha nomeia o
    # substantivo que foi trocado; sem a coluna a linha não conta como feita,
    # porque o veredito fica no gosto de quem escreve. (a)3 · a linha de fecho
    # tem que ser a contagem literal da coluna, ou trazer a regra ao lado.
    sims, sem_coluna = 0, []
    for n, l in enumerate(linhas, 1):
        m = RX_LINHA_NICHO.search(l)
        if not m:
            continue
        if m.group(1).strip().lower().startswith('sim'):
            sims += 1
        ms = RX_SUBST_TROCADO.search(l)
        if not ms or PLACEHOLDER in ms.group(0):
            sem_coluna.append((n, l.strip()[:140]))
    print(f'sobrevive à troca de nicho, `sim`: {sims} (teto 1)')
    print(f'linhas do nicho sem `substantivo trocado: <original> → <outro mercado>`: '
          f'{len(sem_coluna)} (teto 0)')
    for n, l in sem_coluna:
        print(f'  checagem-titulos.md:{n}: {l}')
        falhas.append(f'linha do nicho sem a coluna do substantivo trocado: '
                      f'checagem-titulos.md:{n}')
    if sims > 1:
        falhas.append(f'sobrevive à troca de nicho: {sims} acima do teto 1')

    # 2c · (a)3 · a linha de contagem bate com a tabela que ela fecha
    for n, l in enumerate(linhas, 1):
        mc = RX_CONTAGEM_NICHO.search(l)
        if not mc:
            continue
        declarado_nicho = int(mc.group('n'))
        tem_regra = bool(RX_REGRA_CONTAGEM.search(mc.group('resto')))
        print(f'contagem de fecho do nicho: {declarado_nicho} · `sim` na tabela: {sims} '
              f'· regra de contagem na mesma linha: {"sim" if tem_regra else "não"}')
        if declarado_nicho != sims and not tem_regra:
            falhas.append(
                f'contagem não bate com a tabela: a linha declara {declarado_nicho} e a '
                f'tabela marca {sims} `sim`; ou o número é a contagem literal da coluna, '
                f'ou a regra sai entre parênteses na mesma linha')

    # 2b · (b)9 · a matriz de pares refaz a conta de `teses distintas`. Comparar
    # string só pega tese idêntica, e ninguém escreve duas idênticas: duas teses
    # com o mesmo sujeito E o mesmo predicado contam como UMA.
    pares = [RX_PAR_TESES.search(l) for l in linhas]
    pares = [m for m in pares if m]
    fundidos = sum(1 for m in pares if m.group('c').strip().lower().startswith('s'))
    m_teses = RX_LINHA_TESES.search(texto)
    # R12C2(b)9 · `teses distintas: 0 (teses.txt ausente)` é a saída padrão do
    # próprio gate, e ela reprova por ARQUIVO AUSENTE em lote acima de 3, nunca
    # por "campo com instrução": punir a saída do gate anterior transforma toda
    # atualização de script em reprovação retroativa da frota de entregas.
    if RX_TESES_AUSENTE.search(texto):
        m_l = RX_LINHA_LOTE.search(texto)
        n_l = int(m_l.group(1)) if m_l else 0
        print(f'teses distintas: 0 · teses.txt ausente · títulos no lote: {n_l} '
              f'(acima de 3 exige a lista de teses) | ls teses.txt')
        if n_l > 3:
            falhas.append(
                f'teses.txt ausente: o lote tem {n_l} títulos e `teses distintas` só sai '
                f'da lista de teses salva em teses.txt')
    elif m_teses:
        declaradas = int(m_teses.group(1))
        teto = None
        # o total do lote vem da própria matriz: N pares = N*(N-1)/2 teses
        n_par = len(pares)
        if n_par:
            total = int((1 + (1 + 8 * n_par) ** 0.5) / 2 + 0.5)
            teto = total - fundidos
        print(f'teses distintas: {declaradas} · pares na matriz: {n_par} · '
              f'`conta como 1: sim`: {fundidos}'
              + (f' · teto pela matriz: {teto}' if teto is not None else ''))
        if teto is not None and declaradas > teto:
            falhas.append(
                f'teses distintas: {declaradas} acima do teto {teto} (total menos os '
                f'{fundidos} pares marcados `conta como 1: sim`)')
        # PENDENTE-r14: lote de 1 título tem 0 pares, e 0 pares é a matriz
        # correta, não a matriz ausente. Um editor de vídeo que corta um reels
        # só entrega uma tese: exigir a matriz de pares aí é reprovar o certo.
        m_l_par = RX_LINHA_LOTE.search(texto)
        n_lote_par = int(m_l_par.group(1)) if m_l_par else declaradas
        if n_par == 0 and declaradas > 1 and n_lote_par > 1:
            print('  matriz de pares de teses ausente: `teses distintas` sem a matriz '
                  'de TODOS os pares não conta como feita')
            falhas.append('a matriz de pares de teses não está no checagem-titulos.md')
        elif n_par == 0 and (declaradas <= 1 or n_lote_par <= 1):
            print('  matriz de pares de teses: 0 pares (lote de 1 tese, sem par a comparar)')

    # 3 · reescritos zerado em lote acima de 3 sem motivo
    for l in linhas:
        m = RX_LINHA_REESC.search(l)
        if not m:
            continue
        n_ab, n_re = int(m.group(1)), int(m.group(2))
        # C1(b)3 · a versão morta é o que prova que a reescrita foi tentada. A
        # prosa não pegou em três rodadas seguidas: agora é exit.
        mortas = sum(1 for f in md_da_entrega(base)
                     for l in linhas_de(f) if RX_REESCRITO_DE.search(l))
        print(f'títulos de abertura: {n_ab} · reescritos: {n_re} · '
              f'linhas `reescrito de:` na pasta: {mortas} | '
              f'grep -rc \'reescrito de:\' {base}')
        if n_re == 0 and n_ab > 3 and not RX_MOTIVO_REESC.search(texto):
            falhas.append(
                f'reescritos 0 em {n_ab} títulos de abertura sem a linha '
                f'`nenhum reescrito porque:`')
        if n_re == 0 and n_ab > 3 and mortas == 0:
            falhas.append(
                f'reescritos 0 em {n_ab} títulos de abertura sem nenhuma linha '
                f'`reescrito de:` na pasta: a versão morta colada é o que prova que '
                f'a reescrita foi tentada, e a justificativa em prosa deixou de bastar')
        # B(b)10 · num universo grande, 1 em 52 é a régua rodando de leve
        if n_ab > 20 and n_re * 20 < n_ab:
            falhas.append(
                f'reescritos {n_re} num universo de {n_ab} títulos de abertura: abaixo '
                f'de 5% do universo a régua rodou de leve, e a saída pede a versão '
                f'morta de pelo menos três títulos')

    # 4 · os quatro inteiros do inventário, e o desdobramento nunca menor que o piso
    achou_inv = False
    for l in linhas:
        m = RX_LINHA_INVENT.match(l)
        if not m:
            continue
        achou_inv = True
        n_ints = len(RX_INT.findall(m.group(1)))
        print(f'inteiros na linha `campos no perfil`: {n_ints} (exigido 4)')
        if n_ints != 4:
            falhas.append(
                f'a linha `campos no perfil` traz {n_ints} inteiros, e a régua pede 4 '
                f'(piso, desdobrados, usados, descartados), nunca `ver OUTRO.md`')
    if not achou_inv:
        print('inteiros na linha `campos no perfil`: linha ausente (exigida)')
        falhas.append('a linha `campos no perfil` não existe no checagem-titulos.md')
    m_piso, m_desd = RX_CAMPOS_PERFIL.search(texto), RX_DESDOBRADOS.search(texto)
    if m_piso and m_desd:
        piso, desd = int(m_piso.group(1)), int(m_desd.group(1))
        print(f'campos no perfil: {piso} · valores desdobrados: {desd}')
        if desd < piso:
            falhas.append(
                f'valores desdobrados {desd} menor que campos no perfil {piso}: '
                f'desdobrar campo composto só aumenta')
    # C1(b)8 · o rótulo do piso não se usa no total desdobrado. `campos no
    # perfil: 38` contra `grep -c '^- '` = 29 é o rótulo trocado, e a explicação
    # ao lado não conserta o rótulo: o total desdobrado se chama
    # `valores desdobrados`, e M maior que N é o esperado.
    if m_piso and perfil and Path(perfil).exists():
        real = sum(1 for l in linhas_de(perfil) if l.startswith('- '))
        print(f'campos no perfil declarado: {int(m_piso.group(1))} · '
              f'grep -c \'^- \' {Path(perfil).name}: {real}')
        if int(m_piso.group(1)) > real:
            falhas.append(
                f'rótulo do piso trocado: `campos no perfil` declara '
                f'{int(m_piso.group(1))} e o grep -c \'^- \' do perfil devolve {real}; '
                f'o piso é a saída literal do comando, e o total depois do '
                f'desdobramento se chama `valores desdobrados`')

    # 4a · (b)7 · os três números do inventário saem de comando sobre a tabela
    tab = tabela_de_inventario(base)
    if tab:
        arq_tab, n_linhas, n_usados, n_descartados = tab
        print(f'inventário medido na tabela: {arq_tab} · linhas: {n_linhas} · '
              f'usados: {n_usados} · descartados: {n_descartados} | '
              f'grep -c \'^| \' {arq_tab} menos o cabeçalho, '
              f'grep -ci \'usad\' e grep -ci \'descartad\' sobre as linhas de dados')
        m_us, m_de = RX_DECLARA_USADOS.search(texto), RX_DECLARA_DESCARTADOS.search(texto)
        m_de_piso = RX_DESDOBRADOS.search(texto)
        for rotulo, declarado_m, medido in (
                ('valores desdobrados', m_de_piso, n_linhas),
                ('usados', m_us, n_usados),
                ('descartados', m_de, n_descartados)):
            if not declarado_m:
                continue
            declarado_n = int(declarado_m.group(1))
            print(f'  {rotulo}: declarado {declarado_n} · medido {medido}')
            if declarado_n != medido:
                falhas.append(
                    f'inventário redigitado: `{rotulo}` declarado {declarado_n} e a '
                    f'tabela de {arq_tab} devolve {medido}; o número sai de comando '
                    f'sobre a tabela, nunca da soma que fecha por dentro')
    else:
        print('inventário medido na tabela: sem tabela de inventário na pasta '
              '(os números do inventário ficam sem conferência automática)')

    # 4b · (b)9 · um inventário por entrega. Duas linhas de inventário com
    # números diferentes na mesma entrega reprovam: `Dados fornecidos: 17` num
    # arquivo e `dados no perfil: 29` noutro não são dois recortes, são dois
    # números sobre o mesmo perfil, e o dono não sabe qual vale.
    invent = {}
    for f in md_da_entrega(base):
        for n, l in enumerate(linhas_de(f), 1):
            m = RX_LINHA_INVENT_QUALQUER.search(l)
            if m:
                invent.setdefault(int(m.group('n')), []).append(
                    f'{f.name}:{n}: {l.strip()[:120]}')
    print(f'linhas de inventário na entrega: {sum(len(v) for v in invent.values())} · '
          f'números distintos: {len(invent)} (exigido no máximo 1)')
    for numero in sorted(invent):
        for onde in invent[numero]:
            print(f'  {onde}')
    if len(invent) > 1:
        falhas.append(
            f'inventário duplicado: {len(invent)} números diferentes na mesma entrega '
            f'({", ".join(str(x) for x in sorted(invent))}); o inventário é um só')

    # 4b2 · B(b)2 · a conclusão nasce da saída do grep, e negar a saída colada
    # na mesma checagem é a contradição interna mais barata de detectar do loop:
    # duas ocorrências de palavra-chave coladas no próprio checagem-titulos.md e
    # `palavra-chave: nenhuma` na peça, mais `descartado porque não consta`.
    nega_chave = [(f.name, n, l.strip()[:140])
                  for f in md_da_entrega(base)
                  for n, l in enumerate(linhas_de(f), 1)
                  if RX_CHAVE_NENHUMA.search(l) or RX_DESCARTE_NAO_CONSTA.search(l)]
    achou_chave = [(f.name, n, l.strip()[:140])
                   for f in md_da_entrega(base)
                   for n, l in enumerate(linhas_de(f), 1)
                   if RX_CHAVE_ACHADA.search(l)]
    print(f'conclusão negativa de palavra-chave: {len(nega_chave)} · ocorrências '
          f'coladas na mesma entrega: {len(achou_chave)}')
    for nome_a, n, l in nega_chave + achou_chave:
        print(f'  {nome_a}:{n}: {l}')
    if nega_chave and achou_chave:
        falhas.append(
            f'conclusão contradiz a saída do grep: a entrega declara palavra-chave '
            f'nenhuma e cola {len(achou_chave)} ocorrência(s) na mesma checagem; '
            f'conclusão negativa só é válida com a saída vazia')

    # 4c · (b)10 · a saída do script entra uma vez e não se reescreve em prosa.
    # O mesmo rótulo com duas listas diferentes reprova: recorte mais amplo sai
    # com rótulo diferente e com o comando que o produziu ao lado.
    # PENDENTE-r14: rótulos que o PRÓPRIO script imprime uma linha por ocorrência
    # (uma por hit do grep) são multi-linha por natureza: `linha de cta no insumo`
    # saiu 29 vezes num reclamacao e o gate leu 29 listas diferentes. Só os
    # rótulos de VALOR ÚNICO (um número que resume) contam como reescrita quando
    # aparecem com valores diferentes.
    ROTULOS_MULTI_LINHA = {
        'linha de cta no insumo', 'linhas de cta no insumo',
        'nomes nos insumos privados', 'saída de grep -nwf na peça',
    }
    listas = {}
    for f in md_da_entrega(base):
        for n, l in enumerate(linhas_de(f), 1):
            m = RX_ROTULO_DO_SCRIPT.match(l)
            if not m:
                continue
            rotulo = m.group('rotulo').strip().lower()
            if rotulo in ROTULOS_MULTI_LINHA:
                continue
            valor = ' '.join(m.group('valor').split())
            listas.setdefault(rotulo, {}).setdefault(valor, []).append(f'{f.name}:{n}')
    reescritos = {r: v for r, v in listas.items() if len(v) > 1}
    print(f'rótulos do script com mais de uma lista: {len(reescritos)} (teto 0)')
    for rotulo, valores in sorted(reescritos.items()):
        for valor, ondes in sorted(valores.items()):
            print(f'  {rotulo}: {valor} | {", ".join(ondes)}')
        falhas.append(
            f'saída do script reescrita: o rótulo `{rotulo}` aparece com '
            f'{len(valores)} listas diferentes; recorte mais amplo sai com rótulo '
            f'diferente e o comando ao lado')

    # 5 · o universo da régua é contado por comando, nunca escolhido
    m_lote = RX_LINHA_LOTE.search(texto)
    # (a)2 · quando a skill AUDITA um arquivo que mora fora da pasta (crítico de
    # copy), o universo de títulos é o daquela peça, nunca o da pasta de saída:
    # contar na pasta faz o gate passar sobre uma auditoria que leu outra coisa.
    if peca_externa:
        ext = Path(peca_externa)
        if not ext.exists():
            print(f'--peca-externa não encontrada: {ext}', file=sys.stderr)
            return 2
        pecas = [ext]
    else:
        # só a peça pública: cabeçalho de handoff e de relato é estrutura de
        # bastidor, nunca título que disputa a atenção do leitor
        pecas = sorted(f for f in base.glob('*.md')
                       if f.name != 'RELATO.md' and not RX_BASTIDOR.match(f.name))
    # (b)7 · o universo soma .md, .html e .pptx da pasta. Zero por ausência de
    # varredura nunca é impresso: sem nenhuma das três formas, a linha diz o
    # motivo e reprova, porque zero é uma afirmação sobre a peça.
    if peca_externa:
        n_pecas = len(titulos_de_md(pecas[0]))
        detalhe_univ, motivo_univ = [(pecas[0].name, 'md', n_pecas)], ''
    else:
        n_pecas, detalhe_univ, motivo_univ = universo_de_titulos(base, pecas)
    # conserto 6 (r14a) · peça renderizada em 2 temas (claro/escuro): o universo
    # nasce da COPY fonte (titulos.txt), não do documento operacional que sobra no
    # topo (o PEDIDO-DE-IMAGEM) nem do dobro de PNG. Um por card, e a checagem bate
    # com o titulos.txt que o motor extraiu da copy. Só vale quando a peça sai em
    # temas: a pasta com um único conjunto de render e uma peça .md legível segue
    # medindo o universo pela peça, como sempre.
    arq_tit_univ = caminho_de_bastidor(base, 'titulos.txt')
    if not peca_externa and peca_sai_em_temas(base) and arq_tit_univ.exists():
        n_copy = sum(1 for l in linhas_de(arq_tit_univ) if l.strip())
        if n_copy:
            n_pecas = n_copy
            detalhe_univ = [('titulos.txt', 'copy fonte (um por card)', n_copy)]
            motivo_univ = ''
    for nome_arq, tipo_arq, n_arq in detalhe_univ:
        print(f'  títulos em {nome_arq} ({tipo_arq}): {n_arq}')
    # (b)6 · o universo sai declarado, com os arquivos contados e os de fora
    print(linha_do_universo(detalhe_univ))
    if motivo_univ:
        print(f'sem peça varrível: {motivo_univ}')
        falhas.append(f'sem peça varrível: {motivo_univ}; zero não sai de varredura '
                      f'que não olhou pro arquivo certo')

    # R12C2(b)5 · titulos.txt vazio com peça RENDERIZADA na pasta. Uma entrega
    # saiu com titulos.txt de 0 bytes para 10 cards em dois temas: oito telas
    # foram publicadas sem gate. O universo não é a varredura do topo da pasta,
    # é o que o público lê, e quando a peça mora em subpasta o conserto é
    # apontar o gate pra ela, nunca reduzir o universo.
    arq_tit = caminho_de_bastidor(base, 'titulos.txt')
    if not peca_externa and arq_tit.exists():
        renderizadas = renders_na_pasta(base)
        n_tit_arq = sum(1 for l in linhas_de(arq_tit) if l.strip())
        if renderizadas:
            print(f'peças renderizadas na pasta: {len(renderizadas)} · linhas em '
                  f'titulos.txt: {n_tit_arq} | find {base} -name \'slide-*.png\' -o '
                  f'-name \'*.html\' -o -name \'*.pptx\'')
            for nome_r in renderizadas[:8]:
                print(f'  renderizada: {nome_r}')
        if renderizadas and n_tit_arq == 0:
            extraidos = titulos_da_copy_fonte(base)
            print(f'universo de títulos vazio com peça renderizada: {len(renderizadas)} '
                  f'peças e titulos.txt com 0 linhas')
            if extraidos:
                print(f'títulos extraídos do arquivo de copy ou manifesto: {len(extraidos)} '
                      f'(monte titulos.txt com estes, um por linha, na ordem dos arquivos)')
                for t in extraidos[:20]:
                    print(f'  título da fonte: {t}')
            else:
                print('  nenhum arquivo de copy ou manifesto na pasta pra extrair o '
                      'universo; aponte o gate pros arquivos da subpasta')
            falhas.append(
                f'universo de títulos vazio com peça renderizada: {len(renderizadas)} peças '
                f'renderizadas e titulos.txt com 0 linhas; a peça publicada sai sem gate')
        elif renderizadas and n_tit_arq < len(renderizadas):
            falhas.append(
                f'titulos.txt com {n_tit_arq} linhas para {len(renderizadas)} peças '
                f'renderizadas; o universo cobre uma linha por peça publicada')
    if peca_externa:
        m_aud = RX_LINHA_AUDITADOS.search(texto)
        auditados = int(m_aud.group(1)) if m_aud else 0
        print(f'peça auditada (fora da pasta): {Path(peca_externa).name} · títulos nela: '
              f'{n_pecas} · títulos auditados declarados: {auditados}')
        if auditados < n_pecas:
            falhas.append(
                f'títulos auditados: {auditados} menor que os {n_pecas} títulos da peça '
                f'auditada ({Path(peca_externa).name}); a régua cobre a peça inteira')
    # C1(a)1 e (a)2 · cabeçalho de peça pública que é rótulo, não tese
    if not peca_externa:
        rotulos = rotulos_no_miolo(pecas, texto_fonte)
        introduzidos = [(a, n, l) for a, n, l, herd in rotulos if not herd]
        herdados_rot = [(a, n, l) for a, n, l, herd in rotulos if herd]
        print(f'cabeçalhos de rótulo no miolo da peça pública: {len(introduzidos)} (teto 0) | '
              f'grep -nE \'^#{{1,4}} *(Etapa|Passo|Seção|Bloco|P[0-9]|Parte|Checagem)\' '
              f'nas peças')
        for nome_a, n, l in introduzidos:
            print(f'  rótulo no miolo: {nome_a}:{n}: {l}')
        for nome_a, n, l in herdados_rot:
            print(f'  achado na fonte: cabeçalho herdado (fora do exit) · {nome_a}:{n}: {l}')
        if introduzidos:
            falhas.append(
                f'cabeçalho de peça pública é rótulo, não tese: {len(introduzidos)} '
                f'cabeçalho(s) com padrão de rótulo entram no universo, e a isenção '
                f'estrutural cobre só FAQ, Bio, Índice, Sumário, Referências e Anexo')
        # C1(b)4 · remover o H1 não é alternativa a escrevê-lo bem
        sem_titulo = sem_h1(pecas)
        print(f'peças sem H1: {len(sem_titulo)} (teto 0) | grep -c \'^# \' por peça')
        for nome_a in sem_titulo:
            print(f'  peça sem H1: {nome_a}')
            falhas.append(f'peça sem H1: {nome_a}')

        # consertos 4, 5, r14b-1 · bastidor no arquivo que o dono abre
        vaz = bastidor_na_peca_publica(pecas)
        print(f'linhas de bastidor na peça pública: {len(vaz)} (teto 0) | tabela de '
              f'destino de dado, veredito do gate, contagem desdobrada e saída literal '
              f'moram em conferencia/')
        for nome_a, n, tipo, l in vaz:
            print(f'  bastidor na peça: {nome_a}:{n}: {tipo} · {l}')
        if vaz:
            falhas.append(
                f'bastidor na peça pública: {len(vaz)} linha(s) de auto-avaliação ou '
                f'diário de trabalho no arquivo que o dono abre; mova a tabela de '
                f'destino, o veredito e a saída literal pra conferencia/')

    declarado = int(m_lote.group(1)) if m_lote else 0
    # (b)10 · o lote da régua é o que está NA PEÇA, e os dois números batem.
    # Variação escrita e jogada fora não conta: quem quiser mostrá-la marca a
    # linha `descartada, não publicada` e ela sai da contagem dos dois lados.
    descartadas = sum(1 for l in linhas if RX_DESCARTADA.search(l))
    conta = declarado - descartadas
    if not motivo_univ:
        print(f'títulos na peça: {n_pecas} · na checagem: {conta} | '
              f'markdown por grep -cE \'^#{{1,4}} |^\\*\\*Slide|^Slide [0-9]\', '
              f'html por <title>/<h1>/<h2>/<h3>, pptx por <a:t> do primeiro shape '
              f'de cada slide | ' + ' '.join(n for n, _, _ in detalhe_univ))
    if descartadas:
        print(f'  variações marcadas `descartada, não publicada`: {descartadas} '
              f'(fora da contagem dos dois lados)')
    if not motivo_univ and n_pecas != conta:
        falhas.append(
            f'títulos na peça: {n_pecas} · na checagem: {conta} (os dois têm que bater; '
            f'variação que não foi publicada sai marcada `descartada, não publicada`)')

    # 5b · consentimento, marcador longo, número de terceiro e afirmação sem
    # saída crua, sobre a PEÇA PÚBLICA. O bastidor (RELATO, handoff, checagem,
    # notas, furos, inventário) carrega por regra a saída crua do grep de nomes,
    # o porquê de cada pendência e o número que ainda falta: cobrar dele o gate
    # público reprova a entrega que obedeceu à régua. O lint roda em todos.
    todas_md_pasta = sorted(base.glob('*.md'))
    todas = publicas(todas_md_pasta)
    # R13 · o arquivo INTERNO do dono sai da régua de nome e é impresso como tal.
    # Na fila do dia e no dossiê da call o nome é a coluna que faz o arquivo
    # servir: a dona responde no WhatsApp por nome, e `contato A` obrigava ela a
    # abrir um segundo arquivo pra descobrir quem era.
    internos = [f for f in todas_md_pasta
                if not RX_BASTIDOR.match(f.name) and arquivo_interno_do_dono(f)]
    print(f'arquivos internos do dono (nome permitido): {len(internos)} | '
          f'a anonimização é da peça pública')
    for f in internos:
        print(f'  uso interno: {f.name}')
    if insumos:
        cands = conferir_nomes = candidatos_a_nome(todas, insumos, perfil)
        # o destinatário sai isento antes do teste de origem, como no passo 1:
        # o nome de quem recebe a mensagem vem da caixa de entrada por definição
        dest = destinatarios(todas)
        privados = [n for n, d in cands.items()
                    if n not in dest and d['privado'] and not d['autorizado']]
        print(f'nomes candidatos achados pelo script: {len(conferir_nomes)} · '
              f'de conversa privada sem autorização: {len(privados)} (teto 0)')
        for nome in sorted(cands):
            d = cands[nome]
            marca = 'destinatário' if nome in dest else 'terceiro citado'
            print(f'  {nome} · na peça: {len(d["peca"])} · classificação: {marca} · '
                  f'autorização no insumo: {"sim" if d["autorizado"] else "não"} · '
                  f'mensagem privada: {"sim" if d["privado"] else "não"}')
        for nome in privados:
            if texto_fonte and re.search(
                    r'(?<![0-9A-Za-zÀ-ÿ_])' + re.escape(nome) + r'(?![0-9A-Za-zÀ-ÿ_])',
                    texto_fonte):
                print(f'  achado na fonte: nome {nome} · {Path(fonte).name}')
                continue
            falhas.append(f'nome de conversa privada em peça pública: {nome}')
    else:
        print('nomes candidatos achados pelo script: sem --insumos (passe a pasta de '
              'insumos do dono junto do --conferir)')

    # B(a)1 · número que o perfil marca como não confirmado não entra na peça
    # pública, com ou sem a ressalva ao lado: o leitor lê o número primeiro.
    if perfil and Path(perfil).exists():
        marcados = numeros_marcados_no_perfil(perfil)
        publicados = []
        # R12C2(a)2 · a fala que o dono vai gravar é copy publicada com atraso:
        # o que está na lista de falas vira áudio no ar, e o vídeo não tem onde
        # carregar a ressalva. PEDIDO-DE-GRAVACAO, roteiro e fala entram no gate
        # do número não confirmado mesmo quando o nome do arquivo os isentaria.
        alvo_num = list(publicas(sorted(base.glob('*.md'))))
        gravacao = [f for f in sorted(base.glob('**/*.md'))
                    if RX_PECA_DE_GRAVACAO.match(f.name) and f not in alvo_num]
        if gravacao:
            print(f'peças de gravação no gate do número: {len(gravacao)} '
                  f'(roteiro e lista de falas viram áudio no ar) | '
                  + ', '.join(f.name for f in gravacao))
        for token, valor, unidade, moeda, n_perfil, linha_perfil in marcados:
            # PENDENTE-r14: procura o número COM a unidade/moeda que o perfil lhe
            # deu. Dígito solto na peça (série, faixa, RIR) não casa; só o token
            # inteiro (`6 semanas`, `R$ 63`) reprova.
            if moeda:
                rx = re.compile(r'R\$\s*' + re.escape(valor) + r'(?![\w])', re.I)
            elif unidade:
                rx = re.compile(r'(?<![\w,.])' + re.escape(valor) + r'\s*'
                                + re.escape(unidade) + r'\b', re.I)
            else:
                rx = re.compile(r'(?<![\w,.])' + re.escape(valor) + r'(?![\w])')
            # conserto extenso · além do dígito, caça a forma por extenso do MESMO
            # número marcado quando ele carrega uma unidade de tempo/quantidade.
            # `[A CONFIRMAR: 6 semanas]` no perfil e "seis semanas" na peça reprova
            # igual ao dígito. Só quando há unidade: extenso solto ("seis") é ruído.
            rx_extenso = None
            formas_ext = DIGITO_PARA_EXTENSO.get(valor)
            if formas_ext and unidade:
                alt = '|'.join(re.escape(e) for e in formas_ext)
                rx_extenso = re.compile(
                    r'(?<![\wà-ÿ])(?:' + alt + r')\s+(?:' + RX_UNIDADE_EXTENSO
                    + r')\b', re.I)
            for f in alvo_num + gravacao:
                achou = False
                for n, l in enumerate(linhas_de(f), 1):
                    if rx.search(l):
                        publicados.append((token, f.name, n, l.strip()[:140]))
                        achou = True
                        break
                    if rx_extenso and rx_extenso.search(l):
                        publicados.append((f'{token} (por extenso)', f.name, n,
                                           l.strip()[:140]))
                        achou = True
                        break
                if achou:
                    break
        print(f'números não confirmados no perfil: {len(marcados)} · publicados na '
              f'peça: {len(publicados)} | grep -nE \'\\[A CONFIRMAR\' '
              f'{Path(perfil).name} e grep -nF de cada valor COM a unidade nas peças')
        for token, valor, unidade, moeda, n_perfil, linha_perfil in marcados:
            print(f'  marcado no perfil: {Path(perfil).name}:{n_perfil}: {linha_perfil}'
                  f' · alvo: "{token}"')
        for token, nome_a, n, l in publicados:
            print(f'  número não confirmado na peça: {token} · {nome_a}:{n}: {l}')
            falhas.append(f'número não confirmado na peça: {token} ({nome_a}:{n})')

    longos = marcadores_longos(todas)
    herdados = 0
    print(f'marcadores acima de {TETO_PALAVRAS_MARCADOR} palavras: {len(longos)} (teto 0)')
    for arq, n, npal, dentro in longos:
        literal = f'[{dentro}]'
        onde = mapa_fonte.get(literal)
        if onde is None and texto_fonte and literal in texto_fonte:
            onde = Path(fonte).name
        if onde:
            herdados += 1
            print(f'  achado na fonte: marcador longo ({npal} palavras) · {arq}:{n} · '
                  f'{onde}')
            continue
        print(f'  marcador longo ({npal} palavras): {arq}:{n}: {literal}')
        falhas.append(f'marcador longo ({npal} palavras): {arq}:{n}')
    if fonte:
        print(f'  herdados da fonte (fora do exit): {herdados} · introduzidos por esta '
              f'conversão: {len(longos) - herdados}')

    terceiros = numeros_de_terceiro(todas)
    # (b)1 · linha que já vinha da fonte não é número que esta entrega introduziu
    novos = [t for t in terceiros
             if not (texto_fonte and t['texto'].strip() and t['texto'].strip() in texto_fonte)]
    for t in terceiros:
        if t not in novos:
            print(f'  achado na fonte: número de terceiro · {t["arquivo"]}:{t["linha"]} · '
                  f'{Path(fonte).name}')
    com_trecho = sum(1 for t in novos if t['trecho'])
    com_url = sum(1 for t in novos if t['url'] and t['data'])
    print(f'números de terceiro: {len(novos)} · com trecho literal: {com_trecho} · '
          f'com URL completa: {com_url}')
    for t in novos:
        if not (t['trecho'] and t['url'] and t['data']):
            print(f'  sem a tripla completa: {t["arquivo"]}:{t["linha"]}: {t["texto"]}')
    if not (len(novos) == com_trecho == com_url):
        falhas.append(f'números de terceiro: {len(novos)} · com trecho literal: '
                      f'{com_trecho} · com URL completa: {com_url} (os três têm que bater)')

    soltas = afirmacoes_sem_saida([f for f in todas if f.name != 'checagem-titulos.md'])
    print(f'afirmações de verificação sem saída colada: {len(soltas)} (teto 0)')
    for arq, n, txt in soltas:
        print(f'  afirmação de verificação sem saída colada: {arq}:{n}: {txt}')
        falhas.append(f'afirmação de verificação sem saída colada: {arq}:{n}')

    # 5c · (b)6 · HTML entregue é HTML que abre. Template não renderizado vira
    # `{{` na tela do dono, e um fragmento sem <html> não abre no navegador.
    htmls = sorted(base.glob('*.html'))
    for f in htmls:
        txt_html = ler(f)
        n_chaves = txt_html.count('{{')
        tem_abre = '<html' in txt_html.lower()
        tem_fecha = '</html>' in txt_html.lower()
        print(f'{f.name} · {{{{ não renderizado: {n_chaves} (teto 0) · <html: '
              f'{"sim" if tem_abre else "não"} · </html>: '
              f'{"sim" if tem_fecha else "não"} | grep -c \'{{{{\' {f.name}')
        if n_chaves or not (tem_abre and tem_fecha):
            falhas.append(f'html não renderizado: {f.name}')

    # C1(b)5 · o .html de render é a peça que o dono publica, e entra no lint.
    # Uma entrega declarou `arquivos linteados: 6 · exit 0: 6` sem o preview,
    # que reprovava; outra fez o preview passar reescrevendo a copy da fonte
    # dentro do gerador. A peça não some da contagem, e o render não reescreve.
    lintmod_html = carregar_lint(lint_path)
    for f in htmls:
        if RX_BASTIDOR.match(f.name):
            continue
        texto_render = _texto_limpo(ler(f))
        code_h, saida_h, _ = rodar_lint(
            lintmod_html, lintmod_html.strip_code_blocks(texto_render), f.name)
        print(f'arquivo: {f.name} (texto extraído do render) · exit: {code_h}')
        if code_h != 0:
            for l in saida_h.splitlines():
                if l.strip().startswith('✗'):
                    print(f'  {l.strip()}')
            falhas.append(f'lint reprovou o texto extraído de {f.name} (exit {code_h}); '
                          f'quando a copy vier da fonte, cole `origem reprovada no lint` '
                          f'e devolva a linha à skill de origem, sem reescrever no render')

    # 5d · (a)4 · o binário é lido de volta antes de fechar. Um deck saiu com 20
    # slides e 0 acentos em 2.600 caracteres, com o .md de origem acentuado:
    # ninguém reabriu o arquivo que o dono recebe. Aqui o texto é extraído do
    # .pptx, linteado, e a contagem de acentos é comparada com a do .md de mesmo
    # nome-base. Zero no binário com origem acentuada reprova.
    lintmod_deck = carregar_lint(lint_path)
    for f in sorted(base.glob('*.pptx')):
        texto_deck = texto_do_pptx(f)
        slides_n = len(slides_do_pptx(f))
        ac_deck = sum(1 for l in texto_deck.splitlines() if RX_ACENTO.search(l))
        origem = base / (f.stem + '.md')
        ac_origem = (sum(1 for l in linhas_de(origem) if RX_ACENTO.search(l))
                     if origem.exists() else None)
        print(f'{f.name} · slides: {slides_n} · caracteres: {len(texto_deck)} · '
              f'linhas com acento: {ac_deck} | '
              f'unzip -p {f.name} \'ppt/slides/slide*.xml\' e grep -c \'[áéíóúâêôãõç]\' '
              f'sobre o texto extraído')
        if ac_origem is not None:
            print(f'  origem {origem.name} · linhas com acento: {ac_origem} | '
                  f'grep -c \'[áéíóúâêôãõç]\' {origem.name}')
        if len(texto_deck) > 200 and ac_deck == 0 and (ac_origem or 0) > 0:
            falhas.append(
                f'deck sem acentos: {f.name} tem {len(texto_deck)} caracteres e 0 linha '
                f'com acento, e a origem {origem.name} tem {ac_origem}; o português foi '
                f'perdido entre o .md e o binário que o dono recebe')
        code_deck, saida_deck, _ = rodar_lint(
            lintmod_deck, lintmod_deck.strip_code_blocks(texto_deck), f.name)
        print(f'arquivo: {f.name} (texto extraído) · exit: {code_deck}')
        if code_deck != 0:
            for l in saida_deck.splitlines():
                if l.strip().startswith('✗'):
                    print(f'  {l.strip()}')
            falhas.append(f'lint reprovou o texto extraído de {f.name} (exit {code_deck})')

    # R12C2(b)6 · a ausência de capacidade do ambiente se prova por comando,
    # igual a qualquer outro furo. Uma entrega declarou `sem acesso à web` e
    # fechou com zero fontes; o par, no mesmo ambiente, abriu três URLs. A
    # declaração custou metade do plano, e a skill autorizava o caminho sem
    # pedir prova. Agora a linha exige o comando colado em bloco cercado nas 3
    # linhas seguintes, inclusive quando a saída for o erro.
    # ── R13 · o relato é do dono, e abre pelo que ele recebeu ────────────────
    # "O relato tem que começar pelo que eu recebi e o que eu faço agora." Três
    # linhas antes de qualquer outra coisa, e a última seção junta as pendências
    # escritas como pergunta. Espalhar [A CONFIRMAR pelo miolo deixou a dona sem
    # chão, e ela lê melhor uma caixa com 3 perguntas curtas.
    relatos = relatos_da_pasta(base)
    print(f'relatos e handoffs na pasta: {len(relatos)} | ls {base}/RELATO.md '
          f'{base}/HANDOFF*')
    tem_resumo = False
    tem_lista_perguntas = False
    for f in relatos:
        ok_resumo, motivo = resumo_pro_dono(f)
        print(f'  {f.name} · resumo pro dono nas 3 primeiras linhas: '
              f'{"sim" if ok_resumo else "não"}'
              f'{"" if ok_resumo else " · " + motivo}')
        tem_resumo = tem_resumo or ok_resumo
        achou_secao, perguntas = secao_de_perguntas(f)
        print(f'  {f.name} · seção `Perguntas pra você`: '
              f'{"sim" if achou_secao else "não"} · perguntas escritas: {len(perguntas)}')
        if achou_secao:
            tem_lista_perguntas = True
    if relatos and not tem_resumo:
        falhas.append(
            'relato sem resumo pro dono: o RELATO ou o HANDOFF abre com as 3 linhas '
            '`Pronto: ... · Abra primeiro: ... · Falta você responder: ...`, antes de '
            'qualquer outra coisa')

    # cada [A CONFIRMAR da entrega tem pergunta correspondente na lista
    todos_md = sorted(base.glob('*.md'))
    pendencias = []
    for f in todos_md:
        for n, l in enumerate(linhas_de(f), 1):
            if RX_MARCADOR.search(l):
                pendencias.append((f.name, n, l.strip()[:120]))
    print(f'pendências marcadas na entrega: {len(pendencias)} | '
          f'grep -rn \'\\[A CONFIRMAR\' {base}')
    if pendencias and relatos and not tem_lista_perguntas:
        for nome, n, l in pendencias[:8]:
            print(f'  pendência sem pergunta na lista: {nome}:{n}: {l}')
        falhas.append(
            f'pendências espalhadas sem lista de perguntas: {len(pendencias)} marcadores '
            f'na entrega e nenhuma seção `Perguntas pra você` no relato; junte as '
            f'pendências numa lista só, cada uma escrita como pergunta')

    # ── R13 · nunca entregar comando pro dono ────────────────────────────────
    # "Eu opero tudo pelo Telegram." Ou a skill executa, ou ela diz o que pedir e
    # pra quem. A linha que manda rodar sai por exit, fora de bloco de bastidor.
    alvos_dono = [f for f in todos_md if not RX_BASTIDOR.match(f.name)] + relatos
    vistos = set()
    n_comandos = 0
    isentos_terceiro = 0
    for f in alvos_dono:
        if f in vistos:
            continue
        vistos.add(f)
        # PENDENTE-r14: o arquivo endereçado a quem publica é isento se abre com
        # as 3 linhas pro dono. O RELATO nunca é isento.
        if f.name != 'RELATO.md' and pedido_para_terceiro_valido(f):
            isentos_terceiro += 1
            print(f'  pedido a quem publica isento (abre com as 3 linhas pro dono): '
                  f'{f.name}')
            continue
        for n, l in comandos_pro_dono(f):
            print(f'  comando entregue ao dono: {f.name}:{n}: {l}')
            n_comandos += 1
            falhas.append(
                f'comando entregue ao dono: {f.name}:{n}; ou a skill executa, ou ela '
                f'diz o que pedir e pra quem')
    print(f'comandos entregues ao dono: {n_comandos} (teto 0) | fora de bloco cercado, '
          f'em RELATO, HANDOFF e peça')

    # ── R13 · jargão interno traduzido ou fora ───────────────────────────────
    # "Fase 7", "Tipo 5", "molde de antítese", "RASTREIO QUEBRADO", "PUV": nada
    # disso significa alguma coisa pro dono. Ou vem a glosa de até 4 palavras ao
    # lado, ou o termo sai do texto dele.
    n_jargao = 0
    for f in sorted(vistos, key=lambda x: x.name):
        for n, termo, l in jargao_sem_glosa(f):
            print(f'  jargão sem tradução: {f.name}:{n}: {termo} · {l}')
            n_jargao += 1
            falhas.append(f'jargão sem tradução: {termo} em {f.name}:{n}')
    print(f'jargão interno sem glosa: {n_jargao} (teto 0) | lista fechada, glosa de até '
          f'4 palavras ao lado')

    # ── R13 · caixa alta no título ───────────────────────────────────────────
    palavras_isentas = set(SIGLAS_COMUNS)
    m_chave = re.findall(r'palavra-chave\s*:\s*([A-Z0-9]{2,})', texto)
    palavras_isentas |= {w.upper() for w in m_chave}
    gritos_conf = []
    for f in sorted(vistos, key=lambda x: x.name):
        if RX_BASTIDOR.match(f.name):
            continue
        for n, l in enumerate(linhas_de(f), 1):
            if not RX_TITULO_PECA.match(l):
                continue
            prop = caixa_alta_demais(l, palavras_isentas)
            if prop is not None:
                gritos_conf.append((f.name, n, l.strip(), prop))
    arq_tit_conf = caminho_de_bastidor(base, 'titulos.txt')
    if arq_tit_conf.exists():
        for n, l in enumerate(linhas_de(arq_tit_conf), 1):
            if not l.strip():
                continue
            prop = caixa_alta_demais(l, palavras_isentas)
            if prop is not None:
                gritos_conf.append(('titulos.txt', n, l.strip(), prop))
    for f in sorted(base.glob('*.html')) + sorted(base.glob('*.pptx')):
        titulos_bin = (titulos_de_html(f) if f.suffix == '.html'
                       else slides_do_pptx(f))
        for i, t in enumerate(titulos_bin, 1):
            prop = caixa_alta_demais(t, palavras_isentas)
            if prop is not None:
                gritos_conf.append((f.name, i, t, prop))
    print(f'títulos em caixa alta: {len(gritos_conf)} (teto 0) | 8+ letras e 80%+ em '
          f'maiúscula; sigla de até 6 letras e palavra-chave de CTA fora da conta')
    for arq, n, l, prop in gritos_conf:
        print(f'  título em caixa alta: {arq}:{n}: {l} ({round(prop * 100)}% maiúscula)')
        falhas.append(f'título em caixa alta: {l}')

    relato_md = base / 'RELATO.md'
    if relato_md.exists():
        linhas_rel = linhas_de(relato_md)
        sem_prova = []
        for i, l in enumerate(linhas_rel):
            if not RX_AUSENCIA_DE_CAPACIDADE.search(l):
                continue
            if RX_CERCA.match(l):
                continue
            seguintes = linhas_rel[i + 1:i + 4]
            if not any(RX_CERCA.match(x) for x in seguintes):
                sem_prova.append((i + 1, l.strip()[:140]))
        print(f'afirmações de ausência de capacidade sem comando colado: {len(sem_prova)} '
              f'(teto 0) | grep -nEi \'sem acesso|sem busca|ambiente sem|não tenho '
              f'acesso|indisponível\' RELATO.md')
        for n, l in sem_prova:
            print(f'  ausência sem comando: RELATO.md:{n}: {l}')
            falhas.append(
                f'afirmação de ausência sem comando colado: RELATO.md:{n}; rode a busca, '
                f'cole o comando e a saída literal em bloco cercado, o erro incluso')

    # 5e · (b)4 · todo `<arquivo>: N bytes` declarado no RELATO sai de wc -c
    declarados = bytes_declarados(base)
    print(f'tamanhos declarados no relato: {len(declarados)} | wc -c de cada um, '
          f'tolerância 0')
    for nome, declarado, real, onde in declarados:
        print(f'  {onde}: {nome}: declarado {declarado} · wc -c {real}')
        if declarado != real:
            falhas.append(f'bytes redigitados: {onde} declara {nome} com {declarado} '
                          f'bytes e o wc -c devolve {real}')

    # 6 · exit 0 em TODO entregável, RELATO incluso, e é a última coisa.
    # (b)5 · o RELATO é o último arquivo escrito, então é o último linteado, e o
    # exit dele sai em linha própria, no fim: RELATO escrito depois do lint e
    # nunca relintado foi o que deixou três entregas argumentarem contra a régua
    # usando a palavra que ela proíbe.
    # PENDENTE-r14 · número por extenso em campo numérico (célula de tabela,
    # linha de valor monetário, fase numerada). O gate de número não confirmado
    # empurrava o motor a escrever `dois` na tabela e `seis reais por dia` na
    # coluna de verba pra passar; a peça piorava pra escapar de um gate que não
    # era sobre ela. Numa coluna onde as irmãs trazem algarismo, o extenso quebra
    # a leitura. Só conta em linha de tabela de dados ou de valor monetário.
    # A regra que não pega falso positivo: extenso reprova só quando a MESMA
    # coluna traz algarismo em outra célula (formato misto na coluna que a
    # pessoa varre), ou numa linha de valor monetário com R$/reais. "campo dois"
    # numa coluna sem número nenhum é rótulo, não campo numérico, e não conta.
    extenso_em_campo = []
    RX_DIGITO_CELULA = re.compile(r'(?<![\w,.])\d')
    # o gate é sobre a PEÇA que o dono lê: bastidor (checagem, RELATO, handoff)
    # carrega o teste do nicho trocado, que cita frases da peça com "reais" ao
    # lado, e não é campo numérico da entrega.
    for f in md_da_entrega(base):
        if RX_BASTIDOR.match(Path(f).name):
            continue
        linhas_f = linhas_de(f)
        # mapeia, por tabela contígua, quais colunas trazem algarismo
        i = 0
        while i < len(linhas_f):
            if not (RX_LINHA_TABELA.match(linhas_f[i])
                    and not RX_SEPARADOR_TABELA.match(linhas_f[i])):
                i += 1
                continue
            bloco = []
            j = i
            while j < len(linhas_f) and RX_LINHA_TABELA.match(linhas_f[j]):
                if not RX_SEPARADOR_TABELA.match(linhas_f[j]):
                    bloco.append((j + 1, linhas_f[j]))
                j += 1
            # colunas com algarismo em alguma célula
            col_com_digito = set()
            for _, l in bloco:
                for c, cel in enumerate(l.split('|')):
                    if RX_DIGITO_CELULA.search(cel):
                        col_com_digito.add(c)
            for n_l, l in bloco:
                for c, cel in enumerate(l.split('|')):
                    if c in col_com_digito:
                        m = RX_NUM_EXTENSO.search(cel)
                        if m:
                            extenso_em_campo.append(
                                (f.name, n_l, m.group(0), l.strip()[:120]))
                            break
            i = j
        # valor monetário escrito por extenso: o extenso tem que SER o valor
        # ("doze reais", "R$ doze"), não um extenso qualquer numa linha que também
        # cita um preço. `Doze semanas ... R$ 1.497` é período de tempo, não campo
        # monetário, e o extenso ali é prosa legítima.
        for n, l in enumerate(linhas_f, 1):
            if RX_LINHA_TABELA.match(l):
                continue
            m = RX_EXTENSO_MONETARIO.search(l)
            if m:
                palavra = m.group('ext') or m.group('ext2')
                extenso_em_campo.append((f.name, n, palavra, l.strip()[:120]))
    print(f'número por extenso em campo numérico: {len(extenso_em_campo)} (teto 0) | '
          f'coluna com algarismo em outra célula, ou linha de valor monetário')
    for nome, n, palavra, l in extenso_em_campo:
        print(f'  número por extenso em campo numérico: {nome}:{n}: {palavra} · {l}')
        falhas.append(f'número por extenso em campo numérico: {palavra} ({nome}:{n})')

    lintmod = carregar_lint(lint_path)
    # PENDENTE-r14: o lint da pasta inclui conferencia/*.md. O --conferir
    # declarava exit 0 num checagem-titulos.md que o próprio lint reprova (o
    # travessão em conferencia/checagem-titulos.md:15 do outreach). Gate que
    # aprova o que o lint reprova ensina que o lint é opcional. Os arquivos que
    # a PRÓPRIA execução do gate captura (conferir.txt, conferir.ultimo.txt)
    # ficam fora: eles são a saída literal do gate, não copy escrita à mão.
    RX_SAIDA_DO_GATE = re.compile(r'^conferir[\w.\-]*\.txt$', re.I)  # conserto 8: pega conferir.txt, conferir.ultimo.txt e conferir.ultimo-check.txt
    conf_md = [f for f in sorted((base / SUBPASTA_BASTIDOR).glob('*.md'))
               if not RX_SAIDA_DO_GATE.match(f.name)]
    entregaveis = sorted(set(md_da_entrega(base) + list(base.glob('*.json'))
                             + list((base / SUBPASTA_BASTIDOR).glob('*.json'))
                             + conf_md))
    relatos = [f for f in entregaveis if f.name == 'RELATO.md']
    ordem = [f for f in entregaveis if f.name != 'RELATO.md'] + relatos
    for f in ordem:
        # --ignore-code-blocks: o bloco citado num veredito não é copy da peça
        code, saida, _ = rodar_lint(lintmod, lintmod.strip_code_blocks(ler(f)), f.name)
        if f.name == 'RELATO.md':
            print(f'RELATO.md · exit: {code}')
        else:
            print(f'arquivo: {f.name} · exit: {code}')
        if code != 0:
            for l in saida.splitlines():
                if l.strip().startswith('✗'):
                    print(f'  {l.strip()}')
            falhas.append(f'lint reprovou {f.name} (exit {code})')

    if falhas:
        print('\nREPROVA, e a entrega não sai:')
        for f in falhas:
            print(f'  x {f}')
        # B(b)5 · uma entrega rodou, viu a reprova, escreveu os dois motivos no
        # relato e entregou assim mesmo. A honestidade é exemplar e a entrega
        # continua reprovada, então a frase fecha a saída.
        print('exit diferente de 0 não é entrega, mesmo com relato honesto')
        return 1
    print('\nconferência ok: a entrega sai.')
    return 0


# ── selftest ─────────────────────────────────────────────────────────────────
def selftest():
    import tempfile

    # R13 · as 3 linhas do dono abrem todo RELATO da entrega
    RESUMO = ('Pronto: a peça saiu.\n'
              'Abra primeiro: peca.md\n'
              'Falta você responder: nada\n\n')

    def chk_em(pasta):
        """R13 · o checagem-titulos.md mora em conferencia/, nunca na raiz."""
        return garantir_conferencia(pasta) / 'checagem-titulos.md'
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        # o lint precisa estar ao lado, como fica na skill
        fonte_lint = AQUI / 'lint_copy.py'
        assert fonte_lint.exists(), f'lint_copy.py ausente em {AQUI}'

        # caso 1: limpo, exit 0
        peca = d / 'peca.md'
        peca.write_text(
            '# Peça\n\nToda mulher que parou por dor no joelho, veja isto.\n'
            'Fale comigo e eu te mando o caminho.\n', encoding='utf-8')
        titulos = d / 'titulos.txt'
        titulos.write_text('Toda mulher que parou por dor no joelho, veja isto.\n'
                           'O joelho avisa no dia 12 e você troca o treino por descanso.\n',
                           encoding='utf-8')
        teses = d / 'teses.txt'
        teses.write_text('recorte por causa\nrecaida tem prazo\n', encoding='utf-8')
        perfil = d / 'dono.md'
        perfil.write_text('- campo um\n- campo dois\ntexto solto\n- campo tres\n',
                          encoding='utf-8')
        ins = d / 'insumos'
        ins.mkdir()
        (ins / 'aula.md').write_text(
            'linha\nQuem quiser, manda BASE40 no WhatsApp que eu mando o link.\n'
            'Marcia, 52, caso autorizado pelo dono em 2026-01-01.\n', encoding='utf-8')

        out = []
        args = argparse.Namespace(
            peca=[str(peca)], titulos=str(titulos), teses=str(teses),
            insumos=str(ins), perfil=str(perfil), ressalva=None,
            nomes=None, lint=str(fonte_lint))
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'caso limpo devia sair 0, saiu {code}: {falhas}'
        assert 'títulos no lote: 2' in txt, txt
        assert 'campos no perfil: 3' in txt, txt
        assert 'teses distintas: <preencher> | de 2 no lote' in txt, txt
        # (b)9 · a matriz de TODOS os pares sai impressa, com as 3 respostas
        assert 'matriz de pares de teses: 1 pares' in txt, txt
        assert ('recorte por causa vs recaida tem prazo | sujeito igual? <preencher> | '
                'predicado igual? <preencher> | conta como 1? <preencher>') in txt, txt
        # (a)1 · uma linha por unidade, com a frase copiada inteira
        assert ('t1 | Toda mulher que parou por dor no joelho, veja isto. | '
                'substantivo trocado: <preencher> | sobrevive?') in txt, txt
        assert '(última frase de bloco) | Fale comigo e eu te mando o caminho.' in txt, txt
        assert 'unidades no teste do nicho trocado: 3' in txt, txt
        assert 'BASE40' in txt, 'a palavra-chave do CTA tem que sair dos insumos'
        assert 'marcadores na peça: 0' in txt, txt
        assert f'títulos de abertura: 2 · reescritos: {PLACEHOLDER}' in txt, txt
        assert 'gatilhos fora da lista fechada: <preencher>' in txt, txt
        assert 'com inimigo ou inversão: <preencher> de 2' in txt, txt
        assert 'falas de terceiro: <preencher>' in txt, txt
        assert 'arquivo: peca.md · exit: 0' in txt, txt
        # (a)1: uma linha de nicho trocado por UNIDADE (título + fecho de bloco)
        assert txt.count('| sobrevive? <preencher>') == 3, txt

        # caso 2: molde acima do teto (2 títulos em duas orações) reprova
        titulos.write_text('Nao e sorte, e conta.\n'
                           'Ela tentou tres vezes e sempre doeu. Faltava a fase 1.\n',
                           encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('molde' in f for f in falhas), f'{code} {falhas}'
        assert 'molde de antítese nos títulos: 2' in txt, txt

        # caso 2b · molde de antítese com VÍRGULA + negação ("X, não Y"): o lint
        # só pega o molde com PONTO, e o "duas orações" também. Sem esta detecção
        # a inversão por vírgula escapava e o gate passava o que devia reprovar.
        # 4 títulos de contraste (não/nunca/e não) → conta 4, acima do teto 1.
        titulos.write_text(
            'Sequência salva o joelho, não força bruta\n'
            'É ordem certa, não milagre\n'
            'Treine em casa, nunca na academia\n'
            'Comece devagar, e não desista\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('molde' in f for f in falhas), f'{code} {falhas}'
        assert 'molde de antítese nos títulos: 4' in txt, txt

        # caso 2c · "não"/"nunca" que NÃO é contraste de duas metades não conta.
        # Vírgula sem negação, ou negação no meio de uma oração só, ficam de fora.
        titulos.write_text(
            'Como voltar a treinar sem dor depois dos 40\n'
            'O treino que não machuca seu joelho\n'
            '3 erros que você não sabe que comete\n'
            'Como treinar sem dor no joelho\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert 'molde de antítese nos títulos: 0' in txt, txt
        assert not any('molde' in f for f in falhas), f'nao pode reprovar por molde: {falhas}'

        # caso 3: marcador no miolo reprova; em campo, não
        peca.write_text(
            '# Peça\n\nO protocolo dura [A CONFIRMAR: semanas] e melhora a subida.\n'
            '\n**Dados fornecidos**\n\n- Prazo: [A CONFIRMAR: semanas]\n',
            encoding='utf-8')
        titulos.write_text('Um titulo limpo qualquer aqui.\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('miolo' in f for f in falhas), f'{code} {falhas}'
        assert 'marcadores na peça: 2 · em posição de campo: 1 · no miolo de frase: 1' in txt, txt

        # caso 4: ressalva repetida reprova
        peca.write_text('# Peça\n\nAvaliacao individual antes de comecar.\n'
                        'meio\nAvaliacao individual antes de comecar.\n', encoding='utf-8')
        args.ressalva = 'Avaliacao individual antes de comecar.'
        out = []
        code, falhas = montar(args, out)
        assert code == 1 and any('ressalva' in f for f in falhas), f'{code} {falhas}'
        assert 'ressalvas na peça: 2 (teto 1' in '\n'.join(out)
        args.ressalva = None

        # caso 5: nome sem autorização reprova; com autorização no insumo, passa
        peca.write_text('# Peça\n\nMarcia subiu a escada sem dor.\nRenata tambem.\n',
                        encoding='utf-8')
        nomes = d / 'nomes.txt'
        nomes.write_text('Marcia\n', encoding='utf-8')
        args.nomes = str(nomes)
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'Marcia tem autorizacao no insumo: {falhas}'
        assert 'Marcia · na peça: 1' in '\n'.join(out)
        assert 'autorização no insumo: sim' in '\n'.join(out)
        nomes.write_text('Marcia\nRenata\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 1 and any('Renata' in f for f in falhas), f'{code} {falhas}'
        assert 'Renata · na peça: 1' in '\n'.join(out)
        args.nomes = None

        # caso 6: lint reprovando a peça derruba a entrega
        peca.write_text('# Peça\n\nO metodo destrava tudo.\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 1 and any('lint reprovou' in f for f in falhas), f'{code} {falhas}'
        assert 'arquivo: peca.md · exit: 1' in '\n'.join(out)

        # caso 7 · (b)9: a matriz sai com TODOS os pares, N*(N-1)/2, e o número
        # de teses distintas fica em <preencher> pra ser a conta, não a contagem
        peca.write_text('# Peça\n\nlimpo\n', encoding='utf-8')
        teses.write_text('\n'.join(f'tese numero {i} distinta' for i in range(9)) + '\n',
                         encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert 'matriz de pares de teses: 36 pares' in txt, txt
        assert txt.count('| conta como 1? <preencher>') == 36, txt
        assert 'teses distintas: <preencher> | de 9 no lote' in txt, txt

        # caso 8: sem origem no disco, o CTA sai sem palavra
        vazia = d / 'vazia'
        vazia.mkdir()
        (vazia / 'nada.md').write_text('linha sem gatilho de cta\n', encoding='utf-8')
        args.insumos = str(vazia)
        out = []
        code, falhas = montar(args, out)
        assert 'sem origem no disco: CTA sai sem palavra' in '\n'.join(out)

        # caso 10 · (a)2: palavra-chave do CTA que não existe nos insumos reprova,
        # e a que existe sai com a origem em arquivo:linha
        args.insumos = str(ins)
        args.perfil = str(perfil)
        perfil.write_text('- campo um\n- campo dois\ntexto solto\n- campo tres\n'
                          '- automação de comentário para DM ligada\n', encoding='utf-8')
        teses.write_text('recorte por causa\nrecaida tem prazo\n', encoding='utf-8')
        peca.write_text('# Peça\n\nComenta PROTOCOLO que eu te mando as 3 fases.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('PROTOCOLO' in f for f in falhas), f'{code} {falhas}'
        assert 'palavra-chave inventada: PROTOCOLO' in txt, txt
        peca.write_text('# Peça\n\nComenta BASE40 que eu te mando as 3 fases.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'BASE40 existe no insumo: {falhas}'
        assert 'palavra-chave: BASE40 | origem: ' in txt, txt
        assert 'aula.md:2' in txt, txt
        # sigla comum não é palavra-chave, e CTA sem palavra sai declarado
        peca.write_text('# Peça\n\nMe chama no Direct e eu te mando o PDF.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, falhas
        assert 'palavra-chave: nenhuma (CTA sem palavra)' in '\n'.join(out), '\n'.join(out)

        # caso 11 · (a)2: palavra-chave sem automação declarada no perfil reprova
        perfil.write_text('- campo um\n- campo dois\n- campo tres\n', encoding='utf-8')
        peca.write_text('# Peça\n\nComenta BASE40 que eu te mando as 3 fases.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 1 and any('automação' in f for f in falhas), f'{code} {falhas}'
        assert 'automação declarada no perfil: não' in '\n'.join(out)
        perfil.write_text('- campo um\n- campo dois\n- campo tres\n'
                          '- automação de comentário para DM ligada\n', encoding='utf-8')

        # caso 12 · (a)1: a ressalva conta sobre o LOTE, uma por arquivo já reprova
        d1, d2 = d / 'dia1.md', d / 'dia2.md'
        frase = 'Avaliacao individual antes de comecar.'
        d1.write_text(f'# Dia 1\n\nconteudo\n{frase}\n', encoding='utf-8')
        d2.write_text(f'# Dia 2\n\nconteudo\n{frase}\n', encoding='utf-8')
        args.peca = [str(d1), str(d2)]
        args.ressalva = frase
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('lote inteiro' in f for f in falhas), f'{code} {falhas}'
        assert 'soma sobre as 2 peças do lote' in txt, txt
        d2.write_text('# Dia 2\n\nconteudo sem ressalva\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'uma ressalva no lote passa: {falhas}'
        args.ressalva = None
        args.peca = [str(peca)]

        # caso 13 · (b)9: duas teses que compartilham sujeito E predicado saem
        # na matriz como um par só, e é ele que abaixa o total
        peca.write_text('# Peça\n\nlimpo\n', encoding='utf-8')
        teses.write_text('pressa cobra joelho\npeso cobra joelho\nrecaida tem prazo\n',
                         encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert 'matriz de pares de teses: 3 pares' in txt, txt
        assert 'pressa cobra joelho vs peso cobra joelho | sujeito igual?' in txt, txt
        teses.write_text('recorte por causa\nrecaida tem prazo\n', encoding='utf-8')

        # caso 14 · marcador no html de render vira pixel: exit 1 antes de exportar
        html = d / 'preview.html'
        html.write_text('<div>Semanas de protocolo [A CONFIRMAR: nº exato]</div>\n',
                        encoding='utf-8')
        assert checar_render(str(html)) == 1, 'marcador no render tinha que reprovar'
        html.write_text('<div>Semanas de protocolo</div>\n', encoding='utf-8')
        assert checar_render(str(html)) == 0, 'render limpo tinha que passar'

        # C1(b)8 · daqui pra frente o piso declarado é conferido contra o
        # grep -c '^- ' do perfil, então o perfil das pastas de --conferir
        # passa a ter os 29 campos que as fixtures declaram.
        perfil.write_text('\n'.join(f'- campo {i}' for i in range(1, 29))
                          + '\n- automação de comentário para DM ligada\n',
                          encoding='utf-8')

        # caso 15 · --conferir: sem checagem-titulos.md não há entrega
        saida = d / 'saida'
        saida.mkdir()
        assert conferir(str(saida), fonte_lint) == 1, 'ausência do arquivo tinha que reprovar'

        # caso 16 · --conferir: <preencher> sobrando reprova
        (saida / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')
        base_ok = (
            'títulos no lote: 1\n'
            'campos no perfil: 29 · valores desdobrados: 64 · usados: 16 · '
            'descartados com motivo: 48\n'
            'Um titulo | substantivo trocado: joelho → planilha | '
            'sobrevive à troca de nicho? nao\n'
            'títulos de abertura: 1 · reescritos: 1\n')
        chk = chk_em(saida)
        chk.write_text(base_ok + 'falas de terceiro: <preencher>\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, '<preencher> sobrando tinha que reprovar'
        chk.write_text(base_ok, encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, 'checagem preenchida tinha que passar'

        # caso 17 · --conferir (a)4: `sim` de nicho acima de 1 reprova
        chk.write_text(base_ok.replace('títulos no lote: 1', 'títulos no lote: 3')
                       + 'B | substantivo trocado: joelho → planilha | sobrevive à troca de nicho? sim\n'
                         'C | substantivo trocado: treino → estudo | sobrevive à troca de nicho? sim\n',
                       encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, 'dois `sim` de nicho tinham que reprovar'

        # caso 18 · --conferir (a)5: reescritos 0 em lote acima de 3 sem motivo.
        # A peça carrega os 8 títulos de verdade, senão quem reprova é (b)10.
        (saida / 'peca.md').write_text(
            '\n\n'.join(f'# Titulo {i}\n\nlimpo' for i in range(1, 9)) + '\n',
            encoding='utf-8')
        oito = (base_ok.replace('títulos no lote: 1', 'títulos no lote: 8')
                .replace('títulos de abertura: 1 · reescritos: 1',
                         'títulos de abertura: 8 · reescritos: 0'))
        chk.write_text(oito, encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, 'reescritos 0 sem motivo tinha que reprovar'
        # C1(b)3 · a linha de motivo sozinha deixou de bastar: sem nenhuma
        # `reescrito de:` na pasta, a R7 não rodou, e agora isso é exit 1
        motivo18 = ('nenhum reescrito porque: os 8 nasceram do verbatim · '
                    'título mais fraco do lote: Um titulo\n')
        chk.write_text(oito + motivo18, encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, \
            'motivo sem nenhuma versão morta tinha que reprovar'
        chk.write_text(oito + motivo18 + 'reescrito de: Um titulo qualquer\n',
                       encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, \
            'motivo com a versão morta colada tinha que passar'
        oito = oito + motivo18 + 'reescrito de: Um titulo qualquer\n'

        # caso 18b · (b)10: `títulos na peça` e `na checagem` têm que bater, e a
        # variação descartada sai da contagem dos dois lados
        chk.write_text(oito.replace('títulos no lote: 8', 'títulos no lote: 11')
                       + 'nenhum reescrito porque: os 8 nasceram do verbatim · '
                         'título mais fraco do lote: Um titulo\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, '11 declarados com 8 na peça reprova'
        chk.write_text(oito.replace('títulos no lote: 8', 'títulos no lote: 11')
                       + 'variacao A | descartada, não publicada\n'
                         'variacao B | descartada, não publicada\n'
                         'variacao C | descartada, não publicada\n'
                         'nenhum reescrito porque: os 8 nasceram do verbatim · '
                         'título mais fraco do lote: Um titulo\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, \
            'as 3 variações marcadas descartadas fecham 11 menos 3 igual a 8'
        (saida / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')

        # caso 19 · --conferir (b)7 e (b)8: inventário sem os 4 inteiros, e
        # desdobramento menor que o piso
        chk.write_text(base_ok.replace(
            'campos no perfil: 29 · valores desdobrados: 64 · usados: 16 · '
            'descartados com motivo: 48', 'campos no perfil: ver INVENTARIO.md'),
            encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, 'referência cruzada tinha que reprovar'
        chk.write_text(base_ok.replace('valores desdobrados: 64', 'valores desdobrados: 16'),
                       encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, 'desdobrado < piso tinha que reprovar'

        # caso 20 · --conferir (b)6: peça com mais títulos que o lote declarado
        (saida / 'peca.md').write_text(
            '# Um titulo\n\nlimpo\n\n## Outro titulo\n\nlimpo\n', encoding='utf-8')
        chk.write_text(base_ok, encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, '2 títulos contra 1 tinha que reprovar'

        # caso 21 · --conferir (b)10: o lint roda em TODO .md e .json, RELATO incluso
        (saida / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')
        relato = saida / 'RELATO.md'
        relato.write_text('# Relato\n\n' + RESUMO + 'O metodo destrava tudo.\n',
                          encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, 'RELATO com falha dura tinha que reprovar'
        relato.write_text('# Relato\n\n' + RESUMO + 'O metodo abre o caminho.\n',
                          encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, 'RELATO limpo tinha que passar'
        # e o bloco de código citado não conta (--ignore-code-blocks)
        relato.write_text('# Relato\n\n' + RESUMO + 'O trecho reprovado:\n\n```\n'
                          'nao e sorte, e conta.\n```\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, 'citação em bloco não podia contar'

        # caso 22 · (a)1: o script acha o nome sozinho, sem --nomes. Nome de
        # conversa privada sem autorização reprova; o mesmo nome com autorização
        # no insumo, ou vindo de insumo que não é conversa privada, passa.
        args.peca = [str(peca)]
        args.nomes = None
        args.ressalva = None
        priv = ins / 'caixa-entrada.md'
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Simone, 51: "ja fiz pilates e parei. Serve pra mim?"\n',
                        encoding='utf-8')
        peca.write_text('# Peça\n\nSimone, 51 anos, me escreveu depois de ver o video.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('conversa privada' in f and 'Simone' in f
                                 for f in falhas), f'{code} {falhas}'
        assert 'Simone · na peça: 1' in txt and 'mensagem privada: sim' in txt, txt
        # Marcia vem da transcrição da aula (não é conversa privada) e passa
        peca.write_text('# Peça\n\nMarcia subiu a escada sem dor em seis semanas.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'nome fora de conversa privada tinha que passar: {falhas}'
        assert 'Marcia · na peça: 1' in txt and 'mensagem privada: não' in txt, txt
        # com autorização registrada no insumo privado, o nome sai autorizado
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Simone, 51: "ja fiz pilates e parei."\n'
                        '   caso autorizado pela dona em 2026-01-02\n', encoding='utf-8')
        peca.write_text('# Peça\n\nSimone, 51 anos, me escreveu depois de ver o video.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'nome autorizado tinha que passar: {falhas}'
        assert 'Simone · na peça: 1' in '\n'.join(out)
        # o nome do próprio dono nunca é terceiro citado
        peca.write_text('# Peça\n\nQuem conduz a turma e a Renata, ha 9 anos.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'o nome do dono nao pede autorizacao: {falhas}'
        assert 'nomes candidatos achados pelo script: 0' in '\n'.join(out)
        # bastidor não é peça pública: o nome mora no handoff por regra
        hand = d / 'HANDOFF-x.md'
        hand.write_text('# Handoff\n\nnomes nos insumos privados: Simone, Marcia\n',
                        encoding='utf-8')
        args.peca = [str(hand)]
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'nome no handoff nao reprova: {falhas}'
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Simone, 51: "ja fiz pilates e parei."\n', encoding='utf-8')
        args.peca = [str(peca)]

        # caso 23 · (a)2: marcador de campo com mais de 6 palavras reprova, e o
        # curto passa. O porquê da pendência vai pro handoff, não pra peça.
        peca.write_text(
            '# Peça\n\n**Dados fornecidos**\n\n'
            '- Prazo: [A CONFIRMAR: a aula de 29/09 fica gravada depois ou nao fica]\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('marcador longo' in f for f in falhas), f'{code} {falhas}'
        assert 'marcador longo (12 palavras)' in txt, txt
        peca.write_text('# Peça\n\n**Dados fornecidos**\n\n- Prazo: [A CONFIRMAR: semanas]\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'marcador curto tinha que passar: {falhas}'
        assert 'marcadores acima de 6 palavras: 0' in '\n'.join(out)

        # caso 24 · (b)10: número de terceiro sem a tripla completa reprova
        peca.write_text('# Peça\n\nA concorrente cobra R$ 2.900 pelo mesmo programa.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('números de terceiro' in f for f in falhas), f'{code} {falhas}'
        assert 'números de terceiro: 1 · com trecho literal: 0 · com URL completa: 0' in txt, txt
        peca.write_text(
            '# Peça\n\nA concorrente cobra R$ 2.900 pelo mesmo programa.\n'
            'trecho: "12 semanas por R$ 2.900" | url: https://exemplo.com/planos | '
            'consultado em: 04/09/2026\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'tripla completa tinha que passar: {falhas}'
        assert 'números de terceiro: 1 · com trecho literal: 1 · com URL completa: 1' in txt, txt

        # caso 25 · (b)4: afirmação de verificação sem a saída crua colada
        peca.write_text('# Peça\n\nConfirmei que o arquivo da faxina foi gravado na raiz.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('sem saída colada' in f for f in falhas), f'{code} {falhas}'
        assert 'afirmação de verificação sem saída colada: peca.md:3' in txt, txt
        peca.write_text('# Peça\n\nConfirmei que o arquivo da faxina foi gravado na raiz.\n\n'
                        '```\n-rw-r--r-- 1 dona dona 812 2026-09-04 faxina.md\n```\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'com a saida colada tinha que passar: {falhas}'
        assert 'afirmações de verificação sem saída colada: 0' in '\n'.join(out)
        peca.write_text('# Peça\n\nlimpo\n', encoding='utf-8')

        # caso 26 · --conferir com --insumos roda o consentimento de novo, e o
        # rótulo de seção ISENTO (a lista curta: FAQ, Bio, Índice, Sumário,
        # Referências, Anexo) não entra na contagem de títulos
        (saida / 'peca.md').write_text(
            '## FAQ\n\n# Um titulo de abertura\n\nSimone, 51 anos, escreveu.\n',
            encoding='utf-8')
        chk.write_text(base_ok, encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, 'sem --insumos o gate de nome nao roda'
        assert conferir(str(saida), fonte_lint, str(d), str(perfil)) == 1, \
            'nome de conversa privada tinha que reprovar no --conferir'
        (saida / 'peca.md').write_text('## FAQ\n\n# Um titulo de abertura\n\nlimpo\n',
                                       encoding='utf-8')
        assert conferir(str(saida), fonte_lint, str(d), str(perfil)) == 0, \
            'rotulo de secao isento nao conta como titulo'

        # caso 27 · (b)9: duas linhas de inventário com números diferentes na
        # mesma entrega reprovam com `inventário duplicado`; o mesmo número
        # repetido é o mesmo inventário e passa
        chk.write_text(base_ok, encoding='utf-8')
        lista = saida / 'lista-prospeccao.md'
        lista.write_text('Dados fornecidos: 17 · usados: 6\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, '17 contra 29 tinha que reprovar'
        chk.write_text(base_ok, encoding='utf-8')
        lista.write_text('Dados fornecidos: 29 · usados: 6\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, 'o mesmo numero e o mesmo inventario'
        lista.unlink()

        # caso 28 · (b)10: o mesmo rótulo do script com duas listas diferentes
        # reprova com `saída do script reescrita`; rótulo diferente passa
        chk.write_text(base_ok, encoding='utf-8')
        prosa = saida / 'notas.md'
        prosa.write_text('marcas de tempo: 47:09, 47:18, 53:02\n\n'
                         'marcas de tempo: 47:09, 47:18, 47:31\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 1, 'duas listas no mesmo rotulo reprovam'
        prosa.write_text('marcas de tempo: 47:09, 47:18, 53:02\n\n'
                         'recorte mais amplo (grep -n do bloco inteiro): '
                         '47:09, 47:18, 47:31\n', encoding='utf-8')
        assert conferir(str(saida), fonte_lint) == 0, 'rotulo diferente tinha que passar'
        prosa.unlink()

        # caso 29 · (b)4: sem --insumos e sem --nomes o script nunca imprime
        # zero; e o destinatário entra na contagem com a marca dele
        peca.write_text('# Peça\n\nSimone, tudo bem? Vi que voce parou o treino.\n',
                        encoding='utf-8')
        semflag = argparse.Namespace(
            peca=[str(peca)], titulos=None, teses=None, insumos=None, perfil=None,
            ressalva=None, nomes=None, lint=str(fonte_lint))
        out = []
        code, falhas = montar(semflag, out)
        txt = '\n'.join(out)
        assert code == 1 and any('NÃO CONFERIDO' in f for f in falhas), f'{code} {falhas}'
        assert 'nomes de pessoa na peça: NÃO CONFERIDO' in txt, txt
        assert 'nomes de pessoa na peça: 0\n' not in txt, txt
        # com insumos, a destinatária Simone conta, com a classificação ao lado
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Simone, 51: "ja fiz pilates e parei."\n'
                        '   caso autorizado pela dona em 2026-01-02\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert 'nomes de pessoa na peça: 1' in txt, txt
        assert 'classificação: destinatário, uso interno' in txt, txt
        # peça sem nenhum candidato imprime zero COM o motivo, nunca zero seco
        peca.write_text('# Peça\n\nToda mulher que parou por dor no joelho, veja isto.\n',
                        encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'peca limpa tinha que passar: {falhas}'
        assert ('nomes de pessoa na peça: 0 (nenhuma palavra capitalizada da peça bate '
                'com pessoa nos insumos)') in txt, txt

        # caso 30 · (b)6: universo vazio dispensa a tabela e nunca o fecho: as
        # linhas de título saem com 0 e o motivo, o bloco sai inteiro
        args.titulos = None
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'peca sem titulo tinha que passar: {falhas}'
        assert 'títulos no lote: 0' in txt, txt
        assert f'gatilhos fora da lista fechada: 0{MOTIVO_SEM_TITULO}' in txt, txt
        assert f'com inimigo ou inversão: 0{MOTIVO_SEM_TITULO} de 0' in txt, txt
        assert f'títulos de abertura: 0 · reescritos: 0{MOTIVO_SEM_TITULO}' in txt, txt
        assert 'falas de terceiro: <preencher>' in txt, txt
        assert 'campos no perfil: 29' in txt, 'o inventario sai com o numero real'
        args.titulos = str(titulos)

        # caso 31 · (b)1(i): o RELATO.md é bastidor. A régua manda colar nele a
        # saída crua da extração de nomes e a lista de furos; cobrar dele o gate
        # da peça pública reprovava justamente quem obedeceu. O lint continua
        # rodando sobre ele no --conferir (caso 21).
        rel = d / 'RELATO.md'
        rel.write_text(
            '# Relato\n\nnomes nos insumos privados: Simone, Marcia\n'
            'Prazo do caso: [DADO: o numero exato de semanas ainda nao veio do dono]\n'
            'A concorrente cobra R$ 2.900 pelo mesmo programa, segundo o print.\n'
            'Conferido: o grep voltou vazio.\n', encoding='utf-8')
        args.peca = [str(rel)]
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'o RELATO é bastidor e não responde pelo gate público: {falhas}'
        txt = '\n'.join(out)
        assert 'marcadores acima de 6 palavras: 0' in txt, txt
        assert 'números de terceiro: 0' in txt, txt
        assert 'afirmações de verificação sem saída colada: 0' in txt, txt
        assert 'nomes candidatos achados pelo script: 0' in txt, txt
        # a MESMA peça com nome de peça pública reprova, como sempre reprovou
        pub = d / 'resposta.md'
        pub.write_text('# Resposta\n\nA concorrente cobra R$ 2.900 pelo mesmo programa.\n',
                       encoding='utf-8')
        args.peca = [str(pub)]
        out = []
        code, falhas = montar(args, out)
        assert code == 1 and any('números de terceiro' in f for f in falhas), \
            f'a peça pública continua respondendo pelo gate: {code} {falhas}'

        # caso 32 · (b)1(ii): a isenção do destinatário tem que ser ALCANÇÁVEL.
        # Resposta a reclamação nomeando quem reclamou, nome vindo da caixa de
        # entrada: passa, com `classificação: destinatário`. Antes do conserto o
        # teste de origem privada rodava primeiro e o nome reprovava sempre.
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Claudia (aluna): "o grupo ficou 10 dias sem resposta"\n',
                        encoding='utf-8')
        resp = d / 'caso-claudia.md'
        resp.write_text(
            '# Resposta pronta pra copiar\n\n'
            'Claudia, tudo bem? Voce tem razao: o grupo ficou 10 dias sem resposta minha.\n'
            'Me diz uma coisa, qual horario da semana que vem funciona pra voce?\n',
            encoding='utf-8')
        args.peca = [str(resp)]
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 0, f'o destinatário nomeado tinha que passar: {falhas}'
        assert 'Claudia · na peça:' in txt and 'classificação: destinatário' in txt, txt
        assert 'mensagem privada: sim' in txt, txt
        # e terceiro citado da mesma caixa de entrada continua reprovando
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Claudia (aluna): "o grupo ficou 10 dias sem resposta"\n'
                        '2. Simone, 51: "ja fiz pilates e parei."\n', encoding='utf-8')
        resp.write_text(
            '# Resposta pronta pra copiar\n\n'
            'Claudia, tudo bem? A Simone passou pelo mesmo e hoje sobe a escada.\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 1 and any('Simone' in f for f in falhas), \
            f'terceiro citado da caixa de entrada continua reprovando: {code} {falhas}'
        assert not any('Claudia' in f for f in falhas), f'o destinatário não reprova: {falhas}'

        # caso 33 · (b)6: HTML entregue é HTML que abre
        saida2 = d / 'saida2'
        saida2.mkdir()
        (saida2 / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')
        chk_em(saida2).write_text(base_ok, encoding='utf-8')
        quebrado = saida2 / 'index.html'
        quebrado.write_text('<html><body><h1>{{titulo}}</h1></body></html>\n',
                            encoding='utf-8')
        assert conferir(str(saida2), fonte_lint) == 1, 'template nao renderizado reprova'
        quebrado.write_text('<div>fragmento sem casca</div>\n', encoding='utf-8')
        assert conferir(str(saida2), fonte_lint) == 1, 'html sem <html> nao abre e reprova'
        quebrado.write_text('<html><head><title>x</title></head><body>'
                            '<h1>Um titulo</h1></body></html>\n', encoding='utf-8')
        # (b)7 · o <title> e o <h1> do html entram no universo, então o lote
        # declarado deixa de ser o do .md sozinho
        chk_em(saida2).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 3'), encoding='utf-8')
        assert conferir(str(saida2), fonte_lint) == 0, 'html renderizado e inteiro passa'

        args.peca = [str(peca)]
        priv.write_text('Mensagens nao respondidas:\n'
                        '1. Simone, 51: "ja fiz pilates e parei."\n', encoding='utf-8')

        # caso 40 · (a)1: rótulo de estrutura no titulos.txt reprova. O universo
        # é o texto que o público lê (`Texto na tela`), nunca `Frame 1, Dia 2`.
        titulos.write_text('Frame 1, Dia 1\nFrame 2, Dia 1\nFrame 3, Dia 2\n'
                           'Voce parou de treinar e o joelho continua doendo.\n',
                           encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        txt = '\n'.join(out)
        assert code == 1 and any('rótulo de estrutura' in f for f in falhas), \
            f'rótulo de frame no titulos.txt tinha que reprovar: {code} {falhas}'
        assert 'rótulos de estrutura em titulos.txt: 3 de 4' in txt, txt
        titulos.write_text('Voce parou de treinar e o joelho continua doendo.\n'
                           'A pressa cobra no dia 12, e nao no dia 1.\n', encoding='utf-8')
        out = []
        code, falhas = montar(args, out)
        assert code == 0, f'texto na tela puro tinha que passar: {falhas}'
        titulos.write_text('Toda mulher que parou por dor no joelho, veja isto.\n'
                           'O joelho avisa no dia 12 e você troca o treino por descanso.\n',
                           encoding='utf-8')

        # caso 33 · (a)4: linha de nicho sem a coluna do substantivo reprova
        s33 = d / 's33'
        s33.mkdir()
        (s33 / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')
        c33 = chk_em(s33)
        sem_col = ('títulos no lote: 1\n'
                   'campos no perfil: 29 · valores desdobrados: 64 · usados: 16 · '
                   'descartados com motivo: 48\n'
                   'Um titulo | sobrevive à troca de nicho? nao\n'
                   'títulos de abertura: 1 · reescritos: 1\n')
        c33.write_text(sem_col, encoding='utf-8')
        assert conferir(str(s33), fonte_lint) == 1, \
            'linha de nicho sem `substantivo trocado` tinha que reprovar'
        com_col = sem_col.replace(
            'Um titulo | sobrevive',
            'Um titulo | substantivo trocado: joelho → planilha | sobrevive')
        c33.write_text(com_col, encoding='utf-8')
        assert conferir(str(s33), fonte_lint) == 0, 'com a coluna, passa'

        def rodar34(pasta, lint, **kw):
            buf = io.StringIO()
            antes = sys.stdout
            sys.stdout = buf
            try:
                cod = conferir(str(pasta), lint, **kw)
            finally:
                sys.stdout = antes
            return cod, buf.getvalue()

        # caso 34 · (b)2 e C1(b)2: o --conferir grava a própria saída, e a prova
        # de quem entregou não é apagada por quem confere. Rodar o gate sobre 16
        # pastas de uma rodada sobrescreveu o conferir.txt das 16.
        assert (s33 / SUBPASTA_BASTIDOR / 'conferir.txt').exists(), 'conferir.txt tinha que ser gravado'
        gravado = ler(s33 / SUBPASTA_BASTIDOR / 'conferir.txt')
        assert 'checagem-titulos.md: presente' in gravado, gravado
        marca34 = 'PROVA DA ENTREGA\ntítulos na peça: 99 · na checagem: 99\n'
        (s33 / SUBPASTA_BASTIDOR / 'conferir.txt').write_text(marca34, encoding='utf-8')
        cod34, t34 = rodar34(s33, fonte_lint)
        assert 'prova anterior preservada em conferir.txt' in t34, t34
        assert 'saída gravada em conferir.ultimo.txt' in t34, t34
        assert ler(s33 / SUBPASTA_BASTIDOR / 'conferir.txt') == marca34, 'a prova anterior tinha que ficar'
        assert (s33 / SUBPASTA_BASTIDOR / 'conferir.ultimo.txt').exists(), 'a execução nova tinha que sair'
        assert 'checagem-titulos.md: presente' in ler(s33 / SUBPASTA_BASTIDOR / 'conferir.ultimo.txt')
        # --gravar força a sobrescrita, e aí o aviso da execução anterior volta
        cod34b, t34b = rodar34(s33, fonte_lint, gravar=True)
        assert 'saída gravada em conferir.txt' in t34b, t34b
        assert 'aviso: conferir.txt de execução anterior' in t34b, t34b
        assert ler(s33 / SUBPASTA_BASTIDOR / 'conferir.txt') != marca34, 'com --gravar a prova é trocada'
        (s33 / SUBPASTA_BASTIDOR / 'conferir.ultimo.txt').unlink()

        # caso 35 · (a)3: contagem de fecho que contradiz a tabela reprova
        c33.write_text(com_col + 'sobrevive à troca de nicho, sim: 1\n', encoding='utf-8')
        assert conferir(str(s33), fonte_lint) == 1, \
            'contagem 1 contra tabela com 0 `sim` tinha que reprovar'
        c33.write_text(com_col + 'sobrevive à troca de nicho, sim: 0\n', encoding='utf-8')
        assert conferir(str(s33), fonte_lint) == 0, 'contagem que bate passa'
        # e a regra entre parênteses na MESMA linha isenta
        c33.write_text(com_col + 'sobrevive à troca de nicho, sim: 1 (só o de abertura; '
                                 'os rótulos de serviço ficam fora da conta)\n',
                       encoding='utf-8')
        assert conferir(str(s33), fonte_lint) == 0, 'a regra ao lado do número isenta'
        c33.write_text(com_col, encoding='utf-8')

        # caso 36 · (b)1: a exceção da fonte. Marcador longo herdado sai como
        # `achado na fonte` e não conta pro exit; o introduzido aqui reprova.
        s36 = d / 's36'
        s36.mkdir()
        fonte36 = d / 'fonte36.md'
        fonte36.write_text(
            '# Régua\n\nISCA: [A CONFIRMAR: nome exato do guia gratuito da casa]\n',
            encoding='utf-8')
        (s36 / 'peca.md').write_text(
            '# Um titulo\n\nISCA: [A CONFIRMAR: nome exato do guia gratuito da casa]\n',
            encoding='utf-8')
        chk_em(s36).write_text(com_col, encoding='utf-8')
        assert conferir(str(s36), fonte_lint) == 1, \
            'sem --fonte, o marcador longo reprova como sempre reprovou'
        buf36 = io.StringIO()
        real36 = sys.stdout
        sys.stdout = buf36
        try:
            code36 = conferir(str(s36), fonte_lint, fonte=str(fonte36))
        finally:
            sys.stdout = real36
        t36 = buf36.getvalue()
        assert code36 == 0, f'marcador herdado da fonte não reprova: {t36}'
        assert 'achado na fonte: marcador longo' in t36, t36
        assert 'introduzidos por esta conversão: 0' in t36, t36
        # o que a conversão INTRODUZIU continua reprovando
        (s36 / 'peca.md').write_text(
            '# Um titulo\n\nISCA: [A CONFIRMAR: nome exato do guia gratuito da casa]\n'
            'Prazo: [A CONFIRMAR: numero de semanas que esta conversao inventou agora]\n',
            encoding='utf-8')
        assert conferir(str(s36), fonte_lint, fonte=str(fonte36)) == 1, \
            'marcador introduzido pela conversão continua reprovando'

        # caso 37 · (a)2: o universo de títulos da skill que audita arquivo fora
        # da pasta é contado NA PEÇA AUDITADA, e `títulos auditados` menor reprova
        s37 = d / 's37'
        s37.mkdir()
        externa = d / 'peca-do-cliente.md'
        externa.write_text('# T1\n\ntexto\n\n## T2\n\ntexto\n\n## T3\n\ntexto\n',
                           encoding='utf-8')
        base37 = ('títulos no lote: 3\n'
                  'campos no perfil: 29 · valores desdobrados: 64 · usados: 16 · '
                  'descartados com motivo: 48\n'
                  'Um titulo | substantivo trocado: joelho → planilha | '
                  'sobrevive à troca de nicho? nao\n'
                  'títulos de abertura: 1 · reescritos: 1\n')
        chk_em(s37).write_text(base37 + 'títulos auditados: 2\n',
                                                 encoding='utf-8')
        assert conferir(str(s37), fonte_lint, peca_externa=str(externa)) == 1, \
            '`títulos auditados: 2` sobre peça de 3 títulos tinha que reprovar'
        chk_em(s37).write_text(base37 + 'títulos auditados: 3\n',
                                                 encoding='utf-8')
        assert conferir(str(s37), fonte_lint, peca_externa=str(externa)) == 0, \
            'auditados igual ao universo da peça externa passa'

        # caso 38 · (b)6: a isenção do destinatário cobre o vocativo em INÍCIO DE
        # LINHA seguido de vírgula, dentro de arquivo de mensagens, também no
        # --conferir. Antes disso o gate só passava quando a entrega desobedecia
        # a skill, que manda usar o primeiro nome literal de quem recebe.
        s38 = d / 's38'
        s38.mkdir()
        ins38 = d / 'insumos38'
        ins38.mkdir()
        (ins38 / 'caixa-entrada.md').write_text(
            'Mensagens nao respondidas:\n'
            '1. Claudia (aluna): "o grupo ficou 10 dias sem resposta"\n', encoding='utf-8')
        (s38 / 'primeiras-mensagens.md').write_text(
            '# Primeiras mensagens\n\n'
            'Claudia, tudo bem? Voce tem razao: o grupo ficou 10 dias sem resposta.\n',
            encoding='utf-8')
        chk_em(s38).write_text(
            'títulos no lote: 1\n'
            'campos no perfil: 29 · valores desdobrados: 64 · usados: 16 · '
            'descartados com motivo: 48\n'
            'Primeiras mensagens | substantivo trocado: joelho → planilha | '
            'sobrevive à troca de nicho? nao\n'
            'títulos de abertura: 1 · reescritos: 1\n', encoding='utf-8')
        buf38 = io.StringIO()
        real38 = sys.stdout
        sys.stdout = buf38
        try:
            # R12C2(b)8 · o perfil mora DENTRO da raiz de insumos que o gate recebe
            perfil38 = ins38 / 'dono.md'
            perfil38.write_text(ler(perfil), encoding='utf-8')
            code38 = conferir(str(s38), fonte_lint, insumos=str(ins38),
                              perfil=str(perfil38))
        finally:
            sys.stdout = real38
        t38 = buf38.getvalue()
        assert code38 == 0, f'o destinatário em vocativo de início de linha passa: {t38}'
        assert 'classificação: destinatário' in t38, t38
        assert not any('Claudia' in l and l.strip().startswith('x ')
                       for l in t38.splitlines()), t38

        # caso 39 · (b)9: o --render mede o PNG quando ele existir, e a medição
        # é alerta, nunca falha. Sem PIL o script pula com aviso, e sem PNG diz.
        s39 = d / 's39'
        s39.mkdir()
        h39 = s39 / 'slide-01.html'
        h39.write_text('<html><body><h1>Titulo</h1></body></html>\n', encoding='utf-8')
        buf39 = io.StringIO()
        real39 = sys.stdout
        sys.stdout = buf39
        try:
            code39 = checar_render(str(h39))
        finally:
            sys.stdout = real39
        t39 = buf39.getvalue()
        assert code39 == 0, t39
        assert 'medição da manchete pulada' in t39, t39
        try:
            from PIL import Image as _Img
            im = _Img.new('L', (200, 400), color=255)
            for y in range(10, 90):
                for x in range(10, 190):
                    im.putpixel((x, y), 0)
            im.save(s39 / 'slide-01.png')
            buf39b = io.StringIO()
            real39b = sys.stdout
            sys.stdout = buf39b
            try:
                code39b = checar_render(str(h39))
            finally:
                sys.stdout = real39b
            t39b = buf39b.getvalue()
            assert code39b == 0, t39b
            assert 'altura da manchete:' in t39b and '% da arte' in t39b, t39b
        except ImportError:
            pass

        # ── (b)7 e (a)4 · a peça que não é markdown ─────────────────────────
        def _pptx(caminho, slides):
            """Um .pptx mínimo, só com o que o script lê: ppt/slides/slideN.xml."""
            import zipfile
            with zipfile.ZipFile(str(caminho), 'w') as z:
                for i, textos in enumerate(slides, 1):
                    shapes = ''.join(
                        '<p:sp><p:txBody>'
                        + ''.join(f'<a:p><a:r><a:t>{t}</a:t></a:r></a:p>' for t in bloco)
                        + '</p:txBody></p:sp>'
                        for bloco in textos)
                    z.writestr(f'ppt/slides/slide{i}.xml',
                               f'<p:sld><p:cSld><p:spTree>{shapes}'
                               '</p:spTree></p:cSld></p:sld>')

        base_ok40 = ('campos no perfil: 29 · valores desdobrados: 64 · usados: 16 · '
                     'descartados com motivo: 48\n'
                     'Um titulo | substantivo trocado: joelho → planilha | '
                     'sobrevive à troca de nicho? nao\n'
                     'títulos de abertura: 1 · reescritos: 1\n')

        # caso 40 · (b)7: o universo soma os títulos do .html, e a peça que só
        # tem .html deixa de imprimir `títulos na peça: 0`. Duas pastas fecharam
        # o gate com zero porque o script varria só .md e a peça era .html.
        s40 = d / 's40'
        s40.mkdir()
        (s40 / 'index.html').write_text(
            '<html><head><title>Quanto custa parar</title></head><body>'
            '<h1>157 MB seguem protegidos: o que falta pra fechar</h1>'
            '<h2>A conta do mes</h2><h3>O proximo passo</h3>'
            '</body></html>\n', encoding='utf-8')
        chk_em(s40).write_text(
            'títulos no lote: 4\n' + base_ok40, encoding='utf-8')
        buf40 = io.StringIO()
        real40 = sys.stdout
        sys.stdout = buf40
        try:
            code40 = conferir(str(s40), fonte_lint)
        finally:
            sys.stdout = real40
        t40 = buf40.getvalue()
        assert 'títulos em index.html (html): 4' in t40, t40
        assert 'títulos na peça: 4' in t40, t40
        assert code40 == 0, t40

        # caso 40b · (b)7: sem .md de peça, sem .html e sem .pptx, o script diz
        # o motivo. Zero é uma afirmação sobre a peça e nunca sai de varredura
        # que não olhou pro arquivo certo.
        s40b = d / 's40b'
        s40b.mkdir()
        chk_em(s40b).write_text(
            'títulos no lote: 0\n' + base_ok40, encoding='utf-8')
        (s40b / 'RELATO.md').write_text('# Relato\n\n' + RESUMO + 'A entrega saiu sem peça.\n',
                                        encoding='utf-8')
        buf40b = io.StringIO()
        real40b = sys.stdout
        sys.stdout = buf40b
        try:
            code40b = conferir(str(s40b), fonte_lint)
        finally:
            sys.stdout = real40b
        t40b = buf40b.getvalue()
        assert 'sem peça varrível:' in t40b, t40b
        assert 'títulos na peça: 0' not in t40b, t40b
        assert code40b == 1, t40b

        # caso 41 · (b)7: os títulos dos slides do .pptx entram no universo, um
        # por slide, lidos do primeiro shape.
        s41 = d / 's41'
        s41.mkdir()
        _pptx(s41 / 'deck.pptx',
              [[['Fase 1: a mobilidade primeiro', 'três vezes por semana']],
               [['Fase 2: entra a força', 'depois que a base está instalada']]])
        chk_em(s41).write_text(
            'títulos no lote: 2\n' + base_ok40, encoding='utf-8')
        buf41 = io.StringIO()
        real41 = sys.stdout
        sys.stdout = buf41
        try:
            code41 = conferir(str(s41), fonte_lint)
        finally:
            sys.stdout = real41
        t41 = buf41.getvalue()
        assert 'títulos em deck.pptx (pptx): 2' in t41, t41
        assert 'títulos na peça: 2' in t41, t41
        assert 'deck.pptx · slides: 2' in t41, t41
        assert code41 == 0, t41

        # caso 42 · (a)4: o binário é lido de volta. Deck acentuado passa; deck
        # sem acento nenhum, com o .md de origem acentuado, reprova.
        s42 = d / 's42'
        s42.mkdir()
        (s42 / 'deck.md').write_text(
            '# Deck\n\nFase 1: a mobilidade é a primeira, e é onde o joelho para de doer.\n',
            encoding='utf-8')
        _pptx(s42 / 'deck.pptx',
              [[['FASE 1: A MOBILIDADE PRIMEIRO',
                 'So depois que a base esta instalada o corpo aguenta carga, '
                 'e e por isso que a ordem nao muda em nenhum programa serio '
                 'de quem voltou a treinar depois de uma pausa longa por dor.']]])
        chk_em(s42).write_text(
            'títulos no lote: 2\n' + base_ok40, encoding='utf-8')
        buf42 = io.StringIO()
        real42 = sys.stdout
        sys.stdout = buf42
        try:
            code42 = conferir(str(s42), fonte_lint)
        finally:
            sys.stdout = real42
        t42 = buf42.getvalue()
        assert code42 == 1, t42
        assert 'deck sem acentos' in t42, t42
        assert 'origem deck.md · linhas com acento: 1' in t42, t42
        assert 'arquivo: deck.pptx (texto extraído) · exit: 0' in t42, t42

        # caso 42b · (a)4: com o acento no binário, o mesmo deck passa
        _pptx(s42 / 'deck.pptx',
              [[['Fase 1: a mobilidade primeiro',
                 'Só depois que a base está instalada o corpo aguenta carga, '
                 'e é por isso que a ordem não muda em nenhum programa sério '
                 'de quem voltou a treinar depois de uma pausa longa por dor.']]])
        buf42b = io.StringIO()
        real42b = sys.stdout
        sys.stdout = buf42b
        try:
            code42b = conferir(str(s42), fonte_lint)
        finally:
            sys.stdout = real42b
        t42b = buf42b.getvalue()
        assert code42b == 0, t42b
        assert 'deck sem acentos' not in t42b, t42b

        # caso 43 · (b)2 e (b)5: a primeira linha do --conferir é o comando
        # literal com os caminhos absolutos, e o exit do RELATO sai por último,
        # em linha própria, pra colar no relato.
        s43 = d / 's43'
        s43.mkdir()
        (s43 / 'peca.md').write_text('# Um titulo\n\ntexto da peca\n', encoding='utf-8')
        (s43 / 'RELATO.md').write_text('# Relato\n\n' + RESUMO + 'A entrega saiu inteira.\n',
                                       encoding='utf-8')
        chk_em(s43).write_text(
            'títulos no lote: 1\n' + base_ok40, encoding='utf-8')
        buf43 = io.StringIO()
        real43 = sys.stdout
        sys.stdout = buf43
        try:
            code43 = conferir(str(s43), fonte_lint, insumos=str(d), perfil=str(perfil))
        finally:
            sys.stdout = real43
        t43 = buf43.getvalue()
        linhas43 = [l for l in t43.splitlines() if l.strip()]
        # (b)9 · a primeira linha abre com o md5 do gate e segue com o comando
        assert linhas43[0].startswith(f'script md5: {md5_do_script()} · comando: python3 '), \
            linhas43[0]
        assert f'--conferir {s43.resolve()}' in linhas43[0], linhas43[0]
        assert f'--insumos {Path(d).resolve()}' in linhas43[0], linhas43[0]
        assert f'--perfil {Path(perfil).resolve()}' in linhas43[0], linhas43[0]
        exits43 = [l for l in linhas43 if ' · exit: ' in l]
        assert exits43[-1] == 'RELATO.md · exit: 0', exits43
        assert code43 == 0, t43

        # caso 9: duas orações que o lint não pega entram na contagem
        assert duas_oracoes('Ela tentou voltar 3 vezes e sempre doeu. Faltava a fase 1.')
        assert duas_oracoes('- ★ Marcia subia escada com dor. Em 6 semanas, subiu sem sentir.')
        assert not duas_oracoes('Toda mulher que parou por dor no joelho, veja isto.')
        assert not duas_oracoes('| tabela | com | ponto. E mais |')
        assert not duas_oracoes('Rode o teste em 30 min. e volte')

        # ── rodada 11, casos novos ───────────────────────────────────────────
        base_r11 = ('campos no perfil: 29 · valores desdobrados: 29 · usados: 16 · '
                    'descartados com motivo: 13\n'
                    'sobrevive à troca de nicho? não | substantivo trocado: joelho → '
                    'telhado\n'
                    'títulos de abertura: 1 · reescritos: 1\n'
                    'A vs B | sujeito igual? não | predicado igual? não | conta como 1? não\n'
                    'teses distintas: 2\n')

        def rodar_conferir(pasta, **kw):
            buf = io.StringIO()
            antes = sys.stdout
            sys.stdout = buf
            try:
                cod = conferir(str(pasta), fonte_lint, **kw)
            finally:
                sys.stdout = antes
            return cod, buf.getvalue()

        # caso 44 · (b)3: nome que só aparece em linha de bastidor dentro de um
        # arquivo de planejamento, ou dentro de bloco cercado de código, não é
        # nome publicado. Punir a documentação do descarte ensina a não
        # documentar, e foi o que reprovou uma entrega cujo CSV público tinha
        # `grep -c` zero pro nome acusado.
        s44 = d / 's44'
        s44.mkdir()
        (s44 / 'plano-planejamento.md').write_text(
            '# Plano\n\nA lista sai do perfil e nada dela vira copy.\n'
            'candidatos brutos extraídos do perfil: Marcia, Renata\n'
            'nomes descartados: Renata\n'
            '```\n'
            'for n in Marcia Renata; do grep -nwF "$n" chat.csv; done\n'
            '```\n', encoding='utf-8')
        (s44 / 'peca-publica.md').write_text(
            '# Uma capa que carrega tese\n\nA fase 1 existe pra quem já parou duas vezes.\n',
            encoding='utf-8')
        chk_em(s44).write_text(
            'títulos no lote: 1\n' + base_r11, encoding='utf-8')
        cod44, t44 = rodar_conferir(s44, insumos=str(d), perfil=str(perfil))
        assert 'nome de conversa privada em peça pública' not in t44, t44
        assert 'Marcia · na peça' not in t44, t44

        # caso 44b · (b)3: o mesmo nome numa linha de copy do arquivo público
        # continua sendo nome publicado, e o gate segue valendo
        (s44 / 'peca-publica.md').write_text(
            '# Uma capa que carrega tese\n\nMarcia parou duas vezes antes da fase 1.\n',
            encoding='utf-8')
        _, t44b = rodar_conferir(s44, insumos=str(d), perfil=str(perfil))
        assert 'Marcia · na peça' in t44b, t44b

        # caso 45 · (b)6: cabeçalho de documento operacional sai do universo de
        # títulos de copy, e a linha `universo:` diz quais arquivos entraram
        assert 'universo: ' in t44, t44
        assert 'peca-publica.md' in [x.strip() for x in
                                     t44.split('universo: ')[1].split('\n')[0]
                                     .replace('·', ',').split(',')], t44
        assert 'documento operacional' in t44, t44
        univ45, det45, _ = universo_de_titulos(
            s44, sorted(s44.glob('*.md')))
        assert univ45 == 1, det45

        # caso 46 · (b)7: os números do inventário saem de comando sobre a
        # tabela; número declarado diferente do medido reprova
        s46 = d / 's46'
        s46.mkdir()
        tabela = ('| Dado | Uso ou descarte |\n|---|---|\n'
                  '| campo um | usado na capa |\n'
                  '| campo dois | usado no corpo |\n'
                  '| campo tres | descartado porque não cabe |\n')
        # conserto 4/5 · a tabela de destino mora no bastidor, nunca na peça que o
        # dono abre; o inventário é medido por comando sobre ela onde quer que ela
        # esteja na raiz, e a peça pública fica limpa.
        (s46 / 'peca.md').write_text('# Uma capa com tese\n\ncorpo limpo da peça.\n',
                                     encoding='utf-8')
        (s46 / 'inventario.md').write_text('# Inventário\n\n' + tabela, encoding='utf-8')
        chk_em(s46).write_text(
            'títulos no lote: 1\n'
            'campos no perfil: 3 · valores desdobrados: 9 · usados: 7 · '
            'descartados com motivo: 2\n'
            'sobrevive à troca de nicho? não | substantivo trocado: joelho → telhado\n'
            'títulos de abertura: 1 · reescritos: 1\n'
            'A vs B | sujeito igual? não | predicado igual? não | conta como 1? não\n'
            'teses distintas: 2\n', encoding='utf-8')
        cod46, t46 = rodar_conferir(s46)
        assert 'inventário medido na tabela' in t46, t46
        assert 'linhas: 3 · usados: 2 · descartados: 1' in t46, t46
        assert cod46 == 1, t46
        assert 'inventário redigitado' in t46, t46
        # com os números medidos, passa
        chk_em(s46).write_text(
            'títulos no lote: 1\n'
            'campos no perfil: 3 · valores desdobrados: 3 · usados: 2 · '
            'descartados com motivo: 1\n'
            'sobrevive à troca de nicho? não | substantivo trocado: joelho → telhado\n'
            'títulos de abertura: 1 · reescritos: 1\n'
            'A vs B | sujeito igual? não | predicado igual? não | conta como 1? não\n'
            'teses distintas: 2\n', encoding='utf-8')
        cod46b, t46b = rodar_conferir(s46)
        assert 'inventário redigitado' not in t46b, t46b
        assert cod46b == 0, t46b

        # caso 47 · (b)4: `<arquivo>: N bytes` no RELATO confere contra wc -c,
        # com tolerância 0. É a única parte da entrega que o dono lê sem abrir
        # o terminal, e número redigitado ali vale menos que nada.
        s47 = d / 's47'
        s47.mkdir()
        (s47 / 'peca.md').write_text('# Uma capa com tese\n\ntexto\n', encoding='utf-8')
        real47 = (s47 / 'peca.md').stat().st_size
        chk_em(s47).write_text(
            'títulos no lote: 1\n' + base_r11, encoding='utf-8')
        (s47 / 'RELATO.md').write_text(
            f'# Relato\n\n{RESUMO}peca.md: {real47 + 500} bytes\n', encoding='utf-8')
        cod47, t47 = rodar_conferir(s47)
        assert 'bytes redigitados' in t47, t47
        assert cod47 == 1, t47
        (s47 / 'RELATO.md').write_text(
            f'# Relato\n\n{RESUMO}peca.md: {real47} bytes\n', encoding='utf-8')
        cod47b, t47b = rodar_conferir(s47)
        assert 'bytes redigitados' not in t47b, t47b
        assert cod47b == 0, t47b

        # caso 48 · (b)2: colisão por nome contido, e o nome composto testado
        # também pela primeira palavra. `Paula J.` na peça encosta em
        # `Ana Paula, 40` na caixa de entrada, e o teste por string inteira
        # declarou `coincidências: 0`.
        assert variantes_do_nome('Paula J.') == ['Paula J.', 'Paula'], \
            variantes_do_nome('Paula J.')
        assert variantes_do_nome('Marcia') == ['Marcia'], variantes_do_nome('Marcia')
        s48 = d / 's48'
        s48.mkdir()
        ins48 = d / 'insumos48'
        ins48.mkdir()
        (ins48 / 'caixa-entrada.md').write_text(
            '7. Ana Paula, 40: "quero entrar na turma de outubro"\n', encoding='utf-8')
        (s48 / 'peca.md').write_text(
            '# Uma capa com tese\n\nPaula escreveu no chat que voltou a treinar.\n',
            encoding='utf-8')
        chk_em(s48).write_text(
            'títulos no lote: 1\n' + base_r11, encoding='utf-8')
        cod48, t48 = rodar_conferir(s48, insumos=str(ins48), perfil=str(perfil))
        assert 'nome de conversa privada em peça pública: Paula' in t48, t48
        assert cod48 == 1, t48

        # caso 49 · (b)9: o md5 do gate abre o conferir.txt, e md5 gravado
        # diferente sai como aviso de artefato de versão, nunca como reprova
        assert (s47 / SUBPASTA_BASTIDOR / 'conferir.txt').read_text(encoding='utf-8').startswith(
            f'script md5: {md5_do_script()} · comando: '), \
            (s47 / SUBPASTA_BASTIDOR / 'conferir.txt').read_text(encoding='utf-8')[:120]
        chk_em(s47).write_text(
            'script md5: 00000000\ntítulos no lote: 1\n' + base_r11, encoding='utf-8')
        cod49, t49 = rodar_conferir(s47)
        assert 'gates novos desde a checagem' in t49, t49
        assert cod49 == 0, t49

        # caso 50 · (b)6: campo do fecho fechado com a mensagem de ajuda do
        # próprio script conta como NÃO preenchido e reprova com exit 1.
        s50 = d / 'saida50'
        s50.mkdir()
        (s50 / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')
        chk50 = chk_em(s50)
        chk50.write_text(base_ok, encoding='utf-8')
        assert conferir(str(s50), fonte_lint) == 0, 'base limpa tinha que passar'
        for ajuda in ('sem --teses: salve uma tese de 4 palavras por linha em '
                      'teses.txt e rode de novo',
                      'rode de novo com --insumos',
                      'não informada'):
            chk50.write_text(base_ok + f'falas de terceiro: {ajuda}\n', encoding='utf-8')
            assert conferir(str(s50), fonte_lint) == 1, \
                f'ajuda do script no fecho tinha que reprovar: {ajuda}'
        chk50.write_text(base_ok + 'falas de terceiro: 2\n', encoding='utf-8')
        assert conferir(str(s50), fonte_lint) == 0, 'número no fecho tinha que passar'

        # ── rodada 12, casos novos ───────────────────────────────────────────
        def nova_pasta(nome, corpo, extra=''):
            """pasta de saída mínima que passa: peça limpa + checagem base."""
            s = d / nome
            s.mkdir()
            (s / 'peca.md').write_text(corpo, encoding='utf-8')
            chk_em(s).write_text(base_ok + extra, encoding='utf-8')
            return s

        # caso 51 · B(b)1: os arquivos exigidos pela ação. Uma pasta sem deck e
        # sem página recebeu `conferência ok` num pedido de pacote.
        s51 = nova_pasta('s51', '# Um titulo\n\nlimpo\n')
        assert conferir(str(s51), fonte_lint) == 0, 'sem --exige, a pasta passa'
        cod51, t51 = rodar34(s51, fonte_lint, exige='peca.md')
        assert cod51 == 0, t51
        assert 'arquivo exigido pela ação: peca.md · presente' in t51, t51
        cod51b, t51b = rodar34(s51, fonte_lint, exige='02-slides.pptx,03-pagina.md')
        assert cod51b == 1, t51b
        assert 'arquivo exigido pela ação ausente: 02-slides.pptx' in t51b, t51b
        assert 'arquivo exigido pela ação ausente: 03-pagina.md' in t51b, t51b
        # glob conta como nome
        cod51c, t51c = rodar34(s51, fonte_lint, exige='pec*.md')
        assert cod51c == 0, t51c

        # caso 52 · C1(a)1 e (a)2: cabeçalho de peça pública com padrão de
        # rótulo entra no universo e reprova; a isenção curta continua isenta.
        s52 = nova_pasta('s52',
                         '# Um titulo\n\n## Etapa P3 · Ancoragem\n\nlimpo\n',
                         'títulos no lote: 2\n')
        cod52, t52 = rodar34(s52, fonte_lint)
        assert cod52 == 1, t52
        assert 'rótulo no miolo: peca.md:3: ## Etapa P3 · Ancoragem' in t52, t52
        assert 'cabeçalho de peça pública é rótulo, não tese' in t52, t52
        for rotulo in ('## Passo 2', '## Seção de fecho: a frase que sobrevive',
                       '## Bloco 4', '## P3', '## Checagem', '## Parte II'):
            (s52 / 'peca.md').write_text(f'# Um titulo\n\n{rotulo}\n\nlimpo\n',
                                         encoding='utf-8')
            cod, txt52 = rodar34(s52, fonte_lint)
            assert cod == 1 and '  rótulo no miolo:' in txt52, f'{rotulo}: {txt52}'
        # a isenção que sobrou: nenhum deles sai como `rótulo no miolo`
        for isento in ('## FAQ', '## Bio', '## Índice', '## Anexo', '## Referências',
                       '## Sumário', '## Perguntas frequentes'):
            (s52 / 'peca.md').write_text(f'# Um titulo\n\n{isento}\n\nlimpo\n',
                                         encoding='utf-8')
            chk_em(s52).write_text(base_ok, encoding='utf-8')
            _, txt52 = rodar34(s52, fonte_lint)
            assert '  rótulo no miolo:' not in txt52, f'{isento} continua isento: {txt52}'
            assert 'cabeçalhos de rótulo no miolo da peça pública: 0' in txt52, txt52
        # documento operacional inteiro fica fora pelo nome do arquivo
        (s52 / 'peca.md').unlink()
        (s52 / 'planejamento.md').write_text('## Etapa P3 · Ancoragem\n\nlimpo\n',
                                             encoding='utf-8')
        chk_em(s52).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 0'), encoding='utf-8')
        cod52d, t52d = rodar34(s52, fonte_lint)
        assert cod52d == 0, t52d

        # caso 53 · C1(b)4: `.md` de peça pública sem nenhuma linha `^# `
        s53 = nova_pasta('s53', 'sem cabecalho nenhum aqui\n',
                         '')
        chk_em(s53).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 0'), encoding='utf-8')
        cod53, t53 = rodar34(s53, fonte_lint)
        assert cod53 == 1, t53
        assert 'peça sem H1: peca.md' in t53, t53

        # caso 54 · B(b)2: negar a saída colada na mesma checagem reprova
        s54 = nova_pasta('s54', '# Um titulo\n\npalavra-chave: nenhuma\n')
        chk_em(s54).write_text(
            base_ok + 'trecho de CTA encontrado: aula.md:2 manda BASE40\n',
            encoding='utf-8')
        cod54, t54 = rodar34(s54, fonte_lint)
        assert cod54 == 1, t54
        assert 'conclusão contradiz a saída do grep' in t54, t54
        # `descartado porque não consta` cai no mesmo gate
        (s54 / 'peca.md').write_text(
            '# Um titulo\n\nBASE40 descartado porque não consta no perfil\n',
            encoding='utf-8')
        cod54b, t54b = rodar34(s54, fonte_lint)
        assert cod54b == 1 and 'conclusão contradiz' in t54b, t54b
        # sem ocorrência colada, a conclusão negativa é válida
        chk_em(s54).write_text(base_ok, encoding='utf-8')
        (s54 / 'peca.md').write_text('# Um titulo\n\npalavra-chave: nenhuma\n',
                                     encoding='utf-8')
        cod54c, t54c = rodar34(s54, fonte_lint)
        assert cod54c == 0, t54c

        # caso 55 · C1(b)8: o rótulo do piso não se usa no total desdobrado
        perfil55 = d / 'dono55.md'
        perfil55.write_text('\n'.join(f'- campo {i}' for i in range(1, 30)) + '\n',
                            encoding='utf-8')
        s55 = nova_pasta('s55', '# Um titulo\n\nlimpo\n')
        cod55, t55 = rodar34(s55, fonte_lint, perfil=str(perfil55))
        assert cod55 == 0, t55
        assert "campos no perfil declarado: 29 · grep -c '^- ' dono55.md: 29" in t55, t55
        chk_em(s55).write_text(
            base_ok.replace('campos no perfil: 29', 'campos no perfil: 38')
                   .replace('valores desdobrados: 64', 'valores desdobrados: 64'),
            encoding='utf-8')
        cod55b, t55b = rodar34(s55, fonte_lint, perfil=str(perfil55))
        assert cod55b == 1, t55b
        assert 'rótulo do piso trocado' in t55b, t55b

        # caso 56 · B(a)1: número marcado `[A CONFIRMAR` no perfil publicado
        perfil56 = d / 'dono56.md'
        perfil56.write_text(
            '\n'.join(f'- campo {i}' for i in range(1, 29))
            + '\n- prazo do protocolo: 6 semanas [A CONFIRMAR: número exato]\n',
            encoding='utf-8')
        s56 = nova_pasta('s56', '# Um titulo\n\nEm 6 semanas a subida volta.\n')
        cod56, t56 = rodar34(s56, fonte_lint, perfil=str(perfil56))
        assert cod56 == 1, t56
        assert 'número não confirmado na peça: 6 semanas' in t56, t56
        # a forma sem prazo passa
        (s56 / 'peca.md').write_text(
            '# Um titulo\n\nDepois de algumas semanas a subida volta.\n',
            encoding='utf-8')
        cod56b, t56b = rodar34(s56, fonte_lint, perfil=str(perfil56))
        assert cod56b == 0, t56b
        assert 'números não confirmados no perfil: 1 · publicados na peça: 0' in t56b, t56b

        # caso 57 · C1(b)5: o .html de render entra no lint do --conferir
        s57 = nova_pasta('s57', '# Um titulo\n\nlimpo\n')
        # o <h1> do render soma ao universo: o lote da checagem vira 2
        chk_em(s57).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 2'), encoding='utf-8')
        (s57 / 'preview.html').write_text(
            '<html><body><h1>Um titulo</h1><p>Nao e sorte. E conta. '
            'A pressa nao resolve. O metodo resolve.</p></body></html>\n',
            encoding='utf-8')
        cod57, t57 = rodar34(s57, fonte_lint)
        assert 'arquivo: preview.html (texto extraído do render) · exit:' in t57, t57
        assert cod57 == 1, t57
        assert 'lint reprovou o texto extraído de preview.html' in t57, t57
        (s57 / 'preview.html').write_text(
            '<html><body><h1>Um titulo</h1><p>texto limpo do render</p></body></html>\n',
            encoding='utf-8')
        cod57b, t57b = rodar34(s57, fonte_lint)
        assert cod57b == 0, t57b
        assert 'arquivo: preview.html (texto extraído do render) · exit: 0' in t57b, t57b

        # caso 58 · C1(b)1: os arquivos que o gate escreve saem da checagem de
        # bytes declarados, porque o wc -c deles descreve a rodada anterior
        s58 = nova_pasta('s58', '# Um titulo\n\nlimpo\n')
        (s58 / 'RELATO.md').write_text(
            '# Relato\n\n' + RESUMO + 'conferir.txt: 999 bytes\n'
            'checar-passo1.txt: 999 bytes\ncheckagem-raw.txt: 999 bytes\n',
            encoding='utf-8')
        garantir_conferencia(s58)
        (s58 / SUBPASTA_BASTIDOR / 'conferir.txt').write_text(
            'prova antiga\n', encoding='utf-8')
        (s58 / SUBPASTA_BASTIDOR / 'checar-passo1.txt').write_text(
            'passo 1\n', encoding='utf-8')
        cod58, t58 = rodar34(s58, fonte_lint)
        assert cod58 == 0, t58
        assert 'bytes redigitados' not in t58, t58

        # caso 59 · B(b)5 e C1(b)3: o fecho da reprova, e a R7 em universo > 20
        s59 = nova_pasta('s59', '\n\n'.join(f'# Titulo {i}\n\nlimpo'
                                            for i in range(1, 26)) + '\n')
        chk_em(s59).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 25')
                   .replace('títulos de abertura: 1 · reescritos: 1',
                            'títulos de abertura: 25 · reescritos: 1')
            + 'reescrito de: Titulo velho\n', encoding='utf-8')
        cod59, t59 = rodar34(s59, fonte_lint)
        assert cod59 == 1, t59
        assert 'abaixo de 5% do universo' in t59, t59
        assert t59.strip().splitlines()[-2] == \
            'exit diferente de 0 não é entrega, mesmo com relato honesto', t59
        chk_em(s59).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 25')
                   .replace('títulos de abertura: 1 · reescritos: 1',
                            'títulos de abertura: 25 · reescritos: 2')
            + 'reescrito de: Titulo velho\nreescrito de: Outro velho\n',
            encoding='utf-8')
        cod59b, t59b = rodar34(s59, fonte_lint)
        assert cod59b == 0, t59b

        # ── rodada 12 C2, casos novos ────────────────────────────────────────
        # caso 60 · R12C2(b)9: o gate novo nunca reprova a linha que o gate
        # velho imprime. Sem --ressalva o script agora acha a ressalva sozinho e
        # imprime um NÚMERO; sem teses.txt ele imprime `0 (teses.txt ausente)`.
        args60 = argparse.Namespace(
            peca=[str(s59 / 'peca.md')], titulos=None, teses=None, insumos=None,
            perfil=None, ressalva=None, nomes=None, lint=fonte_lint)
        (s59 / 'peca.md').write_text(
            '# Um titulo\n\nlimpo\n\nSintoma que persiste pede avaliação individual.\n',
            encoding='utf-8')
        out60 = []
        montar(args60, out60)
        t60 = '\n'.join(out60)
        assert 'ressalvas na peça: 1 (detectadas: ' in t60, t60
        assert 'rode com --ressalva' not in t60, t60
        assert 'teses distintas: 0 (teses.txt ausente)' in t60, t60
        assert 'sem --teses' not in t60.split('teses distintas')[1][:80], t60
        # e a linha que o script imprime não conta como campo com instrução
        s60 = nova_pasta('s60', '# Um titulo\n\nlimpo\n',
                         'ressalvas na peça: não informada (rode com --ressalva)\n'
                         'nomes candidatos achados pelo script: sem --insumos\n')
        cod60, t60b = rodar34(s60, fonte_lint)
        assert 'saída do próprio gate: ' in t60b, t60b
        assert 'campo com instrução no lugar do número' not in \
            t60b.split('REPROVA')[-1], t60b
        assert cod60 == 0, t60b
        # `teses distintas: 0 (teses.txt ausente)` reprova por ARQUIVO ausente,
        # e só em lote acima de 3
        s60b = nova_pasta('s60b', '# Um titulo\n\nlimpo\n',
                          'teses distintas: 0 (teses.txt ausente)\n')
        cod60b, t60c = rodar34(s60b, fonte_lint)
        assert cod60b == 0, t60c
        assert 'teses.txt ausente' in t60c, t60c
        chk_em(s60b).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 9')
            + 'teses distintas: 0 (teses.txt ausente)\n', encoding='utf-8')
        cod60c, t60d = rodar34(s60b, fonte_lint)
        assert cod60c == 1, t60d
        assert 'teses.txt ausente: o lote tem 9 títulos' in t60d, t60d
        assert 'campo com instrução' not in t60d.split('REPROVA')[-1], t60d

        # caso 61 · R12C2(b)5: titulos.txt vazio com peça renderizada na pasta
        s61 = nova_pasta('s61', '# A capa que a fonte já trazia\n\nlimpo\n')
        (garantir_conferencia(s61) / 'titulos.txt').write_text('', encoding='utf-8')
        sub61 = s61 / 'cards'
        sub61.mkdir()
        for i in range(1, 4):
            (sub61 / f'slide-{i:02d}.png').write_bytes(b'\x89PNG\r\n')
        cod61, t61 = rodar34(s61, fonte_lint)
        assert cod61 == 1, t61
        assert 'universo de títulos vazio com peça renderizada' in t61, t61
        assert 'peças renderizadas na pasta: 3' in t61, t61
        # e os títulos saem extraídos do arquivo de copy, impressos pro motor
        assert 'títulos extraídos do arquivo de copy ou manifesto: 1' in t61, t61
        assert 'A capa que a fonte já trazia' in t61, t61
        (garantir_conferencia(s61) / 'titulos.txt').write_text('um\ndois\ntres\n', encoding='utf-8')
        cod61b, t61b = rodar34(s61, fonte_lint)
        assert cod61b == 0, t61b

        # caso 62 · R12C2(b)8: o --insumos resolvido sai na saída, e o perfil
        # fora da pasta de insumos reprova a forma do comando
        raiz62 = d / 'raiz62'
        (raiz62 / 'insumos').mkdir(parents=True)
        perf62 = raiz62 / 'dono.md'
        perf62.write_text(ler(perfil), encoding='utf-8')
        s62 = nova_pasta('s62', '# Um titulo\n\nlimpo\n')
        cod62, t62 = rodar_conferir(s62, insumos=str(raiz62 / 'insumos'),
                                    perfil=str(perf62))
        assert cod62 == 1, t62
        assert f'insumos resolvido: {(raiz62 / "insumos").resolve()}' in t62, t62
        assert 'insumos recortado: o perfil está fora da pasta de insumos' in t62, t62
        cod62b, t62b = rodar_conferir(s62, insumos=str(raiz62), perfil=str(perf62))
        assert cod62b == 0, t62b
        assert f'insumos resolvido: {raiz62.resolve()}' in t62b, t62b

        # caso 63 · R12C2(a)2: a fala que o dono vai gravar passa pelo gate do
        # número não confirmado. O que está na lista de falas vira áudio no ar.
        perf63 = d / 'perfil63.md'
        perf63.write_text(ler(perfil)
                          + '- tempo até o resultado: 6 semanas [A CONFIRMAR: exato]\n',
                          encoding='utf-8')
        s63 = nova_pasta('s63', '# Um titulo\n\nlimpo\n')
        chk_em(s63).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 2'), encoding='utf-8')
        (s63 / 'PEDIDO-DE-GRAVACAO-take.md').write_text(
            '# Falas do take\n\nEm 6 semanas de protocolo o ombro escolhe a carga.\n',
            encoding='utf-8')
        cod63, t63 = rodar_conferir(s63, insumos=str(d), perfil=str(perf63))
        assert cod63 == 1, t63
        assert 'número não confirmado na peça: 6 semanas' in t63, t63
        assert 'PEDIDO-DE-GRAVACAO-take.md' in t63, t63
        (s63 / 'PEDIDO-DE-GRAVACAO-take.md').write_text(
            '# Falas do take\n\nDepois de algumas semanas o ombro escolhe a carga.\n',
            encoding='utf-8')
        cod63b, t63b = rodar_conferir(s63, insumos=str(d), perfil=str(perf63))
        assert cod63b == 0, t63b

        # caso 64 · R12C2(b)6: linha de RELATO que declara ausência de
        # capacidade exige o comando colado em bloco cercado nas 3 linhas
        # seguintes, o erro incluso
        s64 = nova_pasta('s64', '# Um titulo\n\nlimpo\n')
        (s64 / 'RELATO.md').write_text(
            '# Relato\n\n' + RESUMO + 'Sem acesso à web nesta rodada, ambiente sem busca.\n',
            encoding='utf-8')
        cod64, t64 = rodar34(s64, fonte_lint)
        assert cod64 == 1, t64
        assert 'afirmação de ausência sem comando colado: RELATO.md:7' in t64, t64
        (s64 / 'RELATO.md').write_text(
            '# Relato\n\n' + RESUMO + 'Sem acesso à web nesta rodada, ambiente sem busca.\n\n'
            '```\ncurl -s https://exemplo.tld\ncurl: (6) could not resolve host\n```\n',
            encoding='utf-8')
        cod64b, t64b = rodar34(s64, fonte_lint)
        assert cod64b == 0, t64b
        assert 'afirmações de ausência de capacidade sem comando colado: 0' in t64b, t64b

        # ── rodada 13, o crivo da dona ───────────────────────────────────────
        # caso 65 · o bastidor na raiz da pasta do dono reprova, e some quando
        # muda pra conferencia/. Ela abriu 9 arquivos e não sabia se guardava.
        s65 = nova_pasta('s65', '# Um titulo\n\nlimpo\n')
        (s65 / 'titulos.txt').write_text('Um titulo\n', encoding='utf-8')
        (s65 / 'teses.txt').write_text('uma tese curta\n', encoding='utf-8')
        (s65 / 'nomes.txt').write_text('', encoding='utf-8')
        cod65, t65 = rodar34(s65, fonte_lint)
        assert cod65 == 1, t65
        assert 'aviso: bastidor na raiz, mova pra conferencia/: titulos.txt' in t65, t65
        assert 'pasta do dono com bastidor' in t65, t65
        for nome65 in ('titulos.txt', 'teses.txt', 'nomes.txt'):
            (s65 / nome65).rename(garantir_conferencia(s65) / nome65)
        cod65b, t65b = rodar34(s65, fonte_lint)
        assert cod65b == 0, t65b
        assert 'bastidor na raiz da pasta do dono: 0' in t65b, t65b

        # caso 66 · log e cache de execução na raiz. Um codex.log de 2,3 MB na
        # pasta de stories fez a entrega inteira parecer bagunçada.
        s66 = nova_pasta('s66', '# Um titulo\n\nlimpo\n')
        (s66 / 'codex.log').write_text('linha de log\n', encoding='utf-8')
        cod66, t66 = rodar34(s66, fonte_lint)
        assert cod66 == 1, t66
        assert 'lixo de máquina na raiz: codex.log' in t66, t66
        (s66 / 'codex.log').unlink()
        assert rodar34(s66, fonte_lint)[0] == 0

        # caso 67 · caixa alta no título. Ênfase é por palavra, nunca por tecla.
        s67 = nova_pasta('s67', '# Um titulo\n\nlimpo\n')
        tit67 = garantir_conferencia(s67) / 'titulos.txt'
        tit67.write_text('TREINO PESADO DEPOIS DOS QUARENTA\n', encoding='utf-8')
        cod67, t67 = rodar34(s67, fonte_lint)
        assert cod67 == 1, t67
        assert 'título em caixa alta' in t67, t67
        # sigla curta passa, e a palavra-chave de CTA também
        tit67.write_text('Manda BASE40 no Direct e eu te mando o PDF\n', encoding='utf-8')
        cod67b, t67b = rodar34(s67, fonte_lint)
        assert cod67b == 0, t67b
        assert 'títulos em caixa alta: 0' in t67b, t67b
        # e a função pura responde do mesmo jeito
        assert caixa_alta_demais('TREINO PESADO DEPOIS DOS QUARENTA') is not None
        assert caixa_alta_demais('Treino pesado depois dos quarenta') is None
        assert caixa_alta_demais('Manda BASE40 no Direct', {'BASE40'}) is None
        assert caixa_alta_demais('O PDF do CREF e o CRM') is None

        # caso 68 · o relato abre com as 3 linhas do dono e fecha com a lista de
        # perguntas. Hoje ele abre com head -5 e md5, o diário do trabalhador.
        s68 = nova_pasta('s68', '# Um titulo\n\nlimpo\n')
        (s68 / 'RELATO.md').write_text(
            '# Relato\n\nLi os 5 arquivos da pasta e conferi cada um.\n',
            encoding='utf-8')
        cod68, t68 = rodar34(s68, fonte_lint)
        assert cod68 == 1, t68
        assert 'relato sem resumo pro dono' in t68, t68
        (s68 / 'RELATO.md').write_text(
            '# Relato\n\nPronto: o carrossel de 10 slides.\n'
            'Abra primeiro: peca.md\n'
            'Falta você responder: 1 pergunta\n\n'
            'O resto do relato vem aqui.\n\n'
            '## Perguntas pra você\n\n'
            '- Qual o horário que fecha melhor pra você?\n', encoding='utf-8')
        cod68b, t68b = rodar34(s68, fonte_lint)
        assert cod68b == 0, t68b
        assert 'resumo pro dono nas 3 primeiras linhas: sim' in t68b, t68b
        assert 'seção `Perguntas pra você`: sim · perguntas escritas: 1' in t68b, t68b

        # caso 69 · pendência espalhada sem a lista de perguntas. Ela ficou sem
        # chão com `[A CONFIRMAR: titularidade da reserva]` no meio do texto.
        s69 = nova_pasta('s69',
                         '# Um titulo\n\nO horario e [A CONFIRMAR: horario]\n')
        (s69 / 'RELATO.md').write_text(
            '# Relato\n\nPronto: a peça saiu.\nAbra primeiro: peca.md\n'
            'Falta você responder: 1 pergunta\n\nsem lista no fim.\n',
            encoding='utf-8')
        cod69, t69 = rodar34(s69, fonte_lint)
        assert cod69 == 1, t69
        assert 'pendências espalhadas sem lista de perguntas' in t69, t69

        # caso 70 · comando entregue ao dono. Ele opera pelo Telegram: ou a
        # skill executa, ou ela diz o que pedir e pra quem.
        s70 = nova_pasta('s70', '# Um titulo\n\nlimpo\n',
                         extra='')
        chk_em(s70).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 2'),
            encoding='utf-8')
        (s70 / 'PUBLICACAO.md').write_text(
            '# Como publicar\n\nRode npx wrangler pages deploy no terminal.\n',
            encoding='utf-8')
        cod70, t70 = rodar34(s70, fonte_lint)
        assert cod70 == 1, t70
        assert 'comando entregue ao dono: PUBLICACAO.md:3' in t70, t70
        # dentro de bloco cercado, o comando é bastidor e não conta
        (s70 / 'PUBLICACAO.md').write_text(
            '# Como publicar\n\nPeça isto a quem cuida do site:\n\n'
            '```\nnpx wrangler pages deploy\n```\n', encoding='utf-8')
        cod70b, t70b = rodar34(s70, fonte_lint)
        assert cod70b == 0, t70b
        assert 'comandos entregues ao dono: 0' in t70b, t70b

        # caso 71 · jargão interno sem a glosa de até 4 palavras. "Fase 7",
        # "PUV" e "molde de antítese" não significam nada pro dono.
        s71 = nova_pasta('s71', '# Um titulo\n\nlimpo\n')
        (s71 / 'HANDOFF-x.md').write_text(
            '# Handoff\n\nPronto: a peça saiu.\nAbra primeiro: peca.md\n'
            'Falta você responder: nada\n\nA Fase 7 fecha a conversa.\n\n'
            '## Perguntas pra você\n\n- Alguma coisa a mudar?\n',
            encoding='utf-8')
        cod71, t71 = rodar34(s71, fonte_lint)
        assert cod71 == 1, t71
        assert 'jargão sem tradução: Fase 7' in t71, t71
        (s71 / 'HANDOFF-x.md').write_text(
            '# Handoff\n\nPronto: a peça saiu.\nAbra primeiro: peca.md\n'
            'Falta você responder: nada\n\nA Fase 7 (o fechamento) fecha a conversa.\n\n'
            '## Perguntas pra você\n\n- Alguma coisa a mudar?\n',
            encoding='utf-8')
        cod71b, t71b = rodar34(s71, fonte_lint)
        assert cod71b == 0, t71b
        assert 'jargão interno sem glosa: 0' in t71b, t71b

        # caso 72 · nome fica no arquivo INTERNO do dono. A triagem trocou as
        # leads por `contato A` e a dona teve que cruzar dois arquivos pra
        # responder no WhatsApp. A anonimização é da peça pública.
        ins72 = d / 'insumos72'
        ins72.mkdir()
        (ins72 / 'caixa-de-entrada.md').write_text(
            'Mensagens:\n1. Simone, 51: "ja fiz pilates e parei."\n', encoding='utf-8')
        s72 = d / 's72'
        s72.mkdir()
        chk_em(s72).write_text(base_ok, encoding='utf-8')
        (s72 / 'fila-do-dia.md').write_text(
            '# A fila de hoje\n\nSimone, 51, espera proposta ha 3 dias.\n',
            encoding='utf-8')
        cod72, t72 = rodar_conferir(s72, insumos=str(ins72))
        assert cod72 == 0, t72
        assert 'uso interno: fila-do-dia.md' in t72, t72
        assert 'nome de conversa privada em peça pública' not in t72, t72
        # a mesma frase num post público continua reprovando
        (s72 / 'post-de-feed.md').write_text(
            '# Um titulo do post\n\nSimone, 51, espera proposta ha 3 dias.\n',
            encoding='utf-8')
        cod72b, t72b = rodar_conferir(s72, insumos=str(ins72))
        assert cod72b == 1, t72b
        assert 'nome de conversa privada em peça pública: Simone' in t72b, t72b

        # caso 73 · o passo 1 grava a checagem direto em conferencia/, sem a
        # colagem à mão de 17 KB que virava prosa reescrita.
        s73 = d / 's73'
        s73.mkdir()
        (s73 / 'peca.md').write_text('# Um titulo\n\nlimpo\n', encoding='utf-8')
        main(['--peca', str(s73 / 'peca.md'), '--insumos', str(ins72),
              '--gravar-checagem', str(s73), '--lint', str(fonte_lint)])
        gravada73 = s73 / SUBPASTA_BASTIDOR / 'checagem-titulos.md'
        assert gravada73.exists(), 'a checagem tinha que ser gravada em conferencia/'
        assert 'fecho da régua de títulos' in ler(gravada73)

        # ── PENDENTE-r14 · os 9 consertos do script ──────────────────────────
        # caso 74 · dígito solto na peça não reprova; só o número COM a unidade
        # do perfil. Treino escreveu `2` de série e `6` de faixa e o gate antigo
        # reprovava; a cura tira o incentivo de escrever `dois` pra passar.
        perf74 = d / 'perfil74.md'
        perf74.write_text('\n'.join(f'- campo {i}' for i in range(1, 29))
                          + '\n- prazo: 6 semanas [A CONFIRMAR: exato]\n', encoding='utf-8')
        s74 = nova_pasta('s74',
                         '# Treino\n\n| série | reps | RIR |\n|---|---|---|\n'
                         '| 1 | 6 a 8 | 2 |\n| 2 | 6 | 2 |\n')
        cod74, t74 = rodar_conferir(s74, perfil=str(perf74))
        assert cod74 == 0, t74  # 2 e 6 soltos na tabela não reprovam
        assert 'números não confirmados no perfil: 1 · publicados na peça: 0' in t74, t74
        # a forma COM a unidade reprova
        (s74 / 'peca.md').write_text('# Treino\n\nEm 6 semanas o ombro sobe a carga.\n',
                                     encoding='utf-8')
        cod74b, t74b = rodar_conferir(s74, perfil=str(perf74))
        assert cod74b == 1 and 'número não confirmado na peça: 6 semanas' in t74b, t74b

        # caso 75 · matriz de 1: lote de 1 tese tem 0 pares, e 0 pares é válido
        # (editor de vídeo que corta 1 reels entrega 1 tese).
        s75 = nova_pasta('s75', '# Uma tese só\n\nlimpo\n',
                         'teses distintas: 1\n')
        cod75, t75 = rodar_conferir(s75)
        assert cod75 == 0, t75
        assert '0 pares (lote de 1 tese' in t75, t75

        # caso 76 · número por extenso em campo numérico. Coluna com algarismo
        # em outra célula + extenso reprova; coluna de rótulos sem número, não.
        s76 = nova_pasta('s76',
                         '# Verba\n\n| dia | verba |\n|---|---|\n'
                         '| 1 | R$ 15 |\n| 2 | seis reais |\n')
        cod76, t76 = rodar_conferir(s76)
        assert cod76 == 1, t76
        assert 'número por extenso em campo numérico: seis' in t76, t76
        # valor monetário por extenso em linha solta também reprova
        (s76 / 'peca.md').write_text('# Verba\n\nA verba diária é seis reais por dia.\n',
                                     encoding='utf-8')
        cod76b, t76b = rodar_conferir(s76)
        assert cod76b == 1 and 'número por extenso em campo numérico: seis' in t76b, t76b
        # coluna de rótulos sem número nenhum não dispara
        (s76 / 'peca.md').write_text(
            '# Fases\n\n| fase | nome |\n|---|---|\n| a | passo dois da base |\n',
            encoding='utf-8')
        cod76c, t76c = rodar_conferir(s76)
        assert 'número por extenso em campo numérico: 0' in t76c, t76c

        # caso 77 · <preencher> em QUALQUER arquivo da pasta (o teste do nicho do
        # webinar entregue em branco) conta como teste não feito.
        s77 = nova_pasta('s77', '# Um titulo\n\nlimpo\n')
        (s77 / 'teste-nicho-trocado.txt').write_text(
            'unidade 1 | substantivo trocado: <preencher> | sobrevive? <preencher>\n',
            encoding='utf-8')
        cod77, t77 = rodar_conferir(s77)
        assert cod77 == 1, t77
        assert '<preencher> em outros arquivos da pasta:' in t77, t77
        assert 'teste-nicho-trocado.txt' in t77, t77

        # caso 78 · o lint da pasta inclui conferencia/*.md: um travessão no
        # checagem-titulos.md (fora conferir.txt/ultimo) reprova.
        s78 = nova_pasta('s78', '# Um titulo\n\nlimpo\n')
        outro = garantir_conferencia(s78) / 'nota-conferencia.md'
        outro.write_text('nota com travessão — proibido\n', encoding='utf-8')
        cod78, t78 = rodar_conferir(s78)
        assert cod78 == 1, t78
        assert 'lint reprovou nota-conferencia.md' in t78, t78

        # caso 79 · rótulo multi-linha do próprio script (uma linha por hit do
        # grep) não conta como saída reescrita.
        s79 = nova_pasta('s79', '# Um titulo\n\nlimpo\n')
        (s79 / 'notas.md').write_text(
            'linha de cta no insumo: aula.md:5 manda BASE\n'
            'linha de cta no insumo: aula.md:9 manda BASE\n', encoding='utf-8')
        cod79, t79 = rodar_conferir(s79)
        assert 'rótulos do script com mais de uma lista: 0' in t79, t79

        # caso 80 · o gerador de render que reescreve a copy (.replace/.upper)
        # reprova; sem essas chamadas, passa.
        s80 = nova_pasta('s80', '# Um titulo\n\nlimpo\n')
        (s80 / 'gerar_card.py').write_text(
            'def render(copy):\n    txt = copy.replace("joelho", "planilha")\n'
            '    return txt.upper()\n', encoding='utf-8')
        cod80, t80 = rodar_conferir(s80)
        assert cod80 == 1, t80
        assert 'gerador reescreve a copy: gerar_card.py' in t80, t80

        # caso 81 · --render reprova nome de terceiro sem autorização no HTML,
        # antes do render (o pixel não desfaz depois).
        perf81 = d / 'perfil81.md'
        perf81.write_text('- nome do dono: Marina Souza\n- caso: Marcia, 52\n',
                          encoding='utf-8')
        html81 = d / 'card81.html'
        html81.write_text('<html><body><p>Marcia, 52 anos, voltou a subir.</p>'
                          '</body></html>\n', encoding='utf-8')
        cod81 = checar_render(str(html81), str(perf81))
        assert cod81 == 1, 'nome sem autorização no render tinha que reprovar'
        # com autorização no perfil, passa
        perf81.write_text('- nome do dono: Marina Souza\n'
                          '- caso: Marcia, 52, autorizado a aparecer\n', encoding='utf-8')
        cod81b = checar_render(str(html81), str(perf81))
        assert cod81b == 0, 'nome autorizado tinha que passar'

        # caso 82 · PEDIDO-PARA-QUEM-PUBLICA com as 3 linhas pro dono isenta os
        # comandos DENTRO dele; o mesmo comando no RELATO nunca é isento.
        s82 = nova_pasta('s82', '# Um titulo\n\nlimpo\n')
        (s82 / 'PEDIDO-PARA-QUEM-PUBLICA.md').write_text(
            '# Pedido\n\nO que é este arquivo: os passos pra publicar o doc.\n'
            'Pra quem mandar: quem tem acesso ao Drive.\n'
            'O que essa pessoa vai fazer: subir o arquivo e me devolver o link.\n\n'
            'Rode `gog drive upload doc.md`.\n', encoding='utf-8')
        cod82, t82 = rodar_conferir(s82)
        assert cod82 == 0, t82
        assert 'pedido a quem publica isento' in t82, t82
        # sem o cabeçalho, o comando volta a reprovar
        (s82 / 'PEDIDO-PARA-QUEM-PUBLICA.md').write_text(
            '# Pedido\n\nRode `gog drive upload doc.md`.\n', encoding='utf-8')
        cod82b, t82b = rodar_conferir(s82)
        assert cod82b == 1 and 'comando entregue ao dono' in t82b, t82b

        # caso 83 · conserto 8 (r14a): os arquivos que o próprio --conferir grava
        # (conferir.txt, conferir.ultimo.txt, conferir.ultimo-check.txt) ficam
        # fora do lint da pasta na re-execução. Sem isso o self-lint pega o jargão
        # que o gate imprimiu e reprova o plano-negocio na segunda passada.
        s83 = nova_pasta('s83', '# Um titulo\n\nlimpo\n')
        cod83a, _ = rodar_conferir(s83)          # 1ª passada grava conferir.txt
        assert cod83a == 0
        cod83b, _ = rodar_conferir(s83)          # 2ª passada grava conferir.ultimo.txt
        assert cod83b == 0
        # mesmo com um nome-variante do arquivo de saída na pasta, o lint o ignora
        (garantir_conferencia(s83) / 'conferir.ultimo-check.txt').write_text(
            'Ação 4 em RELATO.md:52\nAção 1 em RELATO.md:59\n', encoding='utf-8')
        cod83c, t83c = rodar_conferir(s83)
        assert cod83c == 0, t83c
        assert 'jargão sem tradução' not in t83c, t83c

        # caso 84 · conserto 6 (r14a): peça renderizada em 2 temas (claro/escuro).
        # O universo nasce da COPY fonte (titulos.txt), um por CARD, não um por
        # PNG, e o PEDIDO-DE-IMAGEM que sobra no topo fica fora do universo.
        s84 = d / 's84'
        s84.mkdir()
        (s84 / 'PEDIDO-DE-IMAGEM-cards.md').write_text(
            '# Pedido de imagem\n\n## foto 1\n## foto 2\n', encoding='utf-8')
        for tema in ('claro', 'escuro'):
            sub = s84 / tema / 'cards'
            sub.mkdir(parents=True)
            for i in range(1, 4):
                (sub / f'slide-{i:02d}.png').write_bytes(b'\x89PNG\r\n')
        # titulos.txt = um por card + o H1: 3 cards + 1 = 4
        (garantir_conferencia(s84) / 'titulos.txt').write_text(
            'H1 da capa\ncard um\ncard dois\ncard tres\n', encoding='utf-8')
        chk_em(s84).write_text(
            base_ok.replace('títulos no lote: 1', 'títulos no lote: 4'), encoding='utf-8')
        cod84, t84 = rodar_conferir(s84)
        assert 'universo: titulos.txt' in t84, t84
        # 6 PNG (3 cards x 2 temas) colapsam pra 3 cards; titulos.txt tem 4 (>= 3)
        assert 'peças renderizadas na pasta: 3' in t84, t84
        assert 'títulos na peça: 4 · na checagem: 4' in t84, t84
        assert cod84 == 0, t84

        # caso 85 · conserto 7 (r14a): --fonte isenta a régua de títulos do
        # cabeçalho HERDADO de outra skill, igual já isenta marcador longo e nome.
        # Um H1 que bate o padrão de rótulo mas veio idêntico da fonte sai como
        # `achado na fonte`, fora do exit.
        fonte85 = d / 'fonte85.md'
        fonte85.write_text(
            '# Régua de nutrição do programa\n\nCorpo herdado da skill de origem.\n',
            encoding='utf-8')
        s85 = d / 's85'
        s85.mkdir()
        (s85 / 'regua.md').write_text(
            '# Régua de nutrição do programa\n\nCorpo herdado da skill de origem.\n',
            encoding='utf-8')
        chk_em(s85).write_text(base_ok, encoding='utf-8')
        # sem --fonte, o H1 com "Régua" bate o padrão de rótulo e reprova
        cod85a, t85a = rodar_conferir(s85)
        assert cod85a == 1 and 'cabeçalho de peça pública é rótulo' in t85a, t85a
        # com --fonte, o mesmo H1 sai como achado na fonte, fora do exit
        cod85b, t85b = rodar_conferir(s85, fonte=str(fonte85))
        assert 'achado na fonte: cabeçalho herdado' in t85b, t85b
        assert 'cabeçalhos de rótulo no miolo da peça pública: 0' in t85b, t85b
        assert cod85b == 0, t85b

        # caso 86 · aspa atribuída a pessoa tem que ter lastro no insumo. O modelo
        # inventa a fala do cliente e carimba a prova; o script lê a aspa contra o
        # insumo, cego ao carimbo. Aspa-com-lastro passa, aspa-sem-lastro reprova,
        # e o "joelho ruim" inventado (paráfrase de uma frase real do insumo) pega.
        s86 = d / 's86'
        s86.mkdir()
        ins86 = s86 / 'insumos'
        ins86.mkdir()
        (ins86 / 'caixa.md').write_text(
            'Mensagens da caixa de entrada:\n'
            '1. Simone, 52: "isso serve pra mim?"\n'
            '2. Marcia: "eu ja tentei de tudo e nada resolveu a dor."\n',
            encoding='utf-8')
        peca86 = s86 / 'peca.md'
        args86 = argparse.Namespace(
            peca=[str(peca86)], titulos=None, teses=None, insumos=str(ins86),
            perfil=None, ressalva=None, nomes=None, lint=str(fonte_lint))

        # 86a · a aspa que existe idêntica no insumo passa (variando só o espaço e
        # a maiúscula, que a normalização perdoa); a headline da própria peça, sem
        # marcador de citação, NÃO é conferida como aspa (não pode virar falso+)
        peca86.write_text(
            '# Toda mulher que parou por dor no joelho, veja isto\n\n'
            'Uma cliente me escreveu: "Isso serve pra mim?"\n', encoding='utf-8')
        out = []
        code, falhas = montar(args86, out)
        txt = '\n'.join(out)
        assert code == 0, f'aspa com lastro tinha que passar: {falhas}'
        assert 'aspas de citação verificadas contra o insumo: 1 · sem lastro: 0' in txt, txt
        assert not any('aspa sem lastro' in f for f in falhas), f'headline não é citação: {falhas}'

        # 86b · o "joelho ruim" foi INVENTADO: o insumo só tem "isso serve pra
        # mim?", a peça atribui à cliente "isso serve pra mim, mesmo com o joelho
        # ruim?". Paráfrase que mudou a frase = verbatim fabricado, reprova.
        peca86.write_text(
            '# Um título de abertura qualquer\n\n'
            'Uma cliente me disse: "isso serve pra mim, mesmo com o joelho ruim?"\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args86, out)
        txt = '\n'.join(out)
        assert code == 1 and any('aspa sem lastro' in f for f in falhas), \
            f'a aspa inventada tinha que reprovar: {code} {falhas}'
        assert 'aspa sem lastro no insumo: "isso serve pra mim, mesmo com o joelho ruim?"' in txt, txt
        assert 'sem lastro: 1' in txt, txt

        # 86c · aspa longa idêntica ao insumo passa mesmo quebrada em duas linhas
        # no insumo (a normalização colapsa a quebra em espaço)
        (ins86 / 'aula.md').write_text(
            'A aluna contou que ela ja tentou\nde tudo e nada resolveu a dor.\n',
            encoding='utf-8')
        peca86.write_text(
            '# Título\n\nNo depoimento, a aluna: "eu ja tentei de tudo e nada resolveu a dor."\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args86, out)
        assert code == 0, f'aspa com lastro (quebrada no insumo) tinha que passar: {falhas}'

        # 86d · sem --insumos a verificação de aspa não reprova, só declara
        args86.insumos = None
        peca86.write_text(
            '# Título\n\nUma cliente me disse: "isso serve pra mim, mesmo com o joelho ruim?"\n',
            encoding='utf-8')
        out = []
        code, falhas = montar(args86, out)
        assert not any('aspa sem lastro' in f for f in falhas), \
            f'sem --insumos a aspa não reprova por lastro: {falhas}'
        assert 'verificação de aspa: sem --insumos' in '\n'.join(out), '\n'.join(out)

        # caso 87 · conserto extenso: número marcado [A CONFIRMAR] no perfil que a
        # peça publica POR EXTENSO dribla o grep do dígito. "seis semanas" sem
        # lastro PEGA; "três fases de quatro semanas" com lastro literal no dono.md
        # NÃO pega (é fato do próprio perfil, sem marcador).
        perfil87 = d / 'dono87.md'
        perfil87.write_text(
            '\n'.join(f'- campo {i}' for i in range(1, 29))
            # fato COM lastro (sem marcador): o extenso aqui é verdade do dono
            + '\n- estrutura do protocolo: três fases de quatro semanas cada\n'
            # dado marcado [A CONFIRMAR]: o prazo total é o que não tem lastro
            + '- prazo até o resultado: 6 semanas [A CONFIRMAR: número exato]\n',
            encoding='utf-8')
        # 87a · a peça escreve o dado marcado POR EXTENSO -> reprova igual ao dígito
        s87 = nova_pasta('s87', '# Um titulo\n\nEm seis semanas a subida volta.\n')
        cod87, t87 = rodar34(s87, fonte_lint, perfil=str(perfil87))
        assert cod87 == 1, t87
        assert 'número não confirmado na peça: 6 semanas (por extenso)' in t87, t87
        # 87b · o extenso COM lastro no perfil ("três fases", "quatro semanas") não
        # é número marcado, então não é alvo: a peça pode repetir sem reprovar
        (s87 / 'peca.md').write_text(
            '# Um titulo\n\nSão três fases de quatro semanas até a subida voltar.\n',
            encoding='utf-8')
        cod87b, t87b = rodar34(s87, fonte_lint, perfil=str(perfil87))
        assert cod87b == 0, t87b
        assert 'números não confirmados no perfil: 1 · publicados na peça: 0' in t87b, t87b

    print('checar_titulos.py self-test OK: lote, molde (lint + duas orações), exit por arquivo, '
          'ressalva somada no lote, marcador campo vs miolo, marcador acima de 6 palavras, '
          'palavra-chave de CTA literal nos insumos (inventada reprova) com automação no '
          'perfil, piso do perfil, teses e o par mais próximo, nomes com e sem autorização, '
          'nome candidato achado sem --nomes (conversa privada reprova, dono e handoff não), '
          'número de terceiro sem a tripla, afirmação de verificação sem saída crua, nicho '
          'trocado por unidade (título e fecho de bloco), matriz de TODOS os pares de teses, '
          'RELATO como bastidor fora do gate público, isenção do destinatário alcançável, '
          'marcador no html de render, e o --conferir inteiro (arquivo ausente, <preencher>, '
          'nicho, reescritos, inventário, títulos na peça iguais aos da checagem com a '
          'variação descartada fora da conta, teses distintas contra a matriz, html que abre, '
          'inventário duplicado, saída do script reescrita, consentimento com --insumos e '
          'lint de todo entregável), mais a coluna do substantivo trocado, a contagem de '
          'fecho contra a tabela, o conferir.txt gravado e o aviso da execução anterior, a '
          'exceção da --fonte, o universo da --peca-externa, a isenção do destinatário no '
          '--conferir e a medição da manchete no PNG. Mais o universo somado de peça não '
          'markdown (títulos do .html e dos slides do .pptx, e `sem peça varrível` no lugar '
          'do zero de varredura vazia), o deck lido de volta (lint no texto extraído e '
          'acentos contra o .md de origem), a linha de comando com caminhos absolutos na '
          'primeira linha do --conferir, e o exit do RELATO por último em linha própria. '
          'Mais a rodada 11: nome só em linha de bastidor de arquivo de planejamento ou '
          'dentro de bloco de código sai do gate público, cabeçalho de documento operacional '
          'sai do universo com a linha `universo:` declarada, os números do inventário '
          'recontados sobre a tabela, o tamanho em bytes conferido contra wc -c, a colisão '
          'de nome por nome contido e pela primeira palavra do nome composto, e o md5 do '
          'gate na primeira linha do conferir.txt com o aviso de versão. '
          'Mais a rodada 12: os arquivos exigidos pela ação (--exige, por nome ou '
          'glob), o conferir.txt preservado como prova de quem entregou com a '
          'execução nova em conferir.ultimo.txt (--gravar força), os arquivos do '
          'próprio gate fora da checagem de bytes, o cabeçalho de peça pública com '
          'padrão de rótulo entrando no universo com a isenção reduzida a FAQ, Bio, '
          'Índice, Sumário, Referências e Anexo, a peça sem H1, a conclusão que nega '
          'a saída colada na mesma checagem, a R7 como exit (versão morta na pasta, '
          'e 5% do universo acima de 20 títulos), o rótulo do piso trocado contra o '
          'grep do perfil, o número marcado [A CONFIRMAR publicado na peça, o .html '
          'de render no lint, e a última linha do fecho de reprova. '
          'Mais a rodada 13, o crivo do dono: o bastidor morando em conferencia/ '
          '(com o aviso na raiz e a reprova por pasta do dono com bastidor), o log '
          'e o cache de execução fora da raiz, o título em caixa alta com a isenção '
          'de sigla curta e de palavra-chave de CTA, o relato abrindo com Pronto, '
          'Abra primeiro e Falta você responder e fechando em Perguntas pra você, a '
          'pendência espalhada sem lista, o comando entregue ao dono fora de bloco '
          'cercado, o jargão interno sem glosa de até 4 palavras, o nome mantido no '
          'arquivo interno do dono e reprovado na peça pública, e a checagem gravada '
          'direto em conferencia/ pelo --gravar-checagem. '
          'Mais a rodada 14: o número não confirmado só reprova COM a unidade do '
          'perfil (dígito solto de série ou faixa não conta), a matriz de 1 tese '
          '(0 pares é válido), número por extenso em coluna com algarismo ou em '
          'valor monetário, <preencher> em qualquer arquivo da pasta, o lint da '
          'pasta incluindo conferencia/*.md (fora conferir.txt/ultimo), o rótulo '
          'multi-linha do próprio script fora do gate de saída reescrita, o '
          'gerador de render que reescreve a copy (.replace/.upper), o --render '
          'que reprova nome de terceiro sem autorização no HTML, e o '
          'PEDIDO-PARA-QUEM-PUBLICA isento do comando ao dono quando abre com as '
          '3 linhas pro dono. '
          'Mais os consertos da rodada 14 aberta: o bastidor no arquivo que o dono '
          'abre (tabela de destino de dado, veredito do gate, contagem desdobrada '
          'e saída literal) reprova como bastidor na peça pública; o arquivo de '
          'saída do gate (conferir.txt, .ultimo.txt e .ultimo-check.txt) fora do '
          'lint na re-execução; a peça renderizada em 2 temas com o universo pela '
          'copy fonte, um por card e não um por PNG; e o --fonte isentando o '
          'cabeçalho herdado, igual já isentava marcador longo e nome.')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog='checar_titulos.py',
        description='Imprime o bloco de fecho da régua de títulos já preenchido com os '
                    'números que saem de comando, pro agente colar em checagem-titulos.md.',
        epilog='DOIS PASSOS. Passo 1: rode sobre a peça e cole a saída INTEIRA em '
               'checagem-titulos.md, substituindo cada <preencher> e nada mais. Passo 2: '
               'rode --conferir <pasta> e cole a saída; exit diferente de 0 reprova a '
               'entrega inteira. Número escrito à mão diferente do impresso reprova. '
               'Exit 1 quando molde passa do teto, a ressalva passa de 1 no lote inteiro, '
               'marcador cai no miolo de frase, uma palavra-chave de CTA não existe literal '
               'nos insumos, o lint reprova um entregável, ou um nome de pessoa aparece sem '
               'autorização no insumo.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--peca', nargs='+', metavar='ARQUIVO',
                    help='a peça ou peças entregues (todos os entregáveis)')
    ap.add_argument('--titulos', metavar='ARQUIVO',
                    help='um título, headline, capa, assunto ou CTA por linha, extraído por você')
    ap.add_argument('--teses', metavar='ARQUIVO',
                    help='uma tese de até 4 palavras por linha (opcional)')
    ap.add_argument('--insumos', metavar='PASTA',
                    help='pasta de insumos do dono (transcrição, call, caixa de entrada, site)')
    ap.add_argument('--perfil', metavar='ARQUIVO', help='perfil do dono')
    ap.add_argument('--ressalva', metavar='FRASE',
                    help='a frase literal da ressalva clínica ou regulada (opcional)')
    ap.add_argument('--nomes', metavar='ARQUIVO',
                    help='nomes de pessoa presentes na peça, um por linha (opcional)')
    ap.add_argument('--lint', metavar='CAMINHO',
                    help='caminho do lint_copy.py (default: mesma pasta deste script)')
    ap.add_argument('--conferir', metavar='PASTA',
                    help='passo 2: relê o checagem-titulos.md já preenchido na raiz da pasta '
                         'de saída e confere (placeholder, campo do fecho fechado com a '
                         'mensagem de ajuda do próprio script, nicho, reescritos, inventário, '
                         'universo dos títulos, inventário duplicado, saída do script reescrita, '
                         'nome de conversa privada, marcador longo, '
                         'número de terceiro, afirmação sem saída crua e lint de todo '
                         'entregável). O universo de títulos soma .md, .html (title, h1, h2, '
                         'h3) e .pptx (título de cada slide), e sem nenhuma das três formas '
                         'imprime `sem peça varrível` no lugar do zero. O .pptx é lido de '
                         'volta: lint no texto extraído e acentos contra o .md de mesmo '
                         'nome-base. A primeira linha é o comando literal com os caminhos '
                         'absolutos, pra colar no RELATO, e o exit do RELATO.md sai por '
                         'último, em linha própria. Cabeçalho de documento operacional '
                         '(planejamento, prompt, relatório, wiki, spec, notas) fica fora do '
                         'universo de títulos de copy, e a linha `universo:` declara os '
                         'arquivos contados. Os números do inventário são recontados sobre a '
                         'tabela da pasta, e cada `<arquivo>: N bytes` do relato é conferido '
                         'contra wc -c. A primeira linha traz o md5 do gate. Aceita '
                         '--insumos e --perfil junto: sem '
                         'eles o gate de nome não roda; --fonte isenta o achado herdado e '
                         '--peca-externa conta o universo de títulos no arquivo auditado. '
                         'Grava a própria saída em conferir.txt na pasta; se ele já '
                         'existir, a prova anterior é preservada e a execução nova sai '
                         'em conferir.ultimo.txt (--gravar força a sobrescrita). Aceita '
                         '--exige com os arquivos que a ação roteada pede. Reprova '
                         'também: cabeçalho de peça pública com padrão de rótulo, peça '
                         'sem H1, conclusão que nega a saída colada na mesma checagem, '
                         'R7 sem versão morta colada, rótulo do piso trocado, número '
                         'marcado [A CONFIRMAR publicado na peça, e lint do texto '
                         'extraído do .html de render. R13: o bastidor mora em '
                         'conferencia/ (titulos.txt, teses.txt, nomes.txt, '
                         'checagem-titulos.md, conferir.txt e irmãos), e bastidor, '
                         'log ou __pycache__ na raiz da pasta do dono reprova. '
                         'Reprova também: título, headline, capa, assunto ou CTA em '
                         'caixa alta (8+ letras e 80%% ou mais em maiúscula; sigla de '
                         'até 6 letras e palavra-chave de CTA ficam de fora), RELATO '
                         'ou HANDOFF sem as 3 linhas `Pronto: · Abra primeiro: · '
                         'Falta você responder:` na abertura, pendência marcada sem a '
                         'seção final `Perguntas pra você`, comando entregue ao dono '
                         'fora de bloco cercado, e jargão interno da lista fechada sem '
                         'glosa de até 4 palavras. O nome de pessoa continua permitido '
                         'no arquivo INTERNO do dono (fila, dossiê, prospecção, '
                         'relatório), impresso como `uso interno`: a anonimização é da '
                         'peça pública')
    ap.add_argument('--exige', metavar='ARQUIVO1,ARQUIVO2',
                    help='B(b)1: os arquivos que a AÇÃO roteada exige na pasta de saída, '
                         'por nome ou glob, separados por vírgula. Arquivo ausente sai com '
                         'exit 1 e `arquivo exigido pela ação ausente: <nome>`. A lista por '
                         'ação mora no bloco de pronto da skill')
    ap.add_argument('--gravar', action='store_true',
                    help='C1(b)2: força sobrescrever o conferir.txt. Sem esta flag, um '
                         'conferir.txt já existente é preservado como prova de quem '
                         'entregou, e a execução nova sai em conferir.ultimo.txt')
    ap.add_argument('--fonte', metavar='ARQUIVO.MD',
                    help='exceção da fonte, pra skill que CONVERTE: marcador, nome e número '
                         'de terceiro que já existem literalmente neste arquivo saem como '
                         '`achado na fonte` e não contam pro exit. Só o que a conversão '
                         'introduziu reprova')
    ap.add_argument('--peca-externa', metavar='ARQUIVO', dest='peca_externa',
                    help='pra skill que AUDITA arquivo fora da pasta: o universo de títulos '
                         'é contado neste arquivo, e `títulos auditados: N` menor que ele '
                         'reprova')
    ap.add_argument('--render', metavar='ARQUIVO.HTML',
                    help='falha com exit 1 quando o html de render traz marcador de pendência: '
                         'marcador viraria pixel. Com PNG de mesmo nome-base na pasta, imprime '
                         'também `slide <n> | altura da manchete: P%% da arte` (alerta, nunca '
                         'falha)')
    ap.add_argument('--gravar-checagem', metavar='PASTA', dest='gravar_checagem',
                    nargs='?', const='.',
                    help='R13: grava a saída do passo 1 direto em '
                         '<pasta>/conferencia/checagem-titulos.md, sem colagem à mão. '
                         'Sem valor, usa a pasta da primeira --peca. O bastidor mora em '
                         'conferencia/ e a raiz da pasta fica com o entregável e o handoff')
    ap.add_argument('--selftest', '--self-test', '--test', action='store_true',
                    dest='selftest', help='roda o self-test e sai')
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.render:
        code_r = checar_render(args.render, args.perfil)
        if not (args.conferir or args.peca):
            return code_r
    else:
        code_r = 0
    if args.conferir:
        lint_path = Path(args.lint) if args.lint else AQUI / 'lint_copy.py'
        if not lint_path.exists():
            print(f'lint_copy.py não encontrado: {lint_path}', file=sys.stderr)
            return 2
        return conferir(args.conferir, lint_path, args.insumos, args.perfil,
                        args.fonte, args.peca_externa, args.exige,
                        args.gravar) or code_r
    if not args.peca:
        ap.error('--peca é obrigatório (a peça ou peças entregues), '
                 'ou use --conferir <pasta> / --render <arquivo.html>')

    out = []
    code, falhas = montar(args, out)
    texto_saida = '\n'.join(out)
    print(texto_saida)
    # R13 · a gravação é uma só: o passo 1 escreve o próprio bloco em
    # conferencia/checagem-titulos.md. Copiar e colar 17 KB à mão era o passo em
    # que a saída do script virava prosa reescrita.
    if getattr(args, 'gravar_checagem', None):
        alvo_pasta = args.gravar_checagem
        if alvo_pasta == '.' and args.peca:
            alvo_pasta = Path(args.peca[0]).resolve().parent
        try:
            destino = garantir_conferencia(alvo_pasta) / 'checagem-titulos.md'
            destino.write_text(texto_saida + '\n', encoding='utf-8')
            print(f'\nchecagem gravada em {destino}')
        except OSError as e:
            print(f'\naviso: não deu pra gravar a checagem ({e})')
    code = code or code_r
    if falhas:
        print('\nREPROVA, e a entrega não sai:')
        for f in falhas:
            print(f'  x {f}')
        print('Conserte a peça e rode de novo. Exit 0 é a última coisa que acontece.')
    return code


if __name__ == '__main__':
    sys.exit(main())
