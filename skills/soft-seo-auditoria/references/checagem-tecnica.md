# Checagem técnica: os 9 blocos

Cada bloco traz o que olhar, o que reprova e o conserto padrão. Sem acesso ao site, esta checagem vira
lista de verificação pro dono rodar, item por item, com tudo marcado como não verificado.

## 1. Velocidade de carregamento

**Olhe:** quanto tempo até a página mostrar alguma coisa útil.
**Causas mais comuns, nesta ordem:** imagem grande demais e sem compressão · script que bloqueia a
renderização · corrente de redirecionamento · fonte externa carregada antes do conteúdo.
**Conserto padrão:** comprimir e redimensionar imagem, carregar script de forma assíncrona, cortar
redirecionamento intermediário.

## 2. Comportamento no celular

**Olhe:** o texto cabe na tela sem rolar pro lado, o botão dá pra clicar com o polegar, a fonte é
legível sem zoom, a configuração de visualização existe.
**Conserto padrão:** ajustar a folha de estilo responsiva; botão com no mínimo o tamanho de um toque
confortável; nada de texto menor que o corpo padrão.

## 3. Dados estruturados

**Olhe:** a marcação que faz o resultado aparecer enriquecido. Os tipos que mais valem: perguntas
frequentes, passo a passo, produto, artigo, organização, trilha de navegação.
**Conserto padrão:** adicionar a marcação do tipo certo e validar pela ferramenta de teste do
buscador antes de publicar.

## 4. Rastreamento

**Olhe:** o arquivo que orienta o robô (não pode estar bloqueando o que deveria ser lido) · o mapa do
site (existe, está atualizado, aponta só pra página que deve ser indexada) · o endereço canônico (cada
página aponta pra versão certa dela mesma) · as marcas de não indexar e de não seguir (checar se
alguma está onde não deveria).
**Gravidade:** bloqueio indevido aqui é sempre **crítico**. É a falha que sozinha derruba um site
inteiro do resultado de busca.

## 5. Links quebrados e redirecionamento

**Olhe:** links internos e externos que devolvem erro · correntes de redirecionamento com mais de um
salto · links apontando pro endereço velho depois de uma reforma de site.
**Conserto padrão:** corrigir o destino no link, ou redirecionar em um salto só.

## 6. Conexão segura e conteúdo misto

**Olhe:** o site inteiro em conexão segura · nenhum recurso (imagem, script, folha de estilo) carregado
por conexão insegura dentro de página segura.
**Gravidade:** conexão insegura é **crítico**; conteúdo misto é **alto**.

## 7. Os três sinais de experiência de carregamento

**Olhe:** quanto tempo até o maior elemento aparecer · quanto tempo até a página responder ao primeiro
toque · quanto a página pula sozinha enquanto carrega.
**Conserto padrão do pulo:** reservar o espaço da imagem e do anúncio na folha de estilo, pra que o
conteúdo não desça quando eles carregam.

## 8. Indexação e conteúdo duplicado

**Olhe:** quantas páginas o buscador indexou contra quantas existem · páginas que deveriam estar
indexadas e não estão · o mesmo conteúdo servido em dois endereços (com e sem barra no fim, com e sem
prefixo de subdomínio, versão para impressão).
**Conserto padrão:** endereço canônico apontando pra versão única, e redirecionamento das variantes.

## 9. Declarações do cabeçalho da página (o bloco que passa despercebido)

**Olhe, linha por linha, no `<head>` de cada página auditada:**
- **`<meta charset>`**: existe e declara a codificação (o normal é `utf-8`). **Ausente reprova**, e a gravidade é **alta**: sem a declaração o navegador adivinha a codificação e todo acento pode sair corrompido no resultado de busca, o que quebra título e descrição na página de resultados.
- **`<meta name="viewport">`**: existe, com largura do dispositivo. Ausente derruba o comportamento no celular do bloco 2.
- **`lang` no `<html>`**: declarado e correto pro idioma do texto.
- **`<title>`** e **`<meta name="description">`**: existem, são únicos na página e não estão vazios.

**Como checar sem servidor:** basta ler o arquivo HTML e procurar as quatro declarações, uma por uma. É a checagem mais barata da lista e a mais esquecida.
**Conserto padrão:** acrescentar as declarações no topo do `<head>`, o `charset` como primeira linha dentro dele.
**Checagem verificável:** a tabela de entrega traz **uma linha para cada uma das quatro declarações**, com situação preenchida. Bloco 9 com menos de 4 linhas na tabela reprova a auditoria, porque declaração ausente só aparece quando alguém a procura nominalmente.

## A tabela de entrega

| Checagem | Situação | Detalhe | Conserto |
|---|---|---|---|

Situação em três valores: **passou**, **atenção**, **falhou**. Item não verificado escreve
`[A CONFIRMAR: não verificado]` na coluna de situação, e nunca "passou" por presunção.

**Os 9 blocos entram na tabela, sempre.** Bloco que você não conseguiu verificar entra assim mesmo, com
`[A CONFIRMAR: não verificado]`. Tabela entregue sem linha para `meta charset`, `viewport`, `lang`,
`title` e `meta description` reprova a auditoria: são as cinco que somem justamente por não terem
linha própria.
