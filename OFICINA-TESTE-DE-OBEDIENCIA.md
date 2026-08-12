# Teste de Obediência (processo da Oficina de Skills — 12/08)

Toda skill NOVA ou reformada passa por este teste ANTES de entrar no marketplace. A pergunta
que ele responde não é "a skill está bem escrita?" e sim: **o agente OBEDECE a skill quando
tem motivo pra desobedecer?**

## O protocolo (RED → GREEN)

1. **RED — roda o cenário SEM a skill.** Monta um pedido realista do público-alvo que a skill
   deveria governar, com PRESSÃO de verdade (3 ou mais ao mesmo tempo: pressa do dono, custo
   já gasto, cansaço de sessão longa, voz de autoridade mandando atalhar). Termina o pedido
   forçando escolha fechada A/B/C, nunca pergunta aberta.
2. **Colhe as desculpas VERBATIM.** Tudo que o agente inventar pra atalhar o método vira
   linha numa tabela `| Desculpa | Realidade |`. Essas frases são o alvo da skill, não o tema.
3. **GREEN — escreve/ajusta a skill mirando as desculpas colhidas.** Cada desculpa da tabela
   precisa de uma linha na skill que a mate pelo nome.
4. **Re-roda o MESMO cenário COM a skill.** Desculpa nova apareceu? Volta pro passo 2.
   Repete até o agente obedecer sob pressão (ciclos de 3 a 6 são normais).

## As duas leis que acompanham o teste

- **Description é GATILHO, nunca resumo do método.** Description que resume o processo faz o
  agente seguir a description e PULAR o corpo da skill (comprovado em teste de terceiros e
  compatível com o nosso histórico de "skill carregada e não cumprida"). Na description ficam:
  quando usar, quando NÃO usar, e nada do como.
- **Nenhuma alegação de conclusão sem evidência fresca.** Se o comando de verificação não
  rodou NESTA mensagem, o agente não pode dizer que passou. "Ótimo!" antes de verificar é
  bandeira vermelha. Violar a letra é violar o espírito.

## Onde roda

Na sala **Oficina de Skills (Fable)**: o dono manda a skill candidata, a Oficina executa o
protocolo com braços (um simula o usuário sob pressão, outro observa e colhe as desculpas),
mostra a tabela e o antes/depois, e só pede o "sobe" com o GREEN comprovado.
