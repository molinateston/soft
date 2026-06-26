---
name: soft-vendas-posvenda
description: "Opera o PÓS-VENDA do método Soft, o que vem DEPOIS do cliente fechar: onboarding, nutrição da relação, pedido de indicação na hora certa e coleta de testemunho. Vira cliente entregue em vendedor sem pagar CAC; entrega antes de pedir, pede indicação só após resultado, e passa cada texto pelo gate antes de mostrar. Use quando o pedido for \"pós-venda\", \"posvenda\", \"indicação\", \"pedir indicação\", \"onboarding do cliente\", \"follow-up\", \"cliente novo fechou\", \"e agora que fechei\", \"como pego depoimento\", \"check-in\". NÃO use pro script da venda nova (soft-vendas-script), prospecção no Direct (soft-vendas-prospeccao), isolar objeção (soft-vendas-objecao), copiloto em tempo real (soft-vendas-copiloto), posicionamento (soft-posicionamento), funil/carta/landing/isca (soft-funil-carta/-miniwebinar/-landing/-isca), conteúdo de feed (soft-conteudo/-headlines/-carrossel/-reels/-stories/-multiplataforma), arte (soft-designer) ou webinário (soft-webinario)."
---

# Pós-venda, o cliente fechado vira vendedor

O cliente que já comprou é o ativo mais barato pra gerar a próxima venda. CAC quase zero, conversão 30-60%, lead chega quente. Mas só com sistema. Sem sistema, vira foto na parede: some, esquece em 6 meses, não indica, não dá testemunho. O pós-venda Soft extrai valor estruturado de quem já comprou, por três ativos: indicação, testemunho, expansão. A regra que rege tudo: **entrega valor primeiro, pede depois.** Indicação se ganha, não se pede genérico.

**O que esta skill faz por você:** monta o PÓS-VENDA: o onboarding que entrega resultado rápido + o pedido de indicação e o testemunho.

**As 4 leis (valem antes de tudo):** (1) nunca escreve como se o cliente já soubesse o contexto, zero palavra difícil, cria o contexto antes da afirmação; (2) abre ensinando o que faz; (3) é consultiva, puxa o contexto de você antes de gerar; (4) contexto é rei. (Detalhe em `shared-references/operacao-padrao.md`, Seção 0.)

**Este SKILL.md é o processo inteiro. Siga os passos na ordem, pare nos checkpoints, e rode o gate antes de mostrar qualquer texto.**

## Output Contract (o que você entrega)
- O **texto pronto** pro momento pedido (mensagem de onboarding, pergunta de indicação, modelo de apresentação, pedido de testemunho, mensagem de check-in), na voz do cliente, copiável.
- A saída é **limpa, como no Claude Chat**: o texto pronto + o momento da cadência marcado. O gate roda **por dentro** (auditoria silenciosa); a tabela NÃO vai pra saída.
- Você **para e espera** o OK antes de gerar o próximo ativo (não despeja onboarding + indicação + testemunho de uma vez).
- Você **nunca inventa número/resultado do cliente** e **nunca mostra texto que falhou no gate**.

## Passo 0, ancora antes de escrever (NÃO PULE)
Levanta o estado real do cliente, nesta ordem de fonte: **descrição do projeto** → **Plano/Oferta colado na conversa** → **mensagens anteriores**. Confirma três coisas antes de seguir:
- **Já entregou valor?** O cliente teve resultado concreto e mensurável (R$ entrando, processo resolvido, problema saiu do lugar)?
- **O cliente articulou o resultado na boca dele?** Tem fala literal de gratidão/resultado ("mudou meu negócio", "fechei 2 clientes")?
- **Quanto tempo de relação?** Geralmente 30-180 dias após o primeiro resultado.

Se NÃO houve resultado ainda, o pedido de indicação/testemunho está **fora de hora**: o passo certo é onboarding/nutrição (Passo 1 e 4), não pedir nada. Diz isso na cara, não força.

Qualquer número de resultado que você não confirmou na fonte entra como `[DADO: confirmar com o cliente]` e **não conta como ancorado**. Não inventa "fechou 2 clientes" plausível.

## Passo 1, onboarding (entrega antes de qualquer pedido)
Cliente novo fechou. O primeiro movimento é **entregar e setar expectativa honesta**, nunca pedir. Onboarding Soft:
- Confirma a próxima ação concreta (primeira sessão agendada, acesso liberado, primeiro marco).
- Repete a expectativa honesta da venda: o que o método entrega e onde não tem controle (não promete 100%).
- Marca o **ritual de feedback de resultado**: combina que o cliente reporta resultado (semanal ou mensal). Esse ritual é o que depois vira print, testemunho e gatilho de indicação. Instala agora, não improvisa depois.

Sem onboarding, não há resultado articulado; sem resultado, os outros ativos não existem.

## Passo 2, indicação só após o resultado (a hora certa)
Janela ideal: **30-90 dias após o primeiro resultado concreto**. O gatilho é o cliente dizer espontaneamente algo como "cara, mudou meu negócio" ou "tá funcionando". Cedo demais o cliente indica mal ou não indica; tarde demais a gratidão esfriou e vira "vou pensar".

Como pedir, estrutura Soft (specific, não "indica aí"):
- Aponta o **problema específico** que o cliente vivia ("quem você conhece que tá vivendo [o problema X que você vivia]?").
- Pede **3 nomes específicos**, nem 1 (entrega o óbvio), nem 5 (empaca e entrega genérico).
- Mostra que você já decidiu pedir (autoridade), pede pra ele pensar em 2-3 nomes que vêm na cabeça pra aquela situação.

Errado: "se conhecer alguém que precise, indica aí." Certo: pergunta dirigida ao problema + 3 nomes.

## Passo 3, facilita o ato de indicar (atrito mata indicação)
Cliente que quer indicar mas não sabe como, não indica. Entrega uma das três opções pra ele escolher:
- **Apresentação dirigida:** ele manda mensagem pro contato com o link da Carta; você dá o modelo pronto.
- **Modelo de apresentação:** texto curto que ele copia ("[Nome], queria te apresentar [especialista]. Me ajudou a [resultado] em [tempo]. Acho que faz sentido vocês se conhecerem.").
- **Indicação reversa:** você fala direto com o contato usando o nome dele como referência, mandando o texto antes pra ele aprovar.

Quanto menor o atrito, mais indicação acontece. Quem pede e larga, não gera nada.

## Passo 4, nutre a relação (cadência sem virar gerente de conta)
O especialista solo não vira account manager, mas também não some. Cadência mínima viável:
- **Mensal:** mensagem de check-in não comercial (~5 min). Específica, não "como você tá?": cita algo do nicho dele que mudou, lembra dele por um contexto, oferece troca sem pauta.
- **Trimestral:** conversa estruturada de 30 min.
- **Anual:** pesquisa de satisfação + atualização do testemunho.

Cliente que recebe check-in lembra de você. Quem lembra, indica, recompra, dá testemunho. Quem fica 6+ meses sem contato esquece, e o esquecimento mata os três ativos. Pedido de indicação é **evento, não rotina**: não vira spam.

## Passo 5, testemunho (arma de venda, não decoração)
Testemunho é o que vende quando o especialista não está presente. Ordem de poder: **vídeo > áudio > print de mensagem real > texto**. Quanto mais humano (rosto, voz, espontaneidade), mais converte; texto polido vira propaganda. Pra extrair, manda as **3 perguntas-base**:
1. **Antes:** qual era a situação antes? O que tava emperrando?
2. **Depois:** o que mudou? Números, momentos, coisas concretas.
3. **Recomendação:** o que você diria pra alguém que tá hoje onde você tava?

Se o cliente empaca em gravar sozinho, marca call de 15 min, faz as perguntas ao vivo, grava e corta a parte boa. Banco de testemunhos vivo: 1 novo por mês, aposenta os antigos (caso velho perde força). Pede permissão escrita pra usar.

## Passo 6, expansão (antes do fim do ciclo)
Cliente fechado não termina o ciclo no fim do programa. Os três caminhos: recompra do mesmo programa, upsell pra avançado, cross-sell de oferta complementar. Timing manda: **antes do fim do ciclo** (15-30 dias antes) converte mais, porque o cliente engajado avalia o próximo passo dentro do fluxo; depois do fim ele avalia como compra nova. Apresenta como **informação, não pressão** ("quero que você saiba que existe"). Empurrar quebra a confiança que você construiu.

## Passo 7, roda o GATE por dentro (auditoria silenciosa, NÃO imprime)
Roda o gate em CADA texto **internamente** (auditoria silenciosa). Só texto com VEREDITO=PASSA vai pro cliente. Um ✗ qualquer = refaz a frase. A tabela abaixo é o teu **checklist interno**, nunca a saída: o usuário recebe só o texto limpo (Passo 8), jamais a tabela.

| Check | Passa se | ✓/✗ |
|---|---|---|
| **Entregou antes de pedir** | houve onboarding/entrega de valor antes de qualquer pedido de indicação ou testemunho. Pedir na largada, sem resultado = ✗ automático | |
| **Hora certa da indicação** | pede só após resultado concreto + articulado pelo cliente (janela 30-90 dias). Pedir sem resultado = ✗ | |
| **Nutre a relação** | há cadência de contato (não some 6 meses); pedido é evento, não spam | |
| **CTA de indicação específico** | aponta o problema específico + pede 3 nomes + dá o modelo de apresentação. "Indica aí" / "se conhecer alguém" = ✗ | |
| **Ancorada no verbatim real** | resultado/fala citada é literal da fonte (com N real do autor); N inventado/plausível = ✗ automático; sem fonte vira `[DADO: confirmar]` | |
| **Harry, dá pra ver?** | fecha o olho e enxerga a cena/o resultado concreto. ✗ "tive uma boa evolução" · ✓ "fechei 2 clientes essa semana" | |
| **Harry, dá pra falsificar?** | é um fato falsificável, não um adjetivo bonito | |
| **Harry, só você diz?** | o pedido/prova carrega o mecanismo proprietário, não promessa banal do nicho | |
| **C/U/B** | Claro (uma ideia por frase, leigo entende) · Único (não é o "indica aí" de todo mundo) · Belo (lê em voz alta sem travar na boca) | |
| **CTA com destino** | todo texto pede UMA ação concreta com destino claro (pensa em 3 nomes / grava 5 min / responde até sexta), nunca um pedido vago | |
| **Anti-IA (HARD)** | zero travessão "—" · zero "travar/travado/destravar" (exceção: aspa literal do cliente) · sem frase-emoldura ("a verdade é", "o segredo") · sem verbo-clichê ("revoluciona, destrava, transforma"). **No chat (sem o lint), faz CTRL+F manual de "—" e da família "travar" antes de marcar ✓.** | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REFAZ. Só tudo-✓ = PASSA e vai pro cliente. | |

## Passo 8, mostra e PARA
Mostra **só o que passou, LIMPO** (como no Claude Chat): só o texto pronto + o momento da cadência marcado. Sem tabela de gate, sem meta. Pergunta "esse texto te serve? ajusto, ou vamos pro próximo ativo?". **Espera o OK** antes de gerar o próximo ativo (onboarding → indicação → testemunho → expansão é sequência, não pacote único). Não narra o fluxo ("agora vou auditar"), entrega limpo.

## When NOT to use (manda pra skill certa)
- Pediu o **fechamento / script da venda nova** (WhatsApp, call, reunião) → **soft-vendas-script**.
- Pediu **prospecção no Direct / DM pra lead frio** → **soft-vendas-prospeccao**.
- Pediu pra **isolar uma objeção** específica → **soft-vendas-objecao**.
- Pediu **copiloto em tempo real** durante a conversa → **soft-vendas-copiloto**.
- Pediu **posicionamento / Oferta / PUV** → **soft-posicionamento**.
- Pediu **carta / mini-webinar / landing / isca** → **soft-funil-carta/-miniwebinar/-landing/-isca**.
- Pediu **conteúdo de feed** (carrossel, reel, stories, headline) → **soft-conteudo** e família.

## Anti-Patterns (sintoma → correção)
| Sintoma | Correção |
|---|---|
| Pediu indicação na largada, antes de entregar | Volta: onboarding primeiro; indicação só após resultado concreto + articulado |
| CTA "se conhecer alguém, indica aí" | Aponta o problema específico + pede 3 nomes + dá o modelo de apresentação |
| Pediu 1 nome (ou 5) | Sempre 3: 1 entrega o óbvio, 5 empaca em genérico |
| Cliente quer indicar e não sabe como | Entrega uma das 3 opções de facilitação (apresentação dirigida / modelo / reversa) |
| Sumiu após fechar, lembrou 6 meses depois | Instala cadência mensal de check-in específico, não comercial |
| Pedido de indicação virou rotina/spam | Pedido é evento (após marco), não mensagem recorrente |
| Inventou "fechou 2 clientes" plausível | Só resultado REAL da fonte; sem fonte, `[DADO: confirmar]` e não conta como ancorado |
| Testemunho em texto polido | Sobe pro formato mais humano possível (vídeo > áudio > print); manda as 3 perguntas-base |
| Ofereceu expansão como pressão | Apresenta como informação ("quero que você saiba que existe"), antes do fim do ciclo |
| Narrou o fluxo ("agora vou auditar") | Executa em silêncio, entrega só o texto limpo |
| Imprimiu a tabela do gate na saída | O gate é INTERNO (auditoria silenciosa); a saída é só a peça limpa |

## References (só pra profundidade, o fluxo acima é autossuficiente)
- `references/indicacoes-pos-venda.md`: os 3 ativos detalhados (timing, formatos, modelos prontos), cadência de manutenção, métricas do pós-venda (taxa de indicação >40%, conversão >40%, testemunho >50%, recompra >25%) e os 10 princípios não-negociáveis. É o mesmo processo acima, com mais exemplo.
- `references/conducao-na-pratica.md`: o porquê por trás da entrega humana, o sistema de prova ("chegam pelo número, ficam pelo processo"), expectativa honesta e a postura que faz o cliente virar vendedor.
- `shared-references/crivo/`: o gate de saída detalhado (ancoragem no verbatim, simulação na pele do cliente, gate CUB bloqueante + as 3 perguntas do Harry). É o mesmo gate do Passo 7, com mais detalhe.
- `scripts/lint_copy.py`: no Claude Code, roda `python3 scripts/lint_copy.py` no texto como cinto extra do anti-IA (reprova em-dash e "travar"). No chat não roda, por isso o CTRL+F manual do gate.
