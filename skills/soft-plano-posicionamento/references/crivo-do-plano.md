# O Crivo do Plano (a tabela do gate, preenchida e impressa antes do handoff)

Este é o gate bloqueante do Plano de Posicionamento. Roda no Plano completo, antes de ele virar
fundação das outras skills. Preencha cada linha com ✓ ou ✗ e a evidência (a fala citada, a frase
testada). **Sem a tabela impressa, o Plano não passou.** Uma linha ✗ reprova o Plano inteiro e
re-roda o bloco que falhou. Plano fraco vira entrada podre pra todas as outras skills.

Cobre as duas metades: a Parte A (Racional, os 3 blocos, as 2 saídas) e a Parte B (os 5 elementos de
Voz), porque a Voz vira o tom de toda copy depois.

| Check | Passa se | Onde | ✓/✗ + evidência |
|---|---|---|---|
| **Racional visível** | a seção 0 (território · o que vende · contra qual cultura luta · tensão dor para desejo · sentimento) está escrita e decide os blocos; não é lista rasa | `guia/02-plano-marca-pessoal.md` | |
| **Dor ancorada em fala literal** | toda dor do avatar citada bate em fala literal da pesquisa; dor inventada sem fala real = ✗ | `shared-references/crivo/01-entrada-verbatim.md` | |
| **Problema Avançado real** | é o que as OUTRAS soluções já geraram nele (a frustração e o trabalho que ele carrega), não a tática isolada nem o Problema Geral | `references/conducao-na-pratica.md` | |
| **O Grande Dominó existe** | há UMA tese-mãe que, se o lead aceita, a compra vira consequência; cabe em 1 frase e volta em todo conteúdo; tese frouxa ou óbvia = ✗ | seção do Racional | |
| **Mecanismo do Problema + da Solução** | o do Problema explica POR QUE ele está preso, não só descreve; o da Solução é o novo mecanismo único nomeado, desejável e vendável, com nome próprio mais fenômeno do domínio. Processo passo a passo sem mecanismo, ou premissa que cabe em qualquer concorrente = ✗ | `references/bloco-2-metodo.md` | |
| **Crenças contrapostas** | as principais crenças bloqueadoras estão mapeadas e o Mecanismo da Solução contrapõe cada uma; crença solta sem contraposição = ✗ | `references/conducao-na-pratica.md` | |
| **Clareza radical** | cada frase é simples, curta, forma a imagem mental certa, específica acima de abstrata; se exige energia mental pra entender, = ✗ | `guia/CODIGO-DE-ESCRITA.md` | |
| **As 3 perguntas na PUV e no Mecanismo** | dá pra ver? · dá pra falsificar? · **só você assina (o concorrente do nicho não diz igual)?** PUV ou mecanismo banal do nicho = ✗ | `shared-references/crivo/03-gate-cub.md` | |
| **Oferta por valor, não pelo bolso** | PUV + Equação de Valor (4 fatores) + níveis de acesso com o mesmo destino + entregável-tese + garantia; preço ancorado no valor gerado | `references/bloco-3-oferta.md` | |
| **Voz observada, não arquétipo** | os 5 elementos saíram da coleta do especialista (tom, narrativa, bastidor, valores, pilares), amplificados; nada de arquétipo de catálogo | `guia/03-identidade-voz.md` | |
| **Cliente-primeiro (idioma do nicho)** | zero jargão de cozinha vazado ("lead", "funil", "ticket"), zero traço do autor do método; é o vocabulário do cliente final DELE | `shared-references/filtro-cliente-primeiro.md` | |
| **Anti-IA (HARD), ÚLTIMA ação sobre o texto final** | roda sobre o doc consolidado pronto, não sobre o rascunho. **Conte os travessões longos (U+2014) no texto final inteiro, títulos, notas de STOP, corpo e oferta inclusos. Se a conta for maior que zero, o Plano NÃO passou: reescreve trocando por ponto ou vírgula e reconta até dar zero.** O mesmo pra `™`, `®` e pra família do verbo-freio banida pela régua anti-voz, o verbo que rima com "cravar" e suas flexões (exceção: aspa literal do dono). Sem frase-emoldura, sem verbo-clichê de hype. Com shell, roda `python3 scripts/lint_copy.py` no doc final e segue só com saída limpa; sem shell, busca à mão o travessão longo, o `™`, o `®` e o radical do verbo banido, e confere que a conta é zero | `shared-references/filtro-anti-ia/` | |
| **Regulado (DISPARO AUTOMÁTICO)** | se o nicho é saúde, jurídico ou finanças (fisioterapeuta, dentista, nutricionista, psicólogo, médico, enfermeiro, advogado, contador, consultor de investimento) o gate é OBRIGATÓRIO e nunca "não se aplica": a Promessa e a Projeção não podem cravar prazo nem desfecho garantido, e "resultado em X semanas" reprova. Troca por educação, mecanismo e processo, e adiciona a ressalva de que o resultado varia por pessoa, sem prazo garantido, com o pedido de confirmar a redação atual com o conselho da profissão. "Não se aplica" só quando o nicho comprovadamente não é regulado | `shared-references/crivo/04-gate-regulado.md` | |
| **VEREDITO** | **= o PIOR item acima.** Um ✗ qualquer = REPROVA e re-roda o bloco que falhou. Só tudo ✓ (ou "não se aplica" justificado) = PASSA e libera o handoff | | |

## Como preencher a coluna de evidência

Evidência é a citação, não o resumo. Errado: "a dor está ancorada". Certo: "ancorada na fala colhida
na pesquisa, 'o cachorro late o dia inteiro e o vizinho já reclamou duas vezes'".

No check anti-IA, a evidência é **número**, não adjetivo. Errado: "sem travessão". Certo:
"travessão longo U+2014: 0 no doc inteiro · verbo-freio banido e flexões: 0 · ™/®: 0".

## O que o Crivo não faz

Não reescreve o Plano. Ele dá veredito e devolve o bloco que falhou pra ser refeito no passo 5 da
Ação 1. Crítica linha a linha de copy pronta é de outra frente, a `soft-critico-copy`; aqui o objeto
é o Plano inteiro.
