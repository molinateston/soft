# Auditoria pré-preview

Checklist obrigatório que roda **depois** de gerar o HTML e **antes** de mostrar o preview ao usuário. Se qualquer item falhar em qualquer slide, corrija antes de apresentar. Não mostre slide que falhou na auditoria.

## Protocolo

Para **cada slide** do carrossel, responda 12 perguntas. Resposta esperada: SIM em todas. Qualquer NÃO aciona correção.

### As 12 perguntas

1. **Fundo chapado?**, background é cor sólida única (`#0A0908`, `#F5F2EC`, `#FFFFFF`, ou o que a família define). Sem gradiente, sem textura forte, sem imagem de fundo (exceto se o usuário forneceu imagem explicitamente).

2. **Uma cor de accent apenas?**, existe no máximo UMA cor de destaque no slide, e ela aparece em no máximo 4 palavras-chave. Preto/branco e seus tons não contam como accent.

3. **Padding 100px simétrico nos 4 lados?**, top, right, bottom, left todos em 100px. Sem exceção. Inclusive no layout utilitário.

4. **Simetria total no eixo do slide?**, `justify-content: center` vertical + `align-items: center` horizontal no `.slide`. Conteúdo em container interno `text-align: left` ou `center`. Nenhum `position: absolute` em elemento de conteúdo **exceto**: (a) setinha de arraste, (b) layout diagrama manuscrito (nós e setas).

5. **Hierarquia de 2 níveis no máximo?**, título + corpo. Se tiver subtítulo, é exceção rara e deve ser justificável (ex: kicker acima do título principal). Três níveis paralelos = falha.

6. **Negrito em 2–4 palavras apenas?**, dentro do corpo, negrito aparece em 2 a 4 palavras-chave. Negrito em frase inteira ou parágrafo inteiro = falha. Negrito mínimo 700.

7. **Sem sombra, sem ícone colorido, sem canto arredondado no slide?**, zero `text-shadow`, zero `box-shadow` em conteúdo (exceção: screenshots-nó no layout diagrama manuscrito). Zero ícone Material/Font Awesome colorido (só line-art mono permitido). Slide é retângulo sólido sem `border-radius`.

8. **Escala tipográfica bate com `escala-densidade.md`?**, conte as palavras do título e do corpo e confira se o `font-size` aplicado está dentro da faixa da tabela. Slide com título de 3 palavras em 60px falha aqui. Slide com título de 18 palavras em 140px falha aqui.

9. **Seta grande + handle presentes?** Slides de 1 a N-1 têm seta SVG variação C centralizada no rodapé (bottom 80px) + `@handle` centralizado acima (bottom 140px). Slide 1 tem o handle também no topo do bloco de conteúdo, acima do título. Último slide (CTA): sem seta, sem handle no rodapé. A setinha `›` no canto inferior direito está **deprecated**, se aparecer em qualquer slide, é falha.

10. **Zero widows, verificação linha a linha obrigatória?**

    Para **cada bloco de texto com `<br>` explícito** no slide (título e corpo), execute este protocolo antes de aprovar:

    **Passo 1, Liste todas as linhas do bloco:**
    Separe o texto nos `<br>` e liste cada linha individualmente.

    **Passo 2, Cheque a última linha:**
    - Tem 1 palavra só? → **FALHA**
    - Tem 2 palavras mas soma < 8 caracteres (ex: "é só", "no a")? → **FALHA**
    - Tem ≥ 2 palavras E soma ≥ 8 caracteres? → passa

    **Passo 3, Corrija se falhou:**
    Mova 1 palavra da linha anterior para a última, ou puxe a palavra solitária para a linha anterior. Escolha a quebra que respeita a unidade semântica (phrase ragging).

    **Exemplos de falha e correção:**

    | Errado | Correto |
    |---|---|
    | `É a decisão<br>por trás<br>dele.` | `É a decisão<br>por trás dele.` |
    | `Rentabilidade alta<br>sem<br>transparência` | `Rentabilidade alta<br>sem transparência` |
    | `Consciência<br>financeira<br>não é saber<br>investir.` | `Consciência financeira<br>não é saber<br>onde investir.` |

    **Esta verificação é obrigatória em TODOS os slides, em TODOS os blocos com quebra explícita.** Não é opcional. Não é "quando der". É pré-condição para mostrar qualquer preview.

11. **Phrase ragging respeitado?**, cada quebra de linha está entre pedaços semânticos, nunca no meio de um pedaço. Teste: leia cada linha isoladamente, faz sentido? Se soa "cortada no meio", falha. Exceção: corpo muito longo (>40 palavras) pode quebrar por largura do container em vez de phrase ragging.

12. **Termos compostos inteiros?**, nenhuma marca ("WhatsApp", "ChatGPT", "Instagram"), valor monetário ("R$3k"), unidade numérica ("3 msgs", "48h"), ou nome próprio composto ("Soft Business") está quebrado entre linhas. Checar se estão em `<span style="white-space:nowrap">` ou se a quebra manual respeita o termo.

## Teste final, "0,3 segundos"

Depois das 12 perguntas, faça o teste subjetivo:

> Se alguém vê este slide por 0,3 segundo no feed, a mensagem principal chega?

Se a resposta é "talvez", falha. Se é "não", falha. Só SIM passa.

Critérios do teste:
- Título é legível em escala 1080×1350 reduzida a thumbnail (imagine 400×500 no explorar)?
- Hierarquia visual guia o olho direto pra mensagem principal?
- Há contraste suficiente pra destacar do feed colorido ao redor?

## Protocolo de correção

Se um slide falhar em qualquer item:

1. **Identifique qual item falhou**, não vale correção genérica.
2. **Edite apenas aquele slide** com `str_replace`, não regenere o carrossel inteiro.
3. **Rode a auditoria de novo no slide corrigido** antes de mostrar.
4. **Não reporte a auditoria ao usuário**, ela é interna. Mostre só o preview final já auditado.

## O que esta auditoria NÃO é

- **Não é julgamento de copy**. Se o slide está chato porque a copy é chata, isso é problema da skill de copy, não desta.
- **Não é validação de mérito criativo**. Ela só checa se as regras duras foram respeitadas.
- **Não substitui a aprovação do usuário**. Depois que passar na auditoria, ainda assim mostre preview e peça ajuste.
- **Não roda durante a correção pós-preview**. Se o usuário pediu ajuste específico no slide 3 depois do preview, edite o que ele pediu, não re-audite o carrossel inteiro.
