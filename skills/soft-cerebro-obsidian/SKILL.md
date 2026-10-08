---
name: soft-cerebro-obsidian
description: >-
  Monta o SEGUNDO CÉREBRO do negócio: uma pasta de notas em Markdown que o agente lê antes de responder e atualiza sozinho quando aprende algo, mais um mapa visual (página única com núcleos, ligações, busca e versão de celular) que se atualiza todo dia. Abre no Obsidian, mas funciona sem ele. Use quando o pedido for: "monta meu segundo cérebro", "cérebro no Obsidian", "memória do meu negócio em notas", "o agente esquece o que decidimos", "quero um mapa das minhas notas", "base de conhecimento do negócio", "organiza minhas notas em grafo". NÃO use pra: transformar uma aula gravada em apostila (soft-apostila); posicionamento e método de marca (soft-plano-posicionamento); construir site ou painel com código (soft-sistema); converter documento em Word ou PDF (soft-exportar-documentos); decidir o próximo passo do negócio (soft-leon). Leia e siga o fluxo inteiro do SKILL.md.
---

# Segundo cérebro: memória do negócio em notas, com mapa visual

Esta skill entrega duas coisas. A primeira é uma **pasta de notas** (`brain/`) que o agente consulta antes de responder sobre histórico, decisões, números e pessoas, e que ele mesmo atualiza na hora em que aprende algo. A segunda é um **mapa visual** dessas notas, numa página só, que se refaz todo dia sem ninguém mexer.

Quem ganha: o dono para de repetir a mesma explicação para o agente, e o agente para de inventar o que não sabe, porque a resposta sai de uma nota com data e prova.

## Como conduzir (regras de conversa)

- **Uma pergunta por vez.** Cada pergunta diz o que o agente precisa, por quê, onde o dono acha a resposta e o que vem depois. Nunca despeje a lista inteira.
- **Fale em linguagem de gente.** Diga "pasta de notas" e "mapa", não "vault", "grafo" ou "regex" (a não ser que o dono use o termo).
- **Nada de dado inventado.** Toda nota nasce do que o dono disse ou de um arquivo que ele mostrou. O que faltar entra como `PENDENTE:`, nunca como chute. Número, preço e nome de pessoa só entram com a fonte dita na própria nota.
- **Segredo não entra.** Senha, chave de API, token, CPF e cartão ficam fora das notas. Se o dono colar um, o agente guarda só o fato ("a chave existe e fica no cofre X") e avisa.
- **Nunca sobrescreva.** Os scripts não apagam nem trocam nota existente. Se já há uma pasta de notas, o agente lê primeiro e encaixa a estrutura nela.

Os scripts ficam na pasta `scripts/` desta skill (resolva o caminho pela pasta onde esta skill está instalada). Precisam só de Python 3. O teste com imagem usa Chrome ou Chromium, e é opcional.

## Etapa 0. Entender o ponto de partida

Faça estas perguntas, uma por vez, e espere a resposta de cada uma.

1. **"Em qual pasta do seu computador fica o projeto onde você trabalha com o agente?"** (O agente precisa do caminho para criar a pasta `brain/` ao lado do trabalho. Se o dono não sabe, o agente usa a pasta onde está rodando e diz qual é.)
2. **"Você já tem notas escritas (Obsidian, Notion, Google Docs, pastas soltas)?"** Se sim, peça o caminho ou a exportação. O agente lê e encaixa, em vez de recomeçar. Se não, siga para a etapa 1.
3. **"Qual o nome do negócio, como você quer que apareça no topo do mapa?"**

O Obsidian é um aplicativo gratuito que abre uma pasta de notas e mostra as ligações entre elas. É opcional: a pasta `brain/` funciona sem ele, e o mapa desta skill é uma página própria. Se o dono quiser, ele abre a pasta `brain/` no Obsidian ("Abrir pasta como cofre") e usa os `[[links]]` normalmente.

## Etapa 1. Criar a estrutura

Rode `python3 scripts/inicia.py <pasta-do-projeto> --nome "<nome do negócio>"`.

Ele cria, sem sobrescrever nada que exista: `brain/MAPA.md` (o índice), `brain/MEMORIA-VIVA.md` (o que vale agora), `brain/agentes/`, `brain/arquivo/`, `brain/ideias/`, `brain/ESTADO/` (arquivos de robôs, fora do mapa), `trabalho/` (as entregas) e `config.json`. O significado de cada pasta está em `references/estrutura-da-base.md`.

Conte ao dono, em duas frases, o que foi criado e que a próxima etapa é encher o cérebro com o que ele já sabe.

## Etapa 2. Encher o cérebro por entrevista

Use `references/entrevista.md`: cada tema tem a pergunta, o motivo e o nome da nota que nasce dela. Faça **um tema por vez**, nesta ordem:

1. cliente ideal; 2. oferta principal; 3. preços e condições; 4. método (como o trabalho é feito); 5. objeções que empacam a compra; 6. identidade visual e voz; 7. pessoas-chave (clientes, sócios, equipe); 8. números que o dono usa para decidir.

Depois de cada resposta, o agente:
- escreve a nota em `brain/NOME-EM-MAIUSCULAS.md` (um assunto por arquivo, ligando com `[[OUTRA-NOTA]]` quando fizer sentido);
- acrescenta uma linha para ela no `brain/MAPA.md`, na seção certa;
- põe no `MEMORIA-VIVA.md` a linha `- [AAAA-MM-DD HH:MM] nota criada: <assunto>. brain/<arquivo>`;
- mostra ao dono o texto da nota em até 6 linhas e pergunta se está certo antes de seguir.

O dono pode parar quando quiser. Cinco notas boas já funcionam. O que ficou de fora vira `PENDENTE:` no `MEMORIA-VIVA.md`.

## Etapa 3. A regra de gravar na hora

É o passo que mais importa, porque é ele que mantém o cérebro vivo. Explique ao dono: "daqui para frente, sempre que o agente aprender algo, ele grava no cérebro na hora, e antes de responder sobre histórico ele consulta o cérebro".

Peça licença para acrescentar o bloco de regras ao arquivo de instruções do projeto (o que o agente lê toda vez que abre o projeto). Com o sim, rode `python3 scripts/inicia.py <pasta-do-projeto> --grava-claude-md`. Sem o sim, mostre o bloco (ele sai no final do `inicia.py`) e diga onde colar. Detalhes em `references/estrutura-da-base.md`.

## Etapa 4. Definir os conceitos e gerar o mapa

Se o dono quiser ver o resultado antes de ter notas dele, gere o exemplo: `python3 scripts/monta.py exemplo/config.exemplo.json` e abra `exemplo/cerebro-site/index.html` (30 pontos, de uma base de mentira).

Os **conceitos** são as palavras que mais aparecem nas notas e costuram o mapa: toda nota que tiver a palavra se liga ao conceito.

1. Rode `python3 scripts/sugere.py config.json`. Ele lista as palavras mais repetidas que ainda não são conceito.
2. O agente escolhe de 15 a 40 que façam sentido para o negócio (não use palavra que aparece em mais da metade das notas, ela liga tudo com tudo), dá um nome bonito e escolhe o núcleo de cada uma.
3. Edite `config.json` (campos em `references/config.md`): de 6 a 12 núcleos (`hubs`), os `conceitos`, as `pastas` que entram e as `pessoas`, se houver.
4. Rode `python3 scripts/monta.py config.json`. A resposta diz quantos pontos e ligações saíram e avisa das notas órfãs.

Se o mapa saiu quase vazio, faltam conceitos. Se saiu tudo ligado em tudo, alguma regex está genérica. Mais em `references/se-algo-der-errado.md`.

## Etapa 5. Provar antes de dar por pronto

1. `bash scripts/testa.sh cerebro-site/index.html teste-mapa` abre a página num navegador sem tela, confere erros e tira 4 prints (visão geral, nota aberta, busca, celular). Precisa responder `erros JS: 0`.
2. **Abra os 4 prints e olhe.** Confira: nomes legíveis e com acento certo, nenhum núcleo isolado sem ligação, a busca destaca a nota, o celular não corta nada. Zero erro não prova que está bonito.
3. `python3 scripts/confere.py config.json` confere a base: link quebrado, segredo escrito, nota fora do índice. Erro precisa chegar a zero.

Entregue ao dono: o caminho do `index.html` (para abrir com duplo clique), quantas notas e ligações, o que ficou como `PENDENTE:` e o que ele faz de agora em diante (nada: o agente grava sozinho).

## Etapa 6. Atualizar todo dia e publicar (opcional)

Pergunte: **"Você quer ver o mapa no celular, de qualquer lugar?"** Se não, pare aqui: abrir o `index.html` no computador basta.

Se sim, ou se o dono quer atualização diária, siga `references/rotina-e-publicacao.md`: o script `scripts/atualiza.sh` monta de novo, confere e escreve uma linha em `cerebro-diario.log`; o agendamento diário e a publicação em hospedagem estática estão lá. **Aviso obrigatório antes de publicar:** o mapa mostra o nome de todas as notas. Em endereço público, ponha senha, ou use `"texto": "nenhum"` no config para não levar o conteúdo das notas.

## O que esta skill não faz

- Não apaga nem reescreve notas existentes sem pedir.
- Não publica nada sem o dono dizer onde.
- Não guarda segredo, e avisa quando o dono tenta.
- Não substitui o julgamento do dono: o cérebro registra, quem decide é ele.
