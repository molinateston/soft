# O perfil do dono (perfil.json)

Lido no passo 1 do fluxo do `SKILL.md`. O `perfil.json` mora na raiz da pasta de trabalho e vale para todos os vídeos do dono. É o mesmo arquivo das outras skills de edição da casa (Yap, Yap 2, Simples): quem já tem um, usa o mesmo. Antes do primeiro vídeo, procure o arquivo. Se não existir, pergunte UMA vez, numa mensagem só, e salve. Depois disso, só pergunte de novo se o dono pedir para trocar algo.

## Esquema

```json
{
  "nome": "Nome que aparece no perfil",
  "usuario": "arroba_sem_o_arroba",
  "nicho": "Ex.: confeitaria artesanal",
  "seguidores": "",
  "avatar": "",
  "logo": "",
  "cor_acento": "#RRGGBB",
  "fonte_titulo": "fontes/minha-fonte-pesada.otf",
  "fonte_legenda": "fontes/minha-fonte-mono.ttf",
  "pasta_prints": ""
}
```

| Campo | Onde aparece neste estilo | Se faltar |
|---|---|---|
| `cor_acento` | A palavra falada na legenda, o objeto em ação de cada cena (play, barra, anel, mascote, degrau de destino) e a palavra marcada com `*asteriscos*` | Tudo branco, sem cor de acento |
| `fonte_titulo` | Palavras grandes, títulos das cenas, cartões e a headline da abertura | Inter Black, livre (OFL 1.1), que vem com a skill |
| `fonte_legenda` | A legenda (campo opcional, só deste estilo; as outras skills ignoram) | JetBrains Mono Bold, livre (OFL 1.1), que vem com a skill |
| `nome`, `usuario`, `nicho` | Não aparecem no vídeo. Servem para a skill falar com o dono pelo nome | Nada |
| `seguidores`, `avatar`, `pasta_prints` | Não são usados neste estilo (as cenas são ilustrações desenhadas, nunca print nem perfil) | Nada |
| `logo` | Este estilo não usa logo; entra só se o dono pedir, pequeno, numa cena | Nada |

## Regras

- Caminhos podem ser relativos à pasta de trabalho (recomendado) ou completos. No Windows, use barra normal (`fontes/titulo.otf`) ou barra dupla dentro do JSON.
- Fonte só se o dono tem direito de usar em vídeo (comprou a licença ou é livre). Na dúvida, fique com a livre padrão e anote no relatório.
- Fonte de título pesada (Black ou Extra Bold) segura as palavras grandes. Fonte fina some no fundo preto: avise o dono se ele declarar uma.
- Legenda fica melhor em fonte mono ou de largura regular, em negrito. Fonte de enfeite ou cursiva não serve para legenda.
- A cor vai em `#RRGGBB`. Outro formato é ignorado e o vídeo sai sem acento, com aviso. Cor escura demais (perto do preto) some no fundo dos takeovers: sugira um tom mais claro.
- O `novo-reel.mjs` copia a identidade para o `reel.json` de cada projeto. Mudou o perfil depois? Ajuste o `reel.json` do projeto aberto ou crie o projeto de novo.
- Nunca invente número, logo, print nem resultado. As cenas são desenhos de ideia, e o relatório diz isso.

## Como perguntar (modo guiado ou primeira vez)

"Pra deixar o vídeo com a sua cara eu preciso de 3 coisas, uma vez só: a cor da sua marca (o código, tipo #1E88E5, ou me diga a cor e eu te ajudo a achar), a fonte que você usa nos títulos (o arquivo, se tiver; se não, uso uma livre e pesada), e se quiser outra fonte pra legenda. Pode pular qualquer uma: sem cor, o vídeo sai todo em branco."
