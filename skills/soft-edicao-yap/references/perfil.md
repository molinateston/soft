# O perfil do dono (perfil.json)

Lido no passo 1 do fluxo do `SKILL.md`. O `perfil.json` mora na raiz da pasta de trabalho e vale para todos os vídeos do dono. Antes do primeiro vídeo, procure o arquivo. Se não existir, pergunte UMA vez, numa mensagem só, e salve. Depois disso, só pergunte de novo se o dono pedir para trocar algo.

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
  "fonte_titulo": "fontes/minha-fonte-bold.ttf",
  "pasta_prints": "prints"
}
```

| Campo | Onde aparece | Se faltar |
|---|---|---|
| `nome`, `usuario`, `nicho`, `seguidores`, `avatar` | Só numa imitação de tela, quando não existe print e o dono pediu uma | A skill pede o print exato em vez de desenhar |
| `logo` | Este estilo não usa logo (edição de celular não tem marca d'água); entra só se o dono pedir, pequeno | Nada |
| `cor_acento` | A palavra de destaque ocasional (`.y`) | Tudo branco, sem cor de acento |
| `fonte_titulo` | Títulos, textos acima da cabeça e legenda | DM Serif Display, livre (OFL 1.1), que vem com a skill |
| `pasta_prints` | Onde o `indexar-prints.mjs` procura os prints | A skill pergunta a pasta, ou o dono manda os prints direto |

## Regras

- Caminhos podem ser relativos à pasta de trabalho (recomendado) ou completos. Vale em qualquer sistema: no Windows, use barra normal (`fotos/avatar.jpg`) ou barra dupla dentro do JSON.
- `fonte_titulo` só com fonte que o dono tem direito de usar em vídeo (comprou a licença ou é livre). Na dúvida, fique com a fonte livre padrão e anote no relatório.
- A cor vai em `#RRGGBB`. Outro formato é ignorado e o vídeo sai sem acento, com aviso.
- O `novo-reel.mjs` copia a identidade para o `reel.json` de cada projeto. Mudou o perfil depois? Ajuste o `reel.json` do projeto aberto ou crie o projeto de novo.
- Nunca invente número, logo, capa nem print. Se faltar algo, peça ao dono a tela exata.

## Como perguntar (modo guiado ou primeira vez)

"Pra deixar o vídeo com a sua cara eu preciso de 4 coisas, uma vez só: a cor da sua marca (o código, tipo #1E88E5, ou me diga a cor e eu te ajudo a achar), a fonte que você usa nos títulos (o arquivo, se tiver; se não, uso uma livre parecida), a pasta onde ficam seus prints do celular, e o seu @ com o número de seguidores como aparece hoje. Pode pular qualquer uma: sem cor, o vídeo sai todo em branco."
