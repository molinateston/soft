# Verificador de lastro: o segundo par de olhos, cego à peça

> Último passo do Crítico. Bloqueante. Roda DEPOIS que a peça está escrita e ANTES de dizer pronto. A simulação de pele (`02-simulacao-cliente.md`) sente a peça como o cliente; o gate CUB (`03-gate-cub.md`) reprova o que não tem força. Este passo faz a última pergunta que sobra: cada afirmação da peça tem chão no insumo do dono, ou foi inventada pra soar bem? A ancoragem já vive dentro do gate como uma passada de auto-avaliação. O problema provado no teste: sob pressão de entregar, o mesmo modelo que escreveu a peça se autoaprova e deixa passar invenção. A cura é separar os papéis: aqui o modelo para de ser autor e vira VERIFICADOR.

## O que é

Depois da peça pronta, o agente abre um SEGUNDO raciocínio e assume o papel de verificador em vez do papel de autor. O verificador não confia no que o autor alegou ter ancorado. Ele pega cada afirmação factual da peça e confere na fonte, uma por uma. É cego à peça no sentido que importa: não herda a boa-vontade de quem escreveu, não aceita "isso eu tirei do brain" sem apontar onde. A régua é uma só: ou a afirmação tem uma linha do insumo que a sustenta, ou ela sai.

No teste real este passo achou e consertou 14 afirmações sem lastro numa peça e 5 em outra, e o eixo de zero-inventado subiu pra 9. O que ele acha, o autor não achava, porque o autor lê a peça torcendo pra ela estar certa.

## O método do verificador

Lista TODA afirmação factual da peça pública. Não a impressão geral, cada afirmação:

- toda aspa atribuída a uma pessoa (fala de cliente, de aluno, do dono);
- todo número (faturamento, prazo, quantidade, percentual, preço, N de casos);
- toda história, biografia ou cena (a jornada do dono, o "dia em que entendi", o caso do cliente com nome trocado);
- todo fato do produto (o que inclui, preço, prazo, frequência, formato, o que dispensa);
- toda promessa (o resultado prometido, o "em X dias", a garantia).

Pra cada afirmação, aponta a linha do insumo que a sustenta, na forma `arquivo:trecho literal`, OU marca `SEM LASTRO`. O trecho literal sai da leitura da fonte visível na tela, jamais de "confere de cabeça". Fonte = o insumo real do dono: perfil (`00-perfil-do-usuario.md`), brain, o que o dono colou nesta sessão, os arquivos de VoC. Não os exemplos embutidos na skill, que são de outro dono e ensinam COMO escrever, nunca são matéria-prima do QUE a peça afirma.

## A regra de conserto

Afirmação `SEM LASTRO` NÃO vira `[A CONFIRMAR]` na peça pública. `[A CONFIRMAR]` e qualquer placeholder moram no bastidor (o relato, o dossiê, a tabela deste passo), nunca dentro do que o leitor lê. A afirmação sem lastro SAI da peça, ou vira só o que o insumo sustenta.

O verificador CONSERTA a peça, não só aponta. E conserta sem inventar pra preencher: se o insumo não sustenta a promessa de "42 dias", a peça não diz "algumas semanas" pra salvar a frase, ela diz o que é verdade ou não diz nada naquele ponto. Se falta lastro, a peça diz MENOS, com honestidade. Peça mais curta e ancorada ganha da peça cheia e inventada, porque a invenção morre na primeira pergunta do leitor cético.

## Os alvos que mais escapam (checklist do teste real)

Confira um por um, porque foram estes que passaram pela auto-avaliação e só caíram no segundo par de olhos:

- **(a) verbatim adulterado.** A aspa é a fala real do dono ou do cliente MAIS palavras a mais que ninguém disse. "isso serve pra mim?" virou "isso serve pra mim, mesmo com o joelho ruim?". A cauda "mesmo com o joelho ruim" é invenção colada numa fala verdadeira. A aspa volta a ser o que a pessoa disse, caractere a caractere, ou vira paráfrase fora das aspas.
- **(b) biografia inventada do dono.** Jornada, origem, "eu já fui assim", confissão, sem nenhuma linha do insumo que a sustente. História plausível não é história ancorada. Sem lastro, sai.
- **(c) cena ou detalhe inventado colado num caso real.** O caso existe no insumo, mas a peça acrescentou a cena (a hora, o lugar, a frase que a pessoa teria pensado) que o insumo não traz. O caso fica, o detalhe inventado sai.
- **(d) fato de produto que o insumo não diz.** "sem equipamento", "sem carga", "toda semana", "acesso vitalício": cada um é um fato que ou está no insumo do produto ou não entra. O que o insumo não afirma, a peça não afirma.
- **(e) contradição interna.** O mesmo dado aparece com dois valores na peça (o preço num slide e outro no CTA, o prazo de 30 dias no meio e 45 no fim). Um dos dois está errado; os dois batem no insumo ou a peça não sai.
- **(f) bastidor vazando na copy pública.** Jargão do método, nome de arquivo, "conforme o mecanismo X", citação de insumo, marca de pendência: nada disso é texto pro leitor. Bastidor fica no bastidor.
- **(g) número por extenso que devia ser `[A CONFIRMAR]`.** O grep do lint pega dígito, não pega "quarenta e dois dias" nem "dobrou". Número escrito por extenso escapa da varredura automática e é o que mais sobrevive sem lastro. O verificador lê os números por extenso à mão e cobra a mesma fonte que cobraria de um dígito.

## O fecho

O verificador só libera a peça quando TODA afirmação tem lastro OU foi removida. Ele cola no bastidor a tabela, uma linha por afirmação:

`afirmação | lastro (arquivo:trecho) ou REMOVIDA`

Sem essa tabela preenchida, a peça não está pronta. A tabela não vai pra saída do dono; ela vive no relato, no dossiê, no arquivo de conferência, ao lado das outras tabelas do gate. "Conferi tudo" sem a tabela não conta como verificação feita, é a mesma auto-aprovação que este passo existe pra impedir.

## Segunda passada do verificador: CONFORMIDADE

Lastro responde "o que a peça afirma tem chão?". Sobra a outra metade, que a auto-aprovação também deixa passar: "a peça cumpre o que a própria skill exige dela?". O autor, sob pressão de entregar, alega que cumpriu (escreve no rodapé "equação de valor: ok") sem cumprir de fato, e se autoaprova. O verificador abre a segunda passada e confere a peça contra os requisitos DUROS da própria skill, item por item. Item não cumprido volta pra conserto, não vira entrega.

A régua é a mesma disciplina do lastro, virada pra dentro: o verificador não confia no que o autor alegou ter cumprido, ele mede. "Está lá" só conta com a evidência colada (o `wc -w`, a linha do elemento, a conta derivada). "O rodapé diz que está" não conta, é a mesma auto-aprovação que este passo existe pra impedir.

### De onde sai o checklist

O verificador NÃO inventa requisito. Ele lê o SKILL.md da própria skill e extrai só o que a skill declara como obrigatório: o que ela chama de `reprova`, `bloqueante`, `piso`, `teto`, `exige`, `obrigatório`, `sempre`, `nunca corta`. Cada skill tem os seus; o checklist é genérico na forma, específico no conteúdo de cada skill. O que a skill não declara como duro não entra na segunda passada (senão o verificador vira autor de regra nova).

### Os tipos de requisito duro que apareceram falhando

Confira cada um que a skill declarar, com a evidência colada, nunca a alegação:

- **piso/teto de tamanho.** A skill crava um mínimo ou máximo de tamanho (ex.: mini-VSL >= 800 palavras). Cola o `wc -w` da peça e compara com o piso. Abaixo do piso reprova; a alegação "tem mais de 800" sem o número contado não conta.
- **elemento obrigatório presente de fato.** A skill exige um elemento estrutural (ex.: a equação de valor no pitch, com os 4 fatores). O verificador confere se o elemento está LÁ, inteiro, com todas as partes que a skill pede, não se o rodapé ALEGA que está. Rodapé que alega sem o elemento cumprido reprova.
- **dado derivado quando o insumo permite.** Quando o insumo traz os componentes de uma conta, o número é DERIVADO com a conta colada, nunca deixado como `[A CONFIRMAR]` (ex.: meta de caixa quando o perfil tem pró-labore + custo + dívida: a meta é a soma, com a conta à vista). `[A CONFIRMAR]` num dado que o insumo permite calcular é preguiça, não pendência: reprova.
- **elemento marcado, não cortado.** Quando a skill manda MARCAR uma sugestão (ex.: a garantia entra como bloco sugerido pro dono decidir), cortar o bloco inteiro não cumpre a regra. Marcar ≠ cortar: o bloco ausente reprova.
- **seção obrigatória presente.** A skill exige uma seção nomeada no lugar certo (ex.: "Perguntas pra você" no fecho do relato). Seção ausente reprova, mesmo com o resto impecável.

### O fecho da segunda passada

O verificador só libera a peça quando, além de toda afirmação ter lastro, TODO requisito duro da skill está cumprido com a evidência colada. Ele cola no bastidor uma segunda tabela, uma linha por requisito:

`requisito duro (do SKILL.md) | cumprido? evidência (wc -w / linha / conta) ou NÃO CUMPRIDO`

Requisito `NÃO CUMPRIDO` volta pra conserto. Sem as DUAS tabelas preenchidas (lastro e conformidade), a peça não está pronta. Esta passada é do VERIFICADOR, o segundo par de olhos, não uma regra nova pro autor: é a conferência de que o que a skill já exige foi de fato cumprido, além de ancorado.

## Insumo pobre derruba mais afirmações (e isso é o certo)

O verificador roda com o insumo real do dono: brain, perfil, o que ele colou. Quando o insumo é rico, poucas afirmações caem. Quando o insumo é pobre, MAIS afirmações caem como sem-lastro, e a peça sai mais enxuta. Isso é o comportamento correto, não um defeito: com pouco material, dizer menos é honesto e dizer mais é inventar. Se a peça enxuta ficou fraca demais pra servir, o conserto é o dono trazer mais insumo, nunca o verificador afrouxar a régua pra encher a peça.
