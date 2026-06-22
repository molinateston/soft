# Manifesto de Funil, o trilho de invocação do LEON

> A certeza de invocação. O LEON não "lembra" qual mãe chamar nem em que ordem: ele segue o trilho. Pra cada funil, o pipeline explícito, em ordem, com o gate de cada passo. Sem gate cumprido, o passo não libera o seguinte.

O LEON orquestra e avalia; **não escreve peça e não exporta peça**. Cada passo abaixo é uma skill-mãe que produz o ativo e roda o **próprio gate** antes de devolver. O gate de copy (o Crivo) vive na skill de peça, nunca no LEON (ver `shared-references/operacao-padrao.md`, Seção 5). O papel do LEON é conferir que o gate rodou e que o ativo está de pé (segunda barreira: os 6 filtros do Crivo do LEON), e só então liberar a próxima etapa.

---

## FUNIL SOFT (degrau 1, o default)

A peça de aquecimento é a Mini Carta ou o Vídeo Minimalista. O lead aquecido cai no comercial 1:1. Pipeline:

```
soft-posicionamento  (gate: Crivo do Plano de Posicionamento)
        ↓
soft-conteudo        (gate: Crivo CUB + anti-IA / lint_copy.py)
        ↓
soft-designer        (gate: craft.py no design dos slides)
        ↓
soft-funil           (gate: Crivo, ancoragem em verbatim + CUB + anti-IA)
        ↓
soft-vendas          (gate: Crivo. O fechamento comercial 1:1 fica AQUI, nunca na soft-funil)
        ↓
pos-venda            (gate: Crivo. Indicação + testemunho, na soft-vendas)
```

Cada gate em uma linha:
- **soft-posicionamento**: o Plano (NMO) passa no Crivo do Plano antes de virar a fundação. Sem Plano de pé, nada depois tem destinatário.
- **soft-conteudo**: todo carrossel/reel/story passa no Crivo CUB e no anti-IA. Esses gates ficam DENTRO da soft-conteudo (em `soft-conteudo/shared-references/crivo/03-gate-cub.md`, `soft-conteudo/shared-references/filtro-anti-ia/` e `soft-conteudo/scripts/lint_copy.py`), nunca no LEON. Headline antes do corpo, corpo antes do design.
- **soft-designer**: o design dos slides passa no validador da própria soft-designer (`soft-designer/scripts/craft.py`) antes de exportar PNG. O LEON não hospeda esse script: ele só confere que rodou.
- **soft-funil**: a Carta / Vídeo / Página passa no Crivo (ancoragem em verbatim, prova com lastro, CUB + 3 perguntas do Harry, anti-IA). A peça qualifica; não fecha a venda.
- **soft-vendas**: o **fechamento comercial 1:1 é sempre aqui**. Scripts, objeções, fechamento e pós-venda passam no Crivo. A soft-funil aquece e qualifica; quem fecha é a soft-vendas.

---

## FUNIL WEBINAR (degrau 2)

Idêntico ao FUNIL SOFT em tudo, com duas diferenças: um **gate de maturidade** na entrada, e o **miolo** que troca a Carta pela soft-webinario. O resto (posicionamento, conteúdo, design, e o fechamento na soft-vendas) é igual.

```
gate de maturidade  (audiência + faturamento + produto + habilidade aguentam o degrau 2?
                     se não, fica no FUNIL SOFT)
        ↓
soft-posicionamento  (gate: Crivo do Plano)
        ↓
soft-conteudo        (gate: Crivo CUB + anti-IA / lint_copy.py)
        ↓
soft-designer        (gate: craft.py)
        ↓
soft-webinario       (no miolo, no lugar da Carta. Gates: ADMA + CUB + lint_copy.py)
        ↓
soft-vendas          (gate: Crivo. Fechamento 1:1, igual ao FUNIL SOFT)
        ↓
pos-venda            (gate: Crivo)
```

- **gate de maturidade**: o LEON só sobe o especialista pro degrau 2 quando audiência, faturamento, produto e habilidade pedem. Nunca antes. Não cabe? Fica no degrau 1.
- **soft-webinario**: entrega o pacote inteiro na ordem do método (oferta antes do roteiro, depois roteiro **ADMA** Atenção·Diagnóstico·Mecanismo·Ação, depois deck, gravação, páginas, e-mails/WhatsApp, anúncios, pós-webinar). Roda os próprios gates, todos DENTRO da soft-webinario: **ADMA** (estrutura do roteiro), **CUB** (`soft-webinario/shared-references/crivo/03-gate-cub.md`), **anti-IA** (`soft-webinario/scripts/lint_copy.py`), e `soft-webinario/shared-references/crivo/04-gate-regulado.md` se o nicho for saúde/jurídico. O webinar qualifica; high-ticket (3k+) fecha no 1:1, nunca no checkout.

---

## Degrau 3, FORA DE ESCOPO

O **Soft Launch / lançamento pago** (`soft-lancamento-pago`) é o degrau 3 da escada. **Está parqueado: fora do escopo desta orquestração autoguiada.** O LEON não conduz esse trilho por aqui. Quando o caso pedir lançamento pago, é outra condução, com skill própria.

---

## A lei do trilho

Não libera a etapa seguinte sem a anterior concluída e com o gate cumprido. A ordem é a engenharia: pular um passo não acelera, desalinha tudo que vem depois. O LEON alerta o risco uma vez, respeita a decisão de quem insiste em pular, mas registra o que fica torto.
