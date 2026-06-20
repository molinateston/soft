---
name: soft-vendas
description: A venda consultiva do método Soft, o fechamento limpo. Transforma a conversa em cliente sem empurrar, revela a dor real e pede a decisão. Cobre script de venda (WhatsApp / call / reunião), prospecção no Direct, isolamento de objeção, diagnóstico de conversa empacada, copiloto em tempo real, métricas de pipeline e pós-venda (indicações + testemunhos). Puxa a Oferta e a PUV do Plano de Posicionamento. Use SEMPRE que envolver "script de venda", "venda", "vender", "cliente objetou", "objeção", "fechamento", "fechar", "follow-up", "prospecção", "DM/Direct", "WhatsApp", "lead sumiu", "lead frio", "não consigo cobrar caro", "cabeça do vendedor", "pipeline", "win rate", "CAC", "analisa essa conversa", "pós-venda", "pedir indicação", "testemunho". NÃO use pra carta/vídeo de aquecimento ou funil (isso é soft-funil), nem pra posicionamento ou conteúdo.
---

## 📦 O QUE ESTA SKILL PRODUZ

**Serve o agente:** braço-comercial do LEON (orquestrador) e cliente final direto — equipa quem vende e fecha o 1:1 high-ticket; também o copiloto que conduz a conversa ao vivo.

- **Script de venda por canal** — roteiro de fechamento para WhatsApp, call ou reunião presencial, montado pelo `script-builder` a partir da Oferta/PUV do Plano.
- **Mensagem de prospecção no Direct (DM)** — abordagem que abre conversa sem parecer spam (`prospeccao-dm`).
- **Isolamento e resposta de objeção** — uma objeção por vez, com respostas-modelo do `banco-de-objecoes`.
- **Diagnóstico de conversa empacada** — análise de print/transcrição de uma negociação travada e próximo passo (`analise-de-conversa`).
- **Copiloto de venda em tempo real** — conduz uma conversa ao vivo, mensagem a mensagem (`copiloto-tempo-real`).
- **As 7 fases da conversa de venda** — o roteiro-hub do diagnóstico que desce até a dor (`processo-conversao`).
- **Trabalho de mentalidade do vendedor** — a cabeça antes da técnica: sistema de crença, confiança no preço (`mentalidade-do-vendedor`).
- **Frameworks de venda consultiva adaptados ao Soft** — perguntas em escada, checklist de qualificação, ensinar/desafiar a visão, qualificação por dor, tamanho do problema, checklist de recorrência (`frameworks-consolidados`).
- **Arquitetura do Comercial 1:1 high-ticket + Conta de Padaria** — as 4 etapas da venda, o diagnóstico pelos números do próprio comprador, jogadas de fechamento (G4) e de confiança (Mid House), e o comercial operado por IA / Sócio IA (`comercial-1a1-e-conta-de-padaria`).
- **Métricas de pipeline** — lead → reunião → venda → ticket, win rate, CAC/LTV (`funil-e-metricas`).
- **Pós-venda** — pedido de indicação, coleta de testemunho e expansão de cliente (`indicacoes-pos-venda`).
- **Contrato de mentoria/consultoria pronto pra assinar** — gerado no mesmo fluxo depois do sim, em **`.docx`** (D4Sign/Clicksign/Autentique) ou, sem `/mnt/user-data/outputs`, em **markdown inline**; com cláusulas anti-calote, de pagamento, PF/PJ e por formato, mais glossário jurídico (`processo-contratos` + `clausulas-*` + `glossario-juridico`).

**Gate externo obrigatório:** todo texto que vai pro lead (script, DM, follow-up) passa antes pelo `shared-references/crivo/` — o gate CUB bloqueante (Confusão · Inacreditável · Tédio). Mensagem genérica ou promessa sem chão é consertada antes de sair.

# Soft Vendas, a venda consultiva (fechamento limpo)

Transforma a conversa em cliente **sem empurrar**. A venda Soft não convence à força: ela **revela a dor que já existe** e pede a decisão. Quando o Plano está de pé, o lead chega quente da carta e aqui você **confirma, não convence**, mas a conversa ainda precisa ser conduzida, e é isso que esta skill faz.

**Puxa do Plano** (a Oferta, a PUV, o Mecanismo e a Voz da `soft-posicionamento`): o script é a oferta do Plano virando conversa. Sem Plano, volta.

## A fonte e a lei
- Guia: `guia/10-vendas-consultivas.md` (a mecânica). Fonte da verdade.
- `guia/CODIGO-DE-ESCRITA.md`: pegada falada, **simples e honesto, nunca fácil e mágico**, sem travessão na copy.
- **O eixo:** o lead vive o **teto** (preso, comparado por preço, refém da operação); "invisibilidade/percepção" é o teu diagnóstico, não a fala da conversa. Fala pelo teto que ele sente.
- Filtros anti-ia + cliente-primeiro (não vaza Léo nem jargão de cozinha) antes de qualquer texto sair: `shared-references/filtro-anti-ia/` e `filtro-cliente-primeiro.md`.

## A mecânica (Igor Mello + frameworks consolidados)
- **Diagnóstico que desce** do fato neutro à dor que o cliente **nomeia com a própria boca**. Não se entrega a dor pronta, se conduz até ele dizer.
- **Revela dor real, NUNCA inventa.** A mesma escada que revela a verdade pode fabricar urgência, o Soft só usa a primeira. Lead sem a dor real, solta, não empurra.
- **Isola a objeção** (uma de cada vez) antes de responder.
- **Pede o sim ou o não no fim.** Sem follow-up eterno, sem perseguir quem não decide.
- **Filtra E convence:** não trabalha com quem precisa ser arrastado. Trabalha com quem já sentiu o teto e cansou dele.
- **Cabeça antes da técnica:** a mentalidade do vendedor (sistema de crença, confiança no preço) vem antes de qualquer script.
- **Marketing qualifica, Comercial vende.** Todo funil Soft entrega o "sim do produto"; aqui você fecha o "sim da venda" no 1:1 — high-ticket (3k+) nunca fecha sozinho no checkout. As 4 etapas (abertura/investigação/demonstração/obtenção de compromisso) e a **Conta de Padaria** (diagnóstico pelos números do próprio comprador) → `references/comercial-1a1-e-conta-de-padaria.md`.

> **Passo 0, sempre: le o perfil do usuario** (`shared-references/crivo/00-perfil-do-usuario.md`). Avatar, fonte de VoC, banco de provas, voz e nicho sao DELE, nunca os do Leo (que sao so um perfil de exemplo). Usuario sem perfil (cold start) e roteado pro onboarding (Plano na `soft-posicionamento` + mineracao de VoC no `01-entrada-verbatim.md`) antes de produzir, em vez de assumir os dados do Leo.

## Como conduz (por pergunta, nunca despeja)
1. Confirma o Plano (Oferta + PUV + Mecanismo + Voz). Sem ele, volta pra `soft-posicionamento`.
2. Pergunta o estágio: prospecção no Direct? script (WhatsApp / call / reunião)? uma objeção específica? diagnóstico de uma conversa que empacou? copiloto em tempo real? pós-venda (indicação / testemunho)?
3. Puxa o reference certo (`processo-conversao` é o hub) + os densos da etapa.
4. Escreve ou conduz, mostra, ajusta, passa no filtro anti-ia e no gate `shared-references/crivo/` (CUB bloqueante), entrega.

**Consulta `references/conducao-na-pratica.md` o tempo todo** — é o jeito de conduzir que faz a venda sair excelente (diagnóstico de mudança mental, não passo a passo · a nota 0-10 ancora · expectativa honesta, promete melhorar não 100% · mostra o case sem medo · ser pequeno é a vantagem · ofertas de risco/ancoragem/custo invisível · sistema de prova · vender liberta, sem mágica).

## References (densos, sob demanda)
`processo-conversao` (o hub: as 7 fases da conversa) + `script-builder` (monta o script por canal) · `prospeccao-dm` (DM de prospecção) · `mentalidade-do-vendedor` (a cabeça antes da técnica) · `banco-de-objecoes` (objeções e respostas) · `funil-e-metricas` (pipeline, win rate, CAC/LTV) · `indicacoes-pos-venda` (indicações + testemunhos + expansão) · `analise-de-conversa` (diagnóstico de print/transcrição) · `copiloto-tempo-real` (conduz uma conversa ao vivo) · `frameworks-consolidados` (perguntas em escada · checklist de qualificação · ensinar/desafiar a visão · qualificação por dor · tamanho do problema · checklist de recorrência, adaptados ao Soft).

**O Comercial high-ticket (1:1):** `comercial-1a1-e-conta-de-padaria` — a arquitetura do "+ Comercial" de todo funil (marketing qualifica / comercial vende), as 4 etapas da venda, a **Conta de Padaria**, as jogadas de fechamento high-ticket (G4) e de confiança (Mid House), e o comercial operado por IA (Sócio IA: automação de SDR, transcrição+probabilidade, follow-up pela objeção, lead score, roleplay).

**Contratos** (depois do sim): `processo-contratos` + as cláusulas (anti-calote · pagamento · PF/PJ · por formato) + glossário jurídico. Fechou a venda → gera o contrato de mentoria/consultoria no mesmo fluxo, sem trocar de ferramenta. **Entrega:** `.docx` em `/mnt/user-data/outputs/` (pronto pra D4Sign/Clicksign/Autentique); **fallback** — se esse diretório não existir, entrega o contrato como markdown estruturado inline no chat.

**Transversal:** `conducao-na-pratica` — o jeito de conduzir a venda destilado de sessões reais (diagnóstico de mudança mental, nota 0-10, expectativa honesta, case sem medo, ser pequeno como vantagem, ofertas na conversa, sistema de prova, vender liberta); exemplos de nichos neutros, nunca o Léo.

## Princípios
- **Confirma, não convence:** se a oferta do Plano é forte e a carta aqueceu, a conversa fecha confirmando a crença, não construindo do zero.
- **Honesto sempre:** simples e real, nunca fácil e mágico. O avatar já tomou pau de promessa mágica.
- **Pede decisão e respeita o não.** Lead que precisa de empurrão não é cliente, é problema futuro.

## Handoff
Venda fechada → os números (lead → reunião → venda → ticket) voltam pro LEON, que calibra a rotina. Cliente novo → o pós-venda abre indicações e testemunho (que viram prova pra `soft-posicionamento` e `soft-conteudo`).
