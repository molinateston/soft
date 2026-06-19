
# Soft Leon — Landing Page Completa

Constrói a página de vendas inteira, do hero ao botão final. Cobre qualquer produto, qualquer ticket. Aplica arquitetura de conversão comprovada filtrada pelo princípio editorial Soft: **a página não convence — ela torna a decisão inevitável pra quem já é o cliente certo.**

---

## Fundação (consulta na primeira invocação)

Antes de escrever qualquer seção, consulte:

1. **`guia/CODIGO-DE-ESCRITA.md`** — os 5 movimentos são obrigatórios em toda página
2. **`shared-references/dicionario-conversacional.md`** — tom, ritmo, vocabulário
3. **`shared-references/adaptacao-semantica.md`** — tradução para o campo semântico do nicho
4. **a frente de headlines (`soft-conteudo`)** — para headline e VSL hook

---

## 1. Princípio raiz

Uma página de vendas Soft **não empurra** — ela organiza o argumento de forma que o cliente certo chegue ao botão pensando *"seria idiota não entrar agora"*.

O cliente errado abandona antes do botão. **Isso é sucesso.**

> *Página que convence todo mundo não converte ninguém. Página que filtra na entrada converte os certos no fundo.*

Diferença crítica em relação à Carta Minimalista:

| Carta Minimalista | Landing Page |
|---|---|
| Argumento direto em texto corrido | Argumento em blocos visuais com hierarquia |
| Zero subtítulo, zero bullet | Bullets permitidos em seções específicas |
| Ticket alto, público quente | Qualquer ticket, inclui tráfego frio |
| Sem VSL | Com ou sem VSL |
| Preço fora (no WhatsApp) | Preço visível (tickets ≤ R$2k) ou no CTA |

---

## 2. Árbitro de arquitetura

A decisão de qual arquitetura usar depende de **3 variáveis**:

| Variável | Opções |
|---|---|
| **Ticket** | Baixo (≤R$497) · Médio (R$500–R$2k) · Alto (R$2k+) |
| **Tipo de produto** | Infoproduto · Mentoria/Consultoria · Serviço recorrente |
| **Temperatura do tráfego** | Frio (não conhece) · Morno (já viu conteúdo) · Quente (já seguidor) |

**Arquitetura por cenário:**

| Cenário | Arquitetura |
|---|---|
| Infoproduto ≤ R$497, qualquer tráfego | **Página VSL Completa** — vídeo carrega o argumento, página suporta |
| Infoproduto R$500–R$2k, tráfego frio/morno | **Página Híbrida** — VSL + blocos de texto robustos |
| Mentoria/Consultoria R$2k+, tráfego quente | **Página de Autoridade** — sem VSL, texto cirúrgico com seções de prova |
| Serviço recorrente, qualquer ticket | **Página Problema-Solução** — diagnóstico ampliado + método + acesso |

Consulte **`references/arquiteturas.md`** para a estrutura bloco a bloco de cada arquitetura.

---

## 3. Os blocos universais

Toda página, independente de arquitetura, passa pelos mesmos **14 blocos**. A ordem e o peso de cada um muda por arquitetura — mas nenhum some completamente.

| # | Bloco | Função | CTA aqui? |
|---|---|---|---|
| 1 | **Hero** | Para o scroll. Promessa + qualificação imediata | ✅ Botão primário |
| 2 | **VSL** (quando aplica) | Vídeo que carrega 60–80% do argumento | ✅ Botão abaixo |
| 3 | **Para quem é** | Filtra na entrada. Bullet de perfis concretos | Não |
| 4 | **O problema** | Nomeia a dor de 3ª Camada. Justifica falhas. | Não |
| 5 | **Mecanismo do problema** | Explica por que as soluções comuns falham | Não |
| 6 | **Apresentação do método** | Nome próprio + 3 diferenciais + contraste com mercado | ✅ Botão |
| 7 | **Prova social** | Cases com nome + número + condição inusitada | ✅ Botão |
| 8 | **O produto por dentro** | Módulos/etapas + o que ele aprende/conquista em cada um | Não |
| 9 | **Bônus** | Complementos que removem objeções específicas | Não |
| 10 | **Oferta + Empilhamento** | Ancoragem de valor → preço → o que leva | ✅ Botão |
| 11 | **Garantia** | Remove risco. Vendida como benefício, não como proteção | Não |
| 12 | **Sobre o autor** | Autoridade com pontos incomparáveis. Breve. | Não |
| 13 | **FAQ** | Mata objeções remanescentes em formato Q&A | ✅ Botão |
| 14 | **CTA final** | Urgência real + último botão | ✅ Botão |

Detalhe de copy para cada bloco: **`references/blocos-copy.md`**

---

## 4. VSL — quando e como

**Quando incluir VSL:**
- Ticket ≤ R$1.500 com tráfego frio/morno
- Produto complexo que precisa de demonstração
- Especialista com boa presença em vídeo

**Quando NÃO incluir:**
- Tráfego quente (já conhece o especialista — texto converte mais rápido)
- Ticket ≥ R$3k (página de autoridade converte melhor que VSL longo)
- Especialista sem fluência em câmera

**Estrutura do VSL Soft:**

| Bloco | Tempo | Função |
|---|---|---|
| **Hook** | 0–30s | Frase que para o scroll e qualifica quem assiste |
| **Empatia + Justificativa de falha** | 30s–2min | Confirma desconfianças. "Não era você." |
| **Inimigo-categoria** | 2–4min | Nomeia o problema sistêmico. Atirar pedra na prática. |
| **Credencial de procedência** | 4–6min | Quem é, como chegou a isso. História cirúrgica, não currículo. |
| **O método** | 6–15min | Nome próprio + 3–4 passos + contraste com mercado |
| **Prova** | 15–20min | 3–5 casos com nome + número + condição |
| **Oferta** | 20–25min | Empilhamento → preço → garantia → próximo passo |
| **CTA** | Últimos 30s | Instrução clara. Um botão. Uma ação. |

Roteiro completo do VSL: **`references/vsl-script.md`**

---

## 5. Regras invioláveis da página

1. **Zero menu de navegação.** Única saída é o botão. Direto pra WhatsApp ou checkout.
2. **CTA repete a cada 2–3 blocos** nos picos emocionais (após método, após prova, após garantia).
3. **Prova nunca é só elogio.** Todo depoimento tem: nome + nicho + resultado (número + prazo).
4. **Bônus mata objeção específica** — não é recheio. Cada bônus resolve 1 objeção nomeada.
5. **Garantia é vendida, não mencionada.** Tem headline própria, argumento, e apela para o lado do especialista.
6. **FAQ com copy** — cada resposta é uma mini-copy, não texto de SAC.
7. **Urgência real ou silêncio.** Nenhuma urgência fake. Se não tem escassez real, não menciona.
8. **Inimigo-categoria nomeado** em pelo menos 2 blocos da página (Problema + Mecanismo).
9. **Mobile-first.** Cada bloco funciona em 1 tela mobile sem scroll lateral.
10. **Faca Soft presente.** A página descreve resultado e função — nunca entrega o passo a passo.

---

## 6. Fluxo de execução

### Etapa 1 — Briefing

O que a skill precisa antes de escrever:

1. **Produto:** nome, formato (curso, mentoria, consultoria, serviço), o que entrega
2. **Ticket:** valor exato (ou faixa)
3. **Cliente ideal:** quem é, o que já tentou, qual é a 3ª Camada dele
4. **Método nomeado:** nome próprio + 3–4 etapas/passos
5. **Prova disponível:** cases reais (nome + número + prazo)
6. **Bônus disponíveis:** o que tem, pra que serve cada um
7. **Temperatura do tráfego:** frio, morno ou quente
8. **Destino do botão:** WhatsApp, Hotmart/Eduzz, checkout próprio

Se faltar informação crítica, pergunta antes de escrever.

### Etapa 2 — Escolha de arquitetura

Com base no briefing, declara qual arquitetura vai usar e por quê. Uma linha. Sem pergunta.

### Etapa 3 — Estrutura em outline

Entrega um outline numerado dos blocos com headline de cada um para aprovação. Cliente vê o esqueleto antes do corpo.

### Etapa 4 — Página completa

Escreve todos os blocos em sequência, em artifact markdown, com:
- Headlines de cada bloco
- Copy completa
- Marcações de onde ficam os botões de CTA
- Indicações de onde entram depoimentos/prints (quando o especialista não forneceu o texto real)

### Etapa 5 — Auditoria Blair Warren

Antes de entregar, passa pelos 5 movimentos:
1. **Sonhos** incentivados com cena + número?
2. **Falhas** justificadas sem condescendência?
3. **Medos** nomeados e dissolvidos com mecanismo?
4. **Desconfianças** confirmadas com verdade dura?
5. **Inimigo-categoria** nomeado sem ataque pessoal?

4–5 passam → entrega. 3 → reforça. ≤2 → reescreve.

---

## 7. References desta reference

- **`references/arquiteturas.md`** — estrutura bloco a bloco por arquitetura (VSL Completa, Híbrida, Autoridade, Problema-Solução)
- **`references/blocos-copy.md`** — copy detalhada de cada bloco com fórmulas, exemplos e anti-exemplos
- **`references/vsl-script.md`** — roteiro completo do VSL Soft com blocos e exemplos de abertura

---

## Regra única

> **Página não convence. Torna a decisão inevitável pra quem já é o cliente certo. Briefing primeiro. Arquitetura declarada. Outline aprovado. Página completa. Blair Warren auditado. Entrega limpa.**
