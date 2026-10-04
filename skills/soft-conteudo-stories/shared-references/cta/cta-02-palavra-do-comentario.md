# A palavra do comentário: de onde vem, onde fica gravada e como conferir

A palavra do comentário é a que a pessoa digita pra receber alguma coisa no direct, como em "comenta <a palavra> que eu te mando <o material>". Quem responde é a automação do dono: uma regra, numa ferramenta de automação, que lê os comentários e manda a mensagem. Palavra sem automação ligada deixa a pessoa esperando uma mensagem que nunca chega, e palavra com uma letra diferente da regra também.

## Condição de entrada

Vale pra todo CTA com palavra, com direct ou com número. Antes de escrever, procure os 6 dados abaixo no perfil e nos insumos do dono. Cada dado que falta vira a pergunta da última coluna, feita ao dono uma por vez e nesta ordem, dizendo em qual delas ele está e esperando a resposta antes da seguinte. **Sem o dado, o CTA sai sem palavra e sem número**, e a pergunta fica no fim da entrega. Antes de todas vem a do objetivo, porque a peça pede uma ação só e é essa resposta que escolhe o tipo de CTA: "O que você quer que a pessoa faça no fim desta peça: salvar, te seguir, comentar uma palavra ou te chamar no direct?"

| Dado | Onde está | Pergunta quando falta, e por quê |
|---|---|---|
| 1. A palavra | na linha de automação do perfil, letra por letra | "Qual palavra a sua automação de comentário responde hoje, escrita do jeito que a pessoa vai digitar?" Quem digita diferente da regra fica sem resposta. |
| 2. Onde ela está registrada | na regra, dentro da ferramenta de automação | "Em qual ferramenta está a regra que responde essa palavra?" Se ele não sabe: abra a ferramenta e copie a palavra da regra. Sem regra, o fim da entrega traz o passo pra ligar uma. |
| 3. Se a automação responde | na linha do perfil, marcada "ligada" | "Essa automação está ligada? Comente a palavra de outra conta e me diga se a mensagem chegou." Palavra desligada sai do CTA. |
| 4. O que a pessoa recebe | na mensagem que a regra manda | "O que a mensagem manda pra quem comenta?" O CTA conta esse ganho, com as palavras da mensagem. |
| 5. A isca | no arquivo do material, pronto, na pasta do dono | "O material que a mensagem entrega já está pronto? Me mande o arquivo." Material que ainda não existe fica fora da promessa. |
| 6. O número | contado no arquivo da isca ou no insumo, com o rótulo dele | "Quantas páginas, itens ou minutos tem o material? Se me mandar o arquivo, eu conto." Número sem origem é invenção. |

## A regra

1. **A palavra vem do dono, nunca da skill.** Escolher, trocar por uma mais bonita ou sugerir dentro da peça é inventar.
2. **Uma palavra principal por perfil**, gravada no perfil do dono. Ela vale em todas as peças, de todos os formatos.
3. **Palavra de material** (uma isca, uma sequência de stories, uma campanha) só entra quando existe uma automação própria pra ela, registrada no perfil numa linha só dela. Sem essa linha, a peça usa a palavra principal.
4. **Sem origem, o CTA sai sem palavra:** na versão de direct ("me chama no direct que eu te mando <o que a pessoa recebe>") ou com outro tipo de pedido. Até 3 sugestões de palavra podem ir pra seção de perguntas do relato, em letra minúscula e como pergunta ao dono; na peça, nunca.
5. **A grafia é a da regra da ferramenta, letra por letra.** "<A PALAVRA>", "<A PALAVRA> <número>" e "<A PALAVRA><número>", colado, são três palavras diferentes pra quem digita e pra automação.
6. **Palavra que só aparece em legenda antiga, sem linha no perfil, fica fora**, mesmo que já tenha funcionado um dia. A pergunta "ela volta?" vai pro fim da entrega.
7. **Todo CTA com palavra, ou com direct, diz o que a pessoa recebe**, com o número contado no arquivo do material (dado 6): quantas páginas, quantos itens, quanto tempo. Sem o arquivo, o CTA diz o que ela recebe e fica sem número.

## A linha do perfil

A resposta vai pro perfil do dono, na pasta de trabalho dele e nunca dentro da pasta da skill, uma linha por palavra:

```
- Automação de comentário: palavra <A PALAVRA> (principal do perfil) responde com <o que a pessoa recebe> · regra na ferramenta <nome da ferramenta> · ligada · confirmado pelo dono em <data>
- Automação de comentário: palavra <A PALAVRA> (do material <qual>) responde com <o que a pessoa recebe> · regra na ferramenta <nome da ferramenta> · ligada · confirmado pelo dono em <data>
- Automação de comentário: nenhuma, o CTA sai sem palavra · confirmado pelo dono em <data>
```

Automação desligada continua na linha, com "desligada" no lugar de "ligada", e a palavra dela sai de todo CTA até o dono ligar de novo. Essa linha é a origem da palavra: sem ela, nenhuma skill põe a palavra num CTA.

## Como conferir antes de entregar

1. **Procure a palavra nos insumos do dono** com a mesma busca que o gate usa: `grep -rn -iE 'manda |comenta |envia |digita |palavra |chama ' <pasta de insumos do dono>`. Cole a saída.
2. **Rode o gate da skill:** `python3 scripts/checar_titulos.py --peca <arquivos da peça> --insumos <pasta de insumos do dono> --perfil <perfil do dono>`. Ele reprova com `palavra-chave inventada: <X>` quando a palavra da peça não está nos insumos.
3. **Confira a linha do perfil com os olhos.** O script vê se o perfil fala de automação, mas não liga a palavra à automação dela nem lê se ela está ligada; até uma linha "nenhuma" conta como automação declarada pra ele. A palavra da peça tem que ter a linha dela, com "ligada".
4. **Feche com a linha de conferência**, no relato ou em `conferencia/`, nunca na peça: `palavra-chave: <A PALAVRA> | origem: <arquivo:linha> | recebe: <o que a pessoa recebe>`, ou `palavra-chave: nenhuma (CTA sem palavra)`.

## Sem palavra, o que sai

- **Na peça:** a versão de direct, com o que a pessoa recebe e a cena de depois: "Me chama no direct que eu te mando <o material>, pra <como fica depois>." O número do material entra só com origem (dado 6).
- **No fim da entrega, pro dono:** "Quando ligar uma automação de comentário, me diga a palavra e o que ela manda: ela entra no seu perfil e passa a valer em todas as peças."
