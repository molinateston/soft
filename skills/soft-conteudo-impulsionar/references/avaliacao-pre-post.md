# Avaliação pré-post, o duplo eixo antes de publicar ou turbinar

> Reference de profundidade do **Modo Avaliar** da soft-conteudo-impulsionar. O SKILL.md já traz o fluxo do modo autossuficiente; aqui mora o detalhe fino que não cabe no corpo sem inchar: a fórmula de engajamento, a extração do perfil dos 10% melhores, e como degradar com honestidade quando não há dado. Consulta quando a avaliação exige o cálculo cravado. A coleta Apify em si é a MESMA do resto da skill (mecânica no `references/metricas.md` e o comando no SKILL.md Passo 2 do modo turbinar); aqui só o que a avaliação faz com o dado.

## Índice
- 1. Por que dois eixos (empírico + doutrinário, e por que somam)
- 2. A fórmula de engajamento (e por que comentário pesa 3×)
- 3. Extração do perfil dos 10% melhores (o que sai de cada campo)
- 4. Os 5 critérios do eixo empírico, cada um contra qual dado
- 5. O eixo doutrinário, os 6 checks binários
- 6. Como degradar com honestidade quando NÃO há dado
- 7. Amostra pequena, dados velhos, perfil privado (os casos-limite)
- 8. A regra de ouro: toda correção cita um dado

---

## 1. Por que dois eixos (empírico + doutrinário, e por que somam)

A avaliação de uma peça responde DUAS perguntas diferentes, e o scorecard não colapsa num número só.

O **eixo doutrinário** pergunta **"isso está bom pelo padrão certo?"**. É prescritivo: mede a peça contra o método Soft (ancoragem, C/U/B, aponta pro método, filtra o cliente, clareza, anti-IA). Vale sempre, mesmo que o perfil do dono nunca tenha performado, porque o padrão é externo e fixo. É o mesmo padrão do Crivo da soft-leon.

O **eixo empírico** pergunta **"isso vai performar NO SEU perfil?"**. É diagnóstico, não prescritivo. Mede a peça contra o histórico real de engajamento daquele perfil específico. Uma peça pode ser impecável pelo método e ainda destoar do que aquele público responde (formato errado pro feed, gancho que morre no nicho, tamanho fora da faixa que engaja ali). O eixo empírico pega exatamente isso.

**Por que somar, não escolher um:** o empírico sozinho é cego ao futuro. Ele mede contra o passado, e o passado do perfil pode ser medíocre (se o dono sempre postou raso, "bater com o histórico" é bater com o ruim). O doutrinário corrige isso: puxa a peça pro padrão certo mesmo quando o histórico é fraco. E o doutrinário sozinho é surdo ao público específico daquele perfil. Juntos, um cobre o buraco do outro.

**Quando os dois eixos discordam, isso é informação, não erro.** "Forte no método, fraco no perfil" é um recado real (a peça é boa mas o público daquele feed não costuma responder a esse formato/gancho). "Bate com o perfil, falha no método" é outro recado (engaja mas não vira venda). O veredito nomeia qual dos dois casos é.

**Fronteira com os quadrantes (Passo 2.5 do modo turbinar):** o quadrante classifica peças que JÁ postaram, pelo que elas fizeram (reach × engajamento), pra decidir o que turbinar. A avaliação mede uma peça que AINDA NÃO postou, contra o padrão dos melhores, pra decidir se publica/turbina. Um é retrospectivo (o que já rodou), o outro é preditivo (o que vai rodar). Ambos bebem do mesmo perfil de engajamento real.

## 2. A fórmula de engajamento (e por que comentário pesa 3×)

Para cada post coletado, a nota de engajamento é:

```
nota = likesCount + (commentsCount × 3)
```

O comentário pesa 3× a curtida por dois motivos concretos: (a) custa mais ao usuário (escrever é mais que tocar no coração), então sinaliza interesse mais forte; (b) o algoritmo do Instagram premia comentário no alcance mais que curtida, então post com muito comentário tende a distribuir mais. O peso 3 é a convenção do sistema; se o perfil é de um nicho onde salvar/compartilhar importa mais que comentar e o dado de `saves` estiver disponível, você pode anotar isso na leitura, mas a fórmula-base fica em curtida + 3× comentário pra manter comparável.

**Não use taxa de engajamento por seguidor aqui.** O objetivo não é comparar o perfil do dono com outros; é comparar os posts do dono ENTRE SI pra achar os melhores DELE. Número absoluto de engajamento resolve isso e é mais estável que taxa (que oscila com variação de seguidores no período).

## 3. Extração do perfil dos 10% melhores (o que sai de cada campo)

Com os posts e a nota de engajamento calculada:

1. **Ordene** os posts pela nota (desc).
2. **Separe os 10% do topo.** Se o total é pequeno (< 20 posts), use os **3 melhores** e marque a leitura como baixa confiança (Seção 7).
3. Extraia, dos melhores, o "perfil de avaliação" (a régua que cada critério do eixo empírico consulta):

| Traço | Como extrair do dado | Vira a régua de |
|---|---|---|
| **Tipos de gancho** | lê a 1ª linha do `caption` de cada um dos melhores; classifica (número, contrário, afirmação-ousada, história, pergunta, confissão); soma a % de cada | critério "Gancho vs. histórico" |
| **Tamanho médio** | conta palavras do `caption` (ou nº de imagens no `Sidecar` pra carrossel); tira a média dos melhores | critério "Densidade" |
| **Formato dominante** | conta `type` entre os melhores (Image / Sidecar / Video); calcula quanto cada formato engaja vs. a média geral | critério "Formato/estrutura" |
| **Padrão de CTA** | procura no fim do `caption` dos melhores: "comenta X", "salva", "chama no direct", pergunta, nenhum; anota o mais comum | critério "Formato/estrutura" (CTA) |
| **Temas acima da média** | agrupa os `caption` por assunto; vê quais grupos concentram os melhores | contexto do veredito |
| **Ritmo** | tamanho médio de frase e nº de quebras de parágrafo nos melhores | critério "Aderência à voz" |

4. **Extraia também os 10% PIORES** e o padrão deles. Isso rende as correções mais afiadas: quando a peça em avaliação repete um traço dos piores, você diz "este post faz Y, e Y é o padrão dos seus posts que MORREM". É a prova mais forte de risco.
5. **Dado que não sai limpo vira `[A CONFIRMAR]`.** Se você não consegue classificar o gancho de metade dos melhores, não chute a %: reporte a incerteza.

O `type` do JSON Apify: `Image` = imagem única, `Sidecar` = carrossel, `Video` = reel/vídeo. Os campos que a avaliação lê são os mesmos da coleta (`likesCount`, `commentsCount`, `type`, `caption`, `timestamp`).

## 4. Os 5 critérios do eixo empírico, cada um contra qual dado

Cada nota (1 a 10) compara UM traço da peça com o perfil de avaliação. **8+ só quando o traço bate com um padrão dos 10% melhores.** Se bate com o padrão dos piores, a nota vai pra baixo (2 a 4).

1. **Gancho vs. histórico.** A 1ª linha da peça usa o tipo de gancho que domina os melhores dele? Ex.: melhores abrem com número 42% → peça que abre com número tende a 8+; peça que abre com pergunta (padrão dos piores) cai pra 3.
2. **Aderência à voz.** Tom, ritmo e tamanho de frase batem com os melhores? Viola padrão de ausência da voz (o que aquela voz NUNCA faz)? Frase muito mais longa/curta que a média dos melhores derruba.
3. **Densidade vs. os melhores.** A peça ensina/prova/conta no mesmo nível dos que engajaram? O tamanho está na faixa dos melhores? Metade da faixa é raso demais; dobro arrasta.
4. **Formato/estrutura.** O formato da peça é o que mais engaja pra ele? (Se carrossel engaja 2,3× o texto e a peça é texto, isso é um teto no critério.) O CTA está no padrão dos melhores?
5. **Encaixe no feed.** A peça some naturalmente no feed dele ou parece corpo estranho? Junta os traços acima num julgamento de "isto parece coisa que este perfil publica".

Soma /50. Faixas: 40+ alta chance · 25-39 média · abaixo de 25 baixa.

## 5. O eixo doutrinário, os 6 checks binários

Sempre roda (não precisa do histórico do perfil, precisa do método e do contexto de voz). Um ✗ qualquer = REFAZ naquele ponto.

| Check | PASSA se |
|---|---|
| **Ancorado** | nasce de fala real do avatar (verbatim) ou de prova real do dono; número inventado = ✗; sem fonte, `[A CONFIRMAR]` |
| **Aponta pro método** | deixa lacuna que fecha no que o dono vende; NÃO é conselho neutro que resolve tudo de graça (jornalismo) |
| **C/U/B (a Faca Soft)** | aumenta o motivo de COMPRAR (clareza/urgência/crença), não só o de olhar; curtida vazia que não aproxima da venda = ✗ |
| **Filtra o cliente certo** | atrai quem compra, não estranho; viral genérico ("5 hábitos de gente de sucesso") = ✗ |
| **Clareza (Lei 1)** | dá pra entender sem já ser de dentro; zero palavra difícil, zero figura vazia |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" · sem frase-emoldura ("a verdade é", "o segredo") · sem paralelismo negativo ("não só X, mas Y") · sem verbo-clichê. Ambiente com Bash roda `lint_copy.py`; no chat, CTRL+F manual de "—" e "travar" |

O detalhe de cada padrão banido e os falsos-positivos (pra não reprovar prosa autoral legítima) estão em `shared-references/filtro-anti-ia/`. A doutrina de C/U/B e "aponta pro método" está em `shared-references/crivo/05-premissas-mestras.md`.

## 6. Como degradar com honestidade quando NÃO há dado

Este é o ponto onde a maioria dos avaliadores erra: sem dado, cai num "benchmark de reserva" genérico e vende chute com cara de número. O método Soft não faz isso. **Sem dado real do perfil, você NÃO fabrica benchmark.** Você faz o seguinte:

1. Roda **só o eixo doutrinário** (Seção 5). Ele não precisa do histórico do perfil, precisa do método e do contexto de voz. Sempre dá pra rodar.
2. O eixo empírico sai no scorecard marcado **[SEM DADOS, só qualidade]**, com as 5 linhas vazias ou com "s/d", nunca com nota fabricada.
3. No fim, você **pede a coleta**: "pra completar o eixo de probabilidade (o que de fato engaja no seu perfil), preciso rodar a coleta dos seus posts (custa crédito Apify) num ambiente com terminal. Quer que eu faça?".
4. **O que você NUNCA faz:** escrever "seus melhores posts usam gancho de número" sem ter coletado, ou usar uma tabela de benchmark genérica ("média do nicho: 1.872 de engajamento") como se fosse dado do dono. Isso é invenção (Lei 5) e transforma um diagnóstico honesto em chute com cara de dado, que é pior que não ter dado nenhum.

O valor da avaliação sem dado ainda é real: o eixo doutrinário sozinho já é um Crivo de qualidade da peça. O que muda é que você é honesto sobre o que NÃO mediu, em vez de disfarçar o buraco.

**No app/chat (sem Bash):** não coleta (sem terminal pra Apify). Se o dono colar/já ter um export de posts, lê e usa; senão, roda só o doutrinário e marca o empírico [SEM DADOS], pedindo a coleta no Claude Code/agente. **No Claude Code e no agente/Telegram (têm Bash):** pipeline completo, coleta via Apify (avisando do custo), calcula o perfil, roda os dois eixos.

## 7. Amostra pequena, dados velhos, perfil privado (os casos-limite)

- **Amostra pequena (< 20 posts):** use os 3 melhores em vez dos 10%, e marque a leitura como **baixa confiança** no scorecard. Não crave "seu gancho campeão é X" com 3 posts; diga "nos seus 3 posts de maior engajamento, o padrão que aparece é X (amostra pequena, trate como indício, não lei)".
- **Dados velhos (> ~14 dias desde a coleta):** avise e ofereça atualizar antes de avaliar. O que engajava há meses pode ter mudado (público, algoritmo, fase do perfil).
- **Perfil privado / coleta falha:** não force. Reporte a falha e caia no ramo sem dados (Seção 6). A honestidade vale mais que um scorecard empírico fabricado.
- **Peça de formato que o perfil quase não tem:** se o dono quer avaliar um reel mas o perfil só tem posts de texto, diga que não há base histórica pra ESSE formato naquele perfil; avalie o gancho/voz/densidade que dá pra comparar e sinalize que o formato em si é uma aposta nova (sem histórico pra prever).

## 8. A regra de ouro: toda correção cita um dado

É a linha que separa a avaliação de um palpite. Nenhuma correção sai como opinião.

- **No eixo empírico**, o dado é do perfil: *"seus 10% melhores abrem com número (42%); este abre com pergunta (9%, e pergunta cai no seu terço pior). Troca por uma estatística tua."*
- **No eixo doutrinário**, o dado é o critério de método que falhou, com o local exato: *"não ancora: o número no slide 3 não tem fonte. Ou traz a origem, ou marca [A CONFIRMAR]."*
- **Correção proibida:** *"o gancho ficou fraco, melhore."* Sem dado, sem local, sem critério. Se você não tem o dado pra sustentar a correção, você não faz a correção: você pede o insumo que falta.

O teste antes de soltar qualquer correção: *"que número ou critério específico sustenta isso?"* Se a resposta é "nenhum, é minha impressão", a correção não sai.

**Limite da correção:** cada uma das até 3 correções é uma instrução curta ("seus melhores usam X, este usa Y, troque") mais NO MÁXIMO uma linha-exemplo curta, marcada como exemplo cuja versão final sai na soft-conteudo-[carrossel/reels/stories/headlines]. Proibido colar capa inteira, slide inteiro ou peça reescrita dentro da correção: isso é a skill de escrita fazendo o trabalho. A linha-exemplo É copy-de-cliente e passa no MESMO gate Anti-IA (zero travessão, zero clichê, zero negação clipada no rabo).
