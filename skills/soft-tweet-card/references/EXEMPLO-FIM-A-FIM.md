# Exemplo fim a fim (caso FICTÍCIO, nicho neutro)

> **Aviso: tudo aqui é FICTÍCIO.** Nome, handle, marca, números e resultados foram inventados só pra
> mostrar a FORMA de cada saída. Nada disso é caso real, nada disso pode ser copiado pra uma entrega
> de verdade. Num trabalho real, todo número e toda prova sem fonte nascem marcados `[A CONFIRMAR]`
> e o dono confirma antes de sair.

**O caso fictício:** um professor de natação que abriu turma de adulto iniciante. Ele já tem a copy
do carrossel escrita e quer os cards no formato print de tweet, porque é o que funciona no perfil
dele. Dono fictício: "Rafa Peixoto", handle `@rafanadaadulto`.

---

## 1 · O onboarding (primeira vez)

O brain do agente não tinha os dados de perfil, então as três perguntas foram juntas:

> Pra montar o cabeçalho do card eu preciso de três coisas suas:
> 1. Seu nome de exibição, exatamente como você escreve (acento incluído).
> 2. Seu handle, com arroba.
> 3. Um PNG quadrado do seu avatar, de pelo menos 400x400.

**Respostas:** `Rafa Peixoto` · `@rafanadaadulto` · o avatar ele mandou dois dias depois.

**No primeiro dia, sem avatar,** a skill renderizou com o placeholder e disse:

> "Renderizei com um círculo de placeholder no lugar do seu rosto, então esses cards estão marcados
> como rascunho e não dá pra postar assim: card sem avatar real não passa. Me manda um PNG quadrado
> do seu avatar, de pelo menos 400x400, e eu re-renderizo só o cabeçalho. A copy, os frames e o arco
> ficam iguais, é uma passada de 2 minutos."

Os três valores foram guardados no `config.local.md` da pasta da skill, e nas próximas vezes a skill
não perguntou de novo.

**A pasta de saída** não estava definida, então a skill usou o diretório de saída do ambiente e
declarou: "os cards caíram em `saida-natacao/turma-de-natacao-adulto/`".

## 2 · A copy que o dono deu

Ele colou 8 slides, escritos antes. A skill **não reescreveu nada**: nem fato, nem número, nem o CTA,
nem a ordem. Este formato veste a copy; quem escreve a copy é outra skill.

## 3 · A escolha dos tipos de frame, declarada antes de renderizar

> "Esse é o arco que eu montei. Confere antes de eu renderizar, porque depois é retrabalho:"

| Card | Tipo de frame | Trabalho dele no arco |
|---|---|---|
| 1 | texto puro, abertura grande | abrir com a punchline |
| 2 | citação | trazer a fala real do aluno |
| 3 | texto puro | tensionar |
| 4 | número | provar |
| 5 | tópicos | organizar os três pontos da primeira aula |
| 6 | conversa | o bastidor de uma mensagem que ele recebeu |
| 7 | texto puro | fechar o argumento |
| 8 | CTA | pedir o comentário |

São 5 tipos diferentes em 8 cards, dentro da régua de 5 a 8. Nenhum tipo aparece em dois cards
seguidos: os cards 3 e 7 são do mesmo tipo, mas estão separados por três cards.

**O que ele corrigiu:** o card 6 não tinha conversa nenhuma, era só mais um texto. A skill trocou o
frame antes de renderizar. Declarar a lista custou uma mensagem; descobrir isso no mosaico custaria
um render inteiro.

## 4 · O manifesto de entrada, colado no formato que o script lê

```python
CARROSSEIS["turma-de-natacao-adulto"] = [
    slide_texto("Adulto que não sabe nadar não tem medo de água.\n\nTem medo de ser visto tentando.",
                kw="ser visto", big=True),
    slide_texto("Eu pergunto isso na primeira aula e a resposta é quase sempre a mesma: "
                "'e se eu for o pior da turma?'"),
    slide_texto("Ninguém afunda por não saber nadar. Afunda por tentar não parecer que não sabe."),
    slide_kpi("Na turma de adulto iniciante:", "9 de 10",
              "nunca tinham colocado o rosto na água. [A CONFIRMAR]"),
    slide_chips("A primeira aula tem três coisas, e nenhuma é nadar.",
                [("Respirar", "boca fora, rosto dentro, sem pressa."),
                 ("Boiar", "o corpo flutua sozinho, você só atrapalha."),
                 ("Soltar", "a mão sai da borda quando você decidir.")],
                "Nadar vem na terceira.", kw="terceira"),
    slide_texto("A turma de adulto é fechada. Ninguém de fora olha, ninguém compara tempo."),
    slide_cta("Comenta NADAR que eu te mando o horário da próxima turma de adulto.", kw="NADAR"),
]
```

Os cards 2 e 6 (citação e conversa) usam frames do módulo de frames, importados e envolvidos com o
mesmo `wrap`, por isso não aparecem como `slide_*` na lista acima.

O `[A CONFIRMAR]` no card do número é regra: ele disse "9 de 10" de cabeça, sem lista na mão. Sai
marcado, e a skill avisou em 1 linha que ou ele confirma, ou o card sai do carrossel.

## 5 · O render e as duas versões

```bash
SAIDA_DIR=./saida-natacao PERFIL_NOME="Rafa Peixoto" PERFIL_HANDLE="@rafanadaadulto" \
  PERFIL_AVATAR=./avatar-rafa.png python3 scripts/build_tweet_cards.py
```

Saíram `slide-01.png` a `slide-08.png` mais `_mosaico.png`, na versão escura. A versão clara foi
gerada em seguida, porque ele não disse qual queria e a régua manda preparar as duas.

## 6 · A conferência do mosaico (com leitor de imagem)

> Abri o `_mosaico.png` e comparei com o padrão do formato.
>
> - Os 8 cards têm o mesmo cabeçalho no topo: avatar redondo, nome com o acento certo, selo azul,
>   handle. Nenhum selo verde.
> - Uma palavra verde por card, nada de frase inteira. O card 5 tinha "terceira" e também "três"
>   em verde: tirei o segundo.
> - Nenhum indicador de numeração em canto nenhum, como manda a regra deste formato.
> - Silhueta alternando: nenhum par de cards vizinhos tem a mesma forma.
> - Seta de arraste nos cards 1 a 7, ausente no 8. Correto.
> - Abri em tamanho cheio o card 5, que é o mais denso: os três tópicos couberam sem apertar.
> - Card 3: a palavra "sabe" ficou sozinha na última linha. Corrigi e re-renderizei só esse card.
>
> Rodei o verificador depois da correção: 8 cards, todos em 1080x1350, nenhum arquivo vazio,
> terminou sem falha.

## 7 · O STOP de aprovação

> "Esses são os cards. Algum precisa de ajuste antes de você postar?"

Ele pediu pra trocar a palavra verde do card 1, de "ser visto" pra "tentando". A skill editou só
aquele card e re-renderizou. **Nenhuma peça foi dada por pronta sem essa resposta:** o critério de
pronto é do dono.

## 8 · A entrega

- `saida-natacao/turma-de-natacao-adulto/slide-01.png` a `slide-08.png`, versão escura.
- `saida-natacao/turma-de-natacao-adulto-claro/slide-01.png` a `slide-08.png`, versão clara.
- `_mosaico.png` de cada versão.
- Um aviso de 1 linha: o número do card 4 continua marcado `[A CONFIRMAR]` e precisa da confirmação
  dele antes de postar.

---

## O que muda no caminho sem shell

Mesmo caso, ambiente sem shell: a skill não renderiza. Ela faz o onboarding igual, lê a receita
canônica igual, escolhe e **declara os tipos de frame igual**, e entrega o manifesto de entrada
pronto, exatamente no formato colado no item 4. Fecha com 1 linha: "está pronto pra renderizar; num
ambiente com shell é só definir as três variáveis de perfil mais a pasta de saída e rodar o script".

## O que este exemplo prova sobre o fluxo

1. Declarar os tipos de frame antes do render pegou um card errado por uma mensagem.
2. O aviso do avatar dá ao dono o caminho de conclusão, em vez de deixar a peça em rascunho sem
   explicação.
3. A conferência do mosaico encontrou duas coisas que o verificador não pega: a segunda palavra
   verde e a palavra órfã.
4. O STOP existe porque o dono trocou uma palavra que o agente teria dado por boa.
