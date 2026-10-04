# Roteiro parcial: um trecho da aula, sem a aula inteira

Vale quando o roteiro do dono é um trecho (por exemplo, só a abertura e o ensino, ou só a fase de ação sem o preço). O passo 7 do SKILL.md e o checklist "do deck inteiro" do guia supõem a aula toda; aqui está o que muda.

## O que fazer

1. **Diga a cobertura no começo do relato:** "Este deck cobre do slide X ao Y do roteiro; [oferta, bônus, recap] não vieram." O trecho não ganha slide de oferta, bônus, prazo nem recap inventado: tudo que o roteiro não traz fica como está nas regras de "O que nunca entra".
2. **Perguntas ao dono:** só as que o trecho usa e ficaram sem resposta (com dono ou sem ele; sem dono, não espere: registre em "Falta você responder" e siga com o padrão). Sem bônus no trecho, pule a 3; sem preço, a 4 (com preço, a de prazo e link vale); sem resultado afirmado, a 2. Cores, fonte e logo (5) valem sempre. O critério já vale no passo 0 de `perguntas-ao-dono.md`.
3. **Passo 7 (olhar o deck):** uma regra só, pelo que o trecho tem. Com oferta completa (tabela que soma): a abertura do trecho, uma escada ou lista, a oferta e o slide mais cheio. Sem tabela (nem preço, ou só um pedaço dele): os 4 slides mais densos, o do preço entre eles se houver. Densidade é a maior contagem de palavras na tela (conte a linha "Tela:" de cada slide no `notas.md`; o `checar_deck.py` só reprova acima do teto, não imprime a contagem), com desempate pelo maior número de elementos (blocos, formas e números), depois pelo maior número de cliques e, ainda empatado, pelo slide de menor número (história curta, com 6 a 12 palavras por tela, empata sempre: use o desempate, sem tentar contar de novo); a abertura e o último entram só se estiverem nesse grupo. O último slide não ganha lugar fixo: o mosaico já o mostra.
4. **Fundo por bloco:** a alternância de fundo claro e escuro vale por fase. Trecho de uma fase só (um `## Fase A` único) é um bloco só: o deck inteiro com o mesmo fundo, em geral escuro, é o resultado esperado e nunca conta como defeito. Declare numa linha no `_operador.md`, na seção "Decisões de desenho" que o esqueleto já abre ("um bloco, fundo escuro em todos") e deixe a variação por conta da composição (item 3 do checklist abaixo). Com duas fases ou mais no trecho, o fundo troca por fase como no deck inteiro.

## Checklist do deck inteiro, versão trecho

| item do guia (seção 8, "Do deck inteiro") | no trecho |
|---|---|
| 1. esquema principal 3 vezes e a decisão antes do pitch | só as voltas que o trecho cobre; declare quais faltam |
| 2. abertura com as palavras do público | só se o trecho abre a aula |
| 3. layout varia | vale |
| 4. oferta é o único slide denso | sem tabela: vale pro slide do preço, que não pode ficar atrás de outro em palavras; sem preço, não se aplica. Este item se confere a olho e se registra no relato (contagem de cada slide e a posição do preço); nenhum script o mede. Se o roteiro só dá duas linhas curtas de preço, diga "preço atrás em palavras, o roteiro não traz mais" e não encha a tela |
| 5. slide parado mais de 10 s | vale |
| 6. peça do produto antes da ponte | vale: nenhum nome de produto antes da ponte do trecho |
| 7. bônus com logo, resultado e tarja | não se aplica sem bônus |
| 8. percentual ao lado do número e total parcelado fora | só se há percentual ou parcela |
| 9. soma da tabela confere | só se há tabela; com preço e sem tabela, confira que o total parcelado não aparece e que o à vista fica menor que a parcela manchete, e que cada valor da tela está no roteiro (`conferir_fontes.py`) |
| 10. deck bate com página e checkout | sem preço, não se aplica; com preço e sem página nem checkout, não dá pra verificar: diga no relato "preço não conferido com o checkout" e ponha a pergunta na lista |

## Como declarar

No relato, em "Conferência", uma linha: "Roteiro parcial (slides X a Y). Não se aplicam: itens 4, 7, 9 e 10 do checklist do deck inteiro; 1 só nas voltas [quais]." Trecho com preço e sem tabela: os itens 4, 9 e 10 entram na linha com o que valeu, como na tabela acima. O que não se aplica não é falha, mas tem de estar dito.
