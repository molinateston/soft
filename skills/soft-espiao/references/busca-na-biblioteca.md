# Busca na biblioteca: termos, coleta e caminho manual

Lida no passo R1 e R2 da Ação 1, e no passo 1 da Ação 2.

## 1. Como montar o termo

A biblioteca de anúncios da Meta transcreve o áudio de cada anúncio pra revisar, e a busca por palavra acha o que foi DITO no vídeo, em qualquer ordem e posição. Isso acha o anúncio que o concorrente escondeu no título.

Monte cada busca com 2 palavras soltas, sem aspas e sem operador, tiradas de 3 famílias:

| Família | O que é | Exemplos neutros |
|---|---|---|
| Mercado | termo que aparece em quase todo anúncio de resposta direta | causa, erro, método, truque, revela, descobriu, passo |
| Nicho | o tema do dono | violão, confeitaria, joelho, inglês |
| Oferta | o nome do gancho ou do mecanismo de um concorrente que já vende | o apelido que ele dá ao método, o nome do desafio |

Combinações que rendem: mercado + nicho (`erro violao`), oferta + nicho, mercado + oferta. Cada palavra a mais deixa a busca pior, porque a transcrição exige todas: 3 palavras só com motivo escrito.

Tire as palavras da própria VSL ou do anúncio do concorrente, nunca de termo genérico de marketing. A melhor fonte de palavra de nicho é a frase que o cliente do dono usa pra descrever o problema.

## 2. Coleta com shell (script)

O script chama o coletor público da biblioteca pelo Apify. O `APIFY_TOKEN` já vem do ambiente do agente (carregado do arquivo de credenciais); nunca escreva o valor no comando nem no chat, e nunca peça o token ao dono no chat. Confira sem imprimir: `test -n "$APIFY_TOKEN" && echo token: ok || echo token: ausente`. Com `ok`, rode os comandos abaixo; com `ausente`, siga o caminho manual (seção 3).

```
python3 scripts/buscar_anuncios.py --termo "erro violao" --termo "metodo violao" --max 20 --saida planilha-violao.csv
python3 scripts/buscar_anuncios.py --pagina-id 1234567890 --saida planilha-violao.csv --acrescentar
python3 scripts/buscar_anuncios.py --recalcular planilha-violao.csv
python3 scripts/buscar_anuncios.py --modelo planilha-violao.csv
```

- `--max` é por termo. 20 por termo costuma bastar; cada 10 anúncios custam uns 5 a 9 centavos de dólar no coletor, e o script para acima de 50 por termo ou 150 itens por chamada. `--pagina-id` traz até `--max` anúncios ativos da página (padrão 20).
- `--salvar-bruto bruto.json` guarda a resposta inteira pra reler depois com `--de-json`, sem gastar crédito.
- Códigos de saída: 0 ok · 2 sem token · 3 erro na chamada · 4 nada encontrado · 5 erro de uso.
- A coleta demora de 30 segundos a 3 minutos. Em ambiente com limite de tempo por comando, rode um termo por vez.
- O script agrupa as cópias do mesmo anúncio pelo grupo que a própria biblioteca informa (a coluna `copias`) e conta, dentro da coleta, quantas páginas usam o mesmo texto e quantas versões cada página roda.

## 3. Coleta sem shell ou sem token (caminho manual)

1. O dono abre `facebook.com/ads/library`, escolhe o país, "Todos os anúncios", e digita o termo que a skill escreveu.
2. Pra cada anúncio que parecer do eixo, ele copia o link (botão "Ver detalhes do anúncio") e manda um print que mostre: o nome da página, "Veiculação iniciada em", e o aviso "N anúncios usam este criativo e texto", quando houver.
3. A skill preenche a planilha com as mesmas colunas do `--modelo` e aplica a régua de `sinais-de-venda.md` no olho.
4. Em página de concorrente, "Ver todos os anúncios" da página dá a contagem de versões.

## 4. Outras bibliotecas

- **Google e YouTube:** o Centro de Transparência de Anúncios do Google mostra tudo que um anunciante roda agora. Achou o anunciante por uma busca por transcrição ou pela Meta, cruze o nome dele lá.
- **Ferramentas pagas de espionagem** costumam mostrar o que rodou semanas atrás. Recência pesa: a biblioteca oficial mostra o que está no ar hoje.
- **Transcrição de vídeo do YouTube** pra engenharia reversa: com shell, um coletor de transcrição no mesmo Apify resolve; sem shell, o dono cola a transcrição que a própria plataforma mostra.

## 5. Ruído

A busca por palavra traz anúncio de assunto vizinho que usa a mesma palavra. Depois da coleta, leia a coluna `texto_inicio` e marque `fora do eixo: <motivo>` na `nota`. Linha marcada fica na planilha e não entra no Radar.
