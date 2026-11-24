# Provedores de IA por API que o LEON aceita

**Testado** quer dizer: houve chamada real com chave verdadeira em 23/11/2026, naquele endereço e com aquele modelo. **Não testado** quer dizer: nenhuma chamada real registrada naquele endereço. Uso do mesmo fabricante por outra rota não conta (o MiniMax testado pelo OpenRouter não prova o endereço direto da MiniMax).

Custos são **estimativas de 23/11/2026** para um pedido de cerca de 7 mil tokens, e valem só para os modelos citados. Os demais não foram medidos. Preço muda: confira no painel do provedor.

| Provedor | Endereço (URL base) | Modelo padrão | Custo estimado por pedido de 7 mil tokens | Tradutor | Teste real |
|---|---|---|---|---|---|
| DeepSeek | https://api.deepseek.com/anthropic | deepseek-v4-pro | deepseek-v4-pro: cerca de US$ 0,0023. deepseek-flash: cerca de US$ 0,0006 com cache | não | testado: deepseek-v4-pro e deepseek-flash |
| GLM (Z.ai) | https://api.z.ai/api/anthropic | glm-5.3 | glm-5.3-flash: cerca de US$ 0,0005 | não | testado: glm-5.3 e glm-5.3-flash; glm-5.2 não testado |
| OpenRouter | https://openrouter.ai/api | minimax/minimax-m3.1-flash | MiniMax M3.1 Flash: cerca de US$ 0,0007 | não | testado: os 9 modelos do catálogo |
| MiniMax direto | https://api.minimax.io/anthropic | MiniMax-M3 | não medido | não | não testado |
| Kimi direto | https://api.moonshot.ai/anthropic | kimi-k3[1m] | não medido | não | não testado |
| Fireworks | https://api.fireworks.ai/inference | accounts/fireworks/models/kimi-k3 | não medido | não | não testado |
| NVIDIA | http://127.0.0.1:8798/nvidia | minimaxai/minimax-m3.1-flash | não medido | sim | não testado |
| xAI Grok | http://127.0.0.1:8798/xai | grok-4.7 | não medido | sim | não testado |
| Outro (formato Anthropic) | o que o provedor indicar, sempre https | o que o provedor indicar | ver no painel | não | depende |
| Outro (só formato OpenAI) | passa pelo tradutor | o que o provedor indicar | ver no painel | sim | depende |

Modelos do OpenRouter testados em 23/11/2026: minimax/minimax-m3.1-flash, deepseek/deepseek-v4.1-flash, z-ai/glm-5.3-flash, minimax/minimax-m2.7, moonshotai/kimi-k3.1-pro, openai/gpt-6-luna, nvidia/nemotron-3-ultra-550b-a55b:free, xiaomi/mimo-v2.6-flash e tencent/hy4-flash.

## Onde pegar a chave

| Provedor | Onde |
|---|---|
| DeepSeek | platform.deepseek.com, menu API Keys |
| GLM (Z.ai) | z.ai, área de API Keys da conta |
| OpenRouter | openrouter.ai, menu Keys |
| MiniMax | platform.minimax.io, área de API Keys |
| Kimi | platform.kimi.ai, área de API Keys |
| Fireworks | app.fireworks.ai, área de API Keys |
| NVIDIA | build.nvidia.com, botão de gerar API Key |
| xAI | console.x.ai, área de API Keys |

A conta precisa de crédito antes da primeira chamada, salvo período grátis do próprio provedor.

## Avisos

- **No provedor, o LEON só conversa.** Sem ferramentas, sem mexer em arquivos, sem skills. Para trabalho na máquina, volte com /claude ou /codex.
- **A falha de um provedor não troca o motor sozinha.** Saldo, chave ou provedor fora do ar: a sala fica nele e avisa. Você troca com /claude, /codex ou o atalho de outro provedor.
- **Modelos que pensam antes de responder:** relato de 23/11/2026 diz que o MiniMax M3.1 Flash sempre pensa; não conferido em fonte oficial. No teste, ele pode responder "o modelo só pensou e não escreveu; a chave está boa".
- **NVIDIA hospedada:** relato de 23/11/2026, de um blog e não verificado em fonte oficial, diz que ela é só para avaliação e tem limite de cerca de 40 pedidos por minuto.
- **NVIDIA e xAI passam pelo tradutor**, um programa ligado no servidor que converte as mensagens do formato OpenAI. Ligar o tradutor é serviço do suporte.
- **Chave nova:** o LEON costuma pegar a chave nova no próximo pedido. Se o provedor não aparecer em /motor em 1 minuto, peça ajuda ao suporte.
- **Cada provedor cobra por uso**, no seu cartão. Acompanhe o gasto no painel dele.

## Regras do cadastro (o que o script confere)

O cadastro é conferido pelo validador do próprio LEON antes e depois de gravar. Além disso, o script é **mais rígido** que o LEON em quatro pontos:
- endereço sempre https (o LEON aceita http para fora; o script só aceita http em 127.0.0.1 e localhost, que é o tradutor);
- endereço sem usuário ou senha embutidos (o LEON aceita `https://usuario:senha@...`; o script recusa);
- nome da chave sempre MOTOR_ seguido de maiúsculas, números ou _ (o LEON aceita outros nomes; o script recusa, para a chave do motor nunca esconder a chave de outra integração);
- modelo de provedor do catálogo sempre da lista do catálogo (modelo livre só pela opção outro).

E segue o LEON nestes: id com letras minúsculas, números e hífen, até 24, sem ser comando do LEON; id repetido recusado (inclusive id numérico que o LEON lê como texto); só formato Anthropic.
