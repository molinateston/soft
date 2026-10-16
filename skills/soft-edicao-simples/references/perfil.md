# O perfil do dono (perfil.json)

Lido no passo 1 do fluxo do `SKILL.md`. O `perfil.json` mora na raiz da pasta de trabalho e vale para todos os vídeos do dono. É o mesmo esquema das outras skills de edição da casa: quem já tem o arquivo não precisa responder de novo. Antes do primeiro vídeo, procure o arquivo. Se não existir, pergunte UMA vez, numa mensagem só, e salve.

## Esquema

```json
{
  "nome": "Nome que aparece no perfil",
  "usuario": "arroba_sem_o_arroba",
  "nicho": "Ex.: confeitaria artesanal",
  "seguidores": "Ex.: 12,4 mil (como aparece no aplicativo)",
  "avatar": "fotos/avatar.jpg",
  "logo": "",
  "cor_acento": "#RRGGBB",
  "fonte_titulo": "fontes/minha-fonte-black.ttf",
  "pasta_prints": "prints"
}
```

| Campo | Onde aparece neste estilo | Se faltar |
|---|---|---|
| `cor_acento` | A palavra de destaque da headline e a palavra falada da legenda | Tudo branco, sem destaque de cor |
| `fonte_titulo` | A headline da abertura e o CTA | Inter Black na headline e Inter Bold no CTA, livres (OFL 1.1), que vêm com a skill |
| `nome`, `usuario`, `nicho`, `seguidores`, `avatar` | Não aparecem: este estilo não desenha tela de perfil | Nada |
| `logo` | Não usa logo; entra só se o dono pedir, pequeno | Nada |
| `pasta_prints` | Não usa prints; a imagem da abertura e os apoios vêm de outra fonte (veja o SKILL.md) | Nada |

A legenda tem fonte fixa de código (JetBrains Mono, livre), porque ela é a assinatura do estilo. O dono que quiser outra fonte na legenda está pedindo outro estilo; anote no relatório se mudar.

## Regras

- Caminhos podem ser relativos à pasta de trabalho (recomendado) ou completos. No Windows, use barra normal (`fontes/minha.ttf`) ou barra dupla dentro do JSON.
- `fonte_titulo` só com fonte que o dono tem direito de usar em vídeo (comprou a licença ou é livre). Prefira um peso bem grosso (Black ou ExtraBold): a headline é lida em menos de 5 s. Na dúvida, fique com a livre padrão e anote no relatório.
- A cor vai em `#RRGGBB`. Outro formato é ignorado e o vídeo sai sem acento, com aviso.
- O `novo-reel.mjs` copia a identidade para o `reel.json` de cada projeto. Mudou o perfil depois? Ajuste o `reel.json` do projeto aberto ou crie o projeto de novo.
- Nunca invente número, logo, capa nem imagem de caso real. Se faltar algo, peça ao dono.

## Como perguntar (modo guiado ou primeira vez)

"Pra deixar o vídeo com a sua cara eu preciso de 2 coisas, uma vez só: a cor da sua marca (o código, tipo #1E88E5, ou me diga a cor e eu te ajudo a achar) e a fonte que você usa nos títulos (o arquivo, se tiver; se não, uso uma livre bem grossa). Pode pular as duas: sem cor, o vídeo sai todo em branco."
