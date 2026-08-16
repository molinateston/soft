---
name: soft-organizacao-vps
description: "Organiza a VPS Soft Soft: separa PROCESSO (engines, skills, réguas, lote em review) de ARQUIVO PRONTO (PNG/lotes finalizados). Usa hot path vs /root/_ARQUIVO/AAAA-MM-DD-motivo/, ciclo rascunho→review→aprovado→arquivo, mv (nunca rm em massa). Use quando o pedido for 'organizar VPS', 'arquivar lote', 'limpar carrosséis/ads prontos', 'quarentena', 'hot path', 'onde nasce peça', 'não misturar out-v5', checklist pós-lote. NÃO use pra redesenhar peça, escrever copy, renderizar arte, nem hard-delete em massa."
---

> 🔴 **REGRA DURA DE FRASE , "TODA FRASE SE EXPLICA SOZINHA"** (vale em TUDO que esta skill escrever pro público)
>
> Copy Soft é **frase que gera IMAGEM na cabeça de quem lê frio**. Não pode assumir que o leitor já sabe o assunto, o produto, a categoria, o método, o mecanismo ou o antes/depois. Toda frase que você escrever precisa se sustentar sozinha, sem depender do slide anterior, da bio, do título, ou do que "obviamente é". Frase curta que "soa punchy" e deixa o entendimento pro contexto é reprovada.
>
> **Teste antes de aprovar CADA frase:** "se essa frase caísse solta no scroll de uma pessoa que nunca ouviu falar do produto, ela entenderia O QUÊ + PRA QUEM + O RESULTADO CONCRETO?" Se não, REESCREVE nomeando explícito: qual é o objeto ("dieta", "calorias", "conta de calorias", não só "conta"), qual é o público ("mulher que já tentou emagrecer de todas as formas", não só "mulher que já tentou de tudo"), qual é o resultado concreto ("para de recomeçar a dieta", não só "para de recomeçar").
>
> **Ex reprovado →** *"Você come o que ama, um agente faz a conta do seu dia e você para de recomeçar."*
> **Ex aprovado →** *"Você passa a comer o que ama, um agente faz a conta de calorias do seu dia inteiro e não te deixa escorregar, e você para de recomeçar a dieta toda vez do zero."*
>
> Adicionar as 3-5 palavras que ancoram o contexto é MELHOR que a frase curta ambígua. Copy boa não é curta, é **inequívoca e imagética**. Frase que precisa de contexto pra ser entendida = frase quebrada, refaz.

> **REGRA-IRMÃ · "NENHUM VERBO ÓRFÃO" (cérebro preguiçoso do leitor):** o leitor tem cérebro preguiçoso e NÃO vai completar sua frase pra você. Todo verbo precisa vir com seu OBJETO NOMEADO na mesma frase, senão vira frase média. Verbos-armadilha que exigem complemento explícito: cortar (**cortar o quê?**), recomeçar (**recomeçar o quê?**), parar (**parar de quê?**), mudar, melhorar, escapar, largar, controlar, ajustar, resolver, virar, transformar. Sempre nomeia o objeto concreto (arroz, pão, doce, dieta, treino, agenda, cliente, valor), NUNCA deixa aberto.
>
> **Ex ✅ BOA (verbos ancorados + objetos nomeados):** *"Você come arroz, pão e o que ama, e uma ferramenta minha conta as calorias de tudo por você todo dia, pra você emagrecer sem viver de dieta."* , "come" tem objeto (arroz, pão), "conta" tem objeto (calorias), "emagrecer" tem contexto ("sem viver de dieta").
>
> **Ex ⚠️ MÉDIA (verbo órfão no fim):** *"…pra você emagrecer comendo o que gosta em vez de cortar."* , "cortar O QUÊ?" ficou pro leitor completar. Cérebro preguiçoso não completa, desiste. Correto: *"…em vez de cortar arroz, pão e doce."*
>
> Antes de aprovar a frase, sublinha mentalmente cada verbo e confere: cada um tem OBJETO nomeado? Não? Nomeia agora.

# Organização da VPS Soft Soft

**Papel:** skill operacional leve. Mantém a VPS legível: peça nova no hot path, peça pronta em `_ARQUIVO/`. Não escreve copy, não redesenha, não apaga em massa.

**Doc-mãe (fonte da verdade):** `/root/missao-conteudo/PROCESSO-ORGANIZACAO-VPS.md`

**Comando mental:** *peça nova aqui / pronta pra lá.*

## Quando usar

- Léo pede limpar / organizar / arquivar lotes prontos
- Agente vai editar e não sabe se a pasta é processo ou arquivo
- Pós-lote: rejeitados e intermediários ainda no hot path
- Risco de misturar out-v5, webinar antigo, Soft Soft CRS, ads KEEP

## Quando NÃO usar

- Redesenhar ads/carrosséis → `soft-designer` / engines Soft Soft
- Escrever headline/copy → skills `soft-conteudo-*`
- Hard-delete em massa (proibido)
- Inventar pasta nova que alimenta site no ar sem stub

## Passos (ordem)

1. **Ler o doc-mãe** e o README da quarentena ativa (se existir). Rodada 15/jul: `/root/_ARQUIVO/2026-07-15-limpeza-vps/`.
2. **Classificar** cada path: PROCESSO (manter) vs ARQUIVO PRONTO (mover) vs CANDIDATO (site no ar / KEEP → stub + pedir OK).
3. **Se limpeza da mesma data já roda:** completar o MANIFEST dela. Não abrir segunda quarentena. Não devolver pasta que ela acabou de mover.
4. **Se for limpeza nova:** criar `/root/_ARQUIVO/AAAA-MM-DD-motivo/` com README (o quê, por quê, como reverter) + lista origem→destino.
5. **Mover com `mv`** pra subpasta clara (`carrosseis-antigos/`, `banners-ads-antigos/`, `renders-webinar-leo/`, `zips/`).
6. **Stub README** no path antigo se o processo ainda cita esse path.
7. **Atualizar** 1 linha no HANDOFF / MEMORY se o hot path mudou.
8. **Lint** em todo `.md` Soft novo:  
   `python3 /home/cloud/.claude/skills/soft-conteudo-headlines/scripts/lint_copy.py <arquivo>` (exit 0).

## Proibições

- `rm -rf` em massa; hard delete só tmp/log/duplicata confirmada + OK do Léo
- Misturar engines: Soft Soft CRS ≠ out-v5 ≠ banners-army ≠ KEEP ads
- Editar dentro de zip de download (zip ≠ mesa de edição)
- Arquivar sem flag: `renders/CRS-*` do lote enxuto ativo, PNG KEEP em `ads/`, skills, `.cjs` engines, docs-mãe/réguas/HANDOFF
- Mover path que quebra site no ar sem stub + candidatura

## Reverter um `mv`

```bash
# Ler MANIFEST da quarentena, depois:
mv /root/_ARQUIVO/AAAA-MM-DD-motivo/<sub>/<pasta> <path-origem-listado>
```

Sem inventar destino. Se não está no MANIFEST, deixa na quarentena.

## Entrega

Um doc MD curto (ou atualização do README da quarentena) com: o que manteve, o que arquivou, o que não tocou, comando de revert de 1 pasta. Paths absolutos.


---

## RÉGUA DE DIAGRAMAÇÃO obrigatória (18/07/2026)

Todo doc/entregável que essa skill produz DEVE seguir `/home/cloud/.openclaw/brain/REGUA-DIAGRAMACAO-DOCS.md`:

- Topo: rótulo pequeno + título grande + subtítulo + metadata `chave: valor`
- Números ANTES da narrativa (seção "0" com tabela/KPI ancora tudo)
- Numeração hierárquica (1, 2, 3.1, 3.2), divisa entre seções
- Bloco padronizado que se repete em TODAS as seções
- Bullet > parágrafo, com palavra-âncora em **negrito**
- Callouts (azul/verde/amarelo/vermelho) 1 por seção no máximo
- Comparação = 2 colunas paralelas · Fluxo = seta ↓ · KPI = cards
- Aspas literais pra citação · badges pra marcar novidade
- Fecha com checklist acionável (dono/prazo quando existe)
- Zero gordura, zero changelog, zero meta-processo
- 1 bloco = 1 tela de celular
