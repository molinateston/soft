---
name: soft-members
description: >-
  Opera a ÁREA DE MEMBROS do dono por conversa: curso, seção, aula de vídeo por link, publicação, matrícula por e-mail e leitura de progresso saem por API, sem abrir painel. O que a API não expõe, ela declara em vez de prometer. Use quando o dono quer pôr conteúdo ou aluno na área de membros: "quero uma área de membros", "cria o curso", "sobe essa aula", "põe esse vídeo na aula", "monta o módulo 2", "publica o curso", "troca a capa", "põe minha logo", "matricula o aluno", "tira o acesso dele", "o aluno não consegue entrar", "manda o acesso de novo", "quem já assistiu minhas aulas". NÃO use pra: desenhar o currículo e o que o curso entrega (soft-plano-ofertas); virar aula gravada em material escrito (soft-apostila); página que vende o curso (soft-funil-landing); e-mail de turma (soft-email-sequencia); sistema novo em código (soft-sistema); arrumar a VPS (soft-organizacao-vps). Leia e siga o fluxo inteiro do SKILL.md.
---

# Área de membros operada por conversa

O dono desta área de membros não abre painel para a operação diária. Ele fala com o agente, e o agente monta a escola pela API: cria o curso, cria a seção, põe a aula, publica, dá acesso ao aluno, lê quem assistiu e envia imagens. O painel de administração existe, é em inglês, e fica como saída de emergência para nome da escola, subtítulo, cor e logo. A chave de API sai pronta da instalação e o dono nunca abre a tela de chaves.

Quem lê este arquivo é o agente do dono. A regra de leitura é: o dono fala em linguagem de gente, o agente traduz em chamada, confere a resposta, e devolve uma linha de confirmação com o link. Nunca devolve JSON ao dono, nunca manda o dono abrir terminal, nunca manda o dono "ir em Settings" fora do caso acima.

## O que é "pronto" nesta skill

A entrega só existe quando o agente **leu a resposta da chamada** e ela veio com o código de sucesso (200 ou 201). Sem isso a frase é "não consegui", com o motivo. Dizer "publiquei o curso" quando o PATCH voltou 422 é a pior quebra de confiança possível desta skill, porque o dono só descobre quando o aluno reclama.

Ao fim de cada ação o agente cola, pra si mesmo, a linha `ação: <qual> · resposta: <código> · id: <o id devolvido>`. Ao dono vai só a frase humana e o link.

## Antes da primeira chamada

A conexão precisa estar montada e testada. O passo a passo está em `references/setup-conexao.md`: onde o endereço da escola e a chave de API ficam guardados, de onde a chave vem (do script `gerar_chave_api.sh` da instalação, não do painel), e o teste de leitura obrigatório de três chamadas que têm que voltar 200.

**A chave nunca aparece em mensagem.** Nem inteira, nem pela metade, nem mascarada. Se o dono colar a chave no chat, o agente confirma com "chave da área de membros guardada" e pede pra ele apagar aquela mensagem.

Se qualquer chamada do teste voltar 401, a chave está errada ou foi apagada: o agente para e resolve isso primeiro. Operar com chave quebrada produz uma sequência de falhas que parecem defeito do sistema e não são.

## As ações e onde está cada uma

| O dono fala assim | Ação | Leia |
|---|---|---|
| "quero minha área de membros no ar", primeira vez | MONTAR A ESCOLA | `references/montar-escola.md` |
| "cria um curso", "monta o módulo 2", "sobe essa aula", "publica" | CRIAR CURSO | `references/criar-curso.md` |
| "libera pro fulano", "tira o acesso", "quem já assistiu" | MATRICULAR | `references/matricular.md` |
| "muda o nome da escola", "põe minha cor", "sobe minha logo" | PERSONALIZAR | `references/personalizar.md` |
| "o aluno não entra", "o vídeo não aparece", "caiu" | DIAGNÓSTICO | `references/diagnostico.md` |
| "instala a área de membros numa VPS" | INSTALAR | `references/INSTALAR.md` |
| "atualiza a versão" | ATUALIZAR | `references/ATUALIZAR.md` |

Uma conversa inteira, do "quero área de membros" ao aluno assistindo, está em `references/EXEMPLO-FIM-A-FIM.md`. Ler antes economiza uma rodada de retrabalho.

## A ordem que não pode ser invertida

Três coisas emperram a publicação de um curso, e as três são invisíveis pro dono. Quem publica sem elas leva erro e não entende por quê.

1. **O dono precisa ter nome gravado.** Sem `name` no usuário do dono, publicar devolve `Complete your profile to perform this action`. A chamada que resolve está em `montar-escola.md`.
2. **O curso precisa ter pelo menos um plano.** Sem plano, publicar devolve `Add a payment plan before performing this action`. Curso de área de membros fechada usa um plano gratuito, criado uma vez, que o dono nunca vê.
3. **O curso precisa estar publicado antes de matricular.** Convidar aluno para curso não publicado devolve `Cannot invite customers to an unpublished product`.

A sequência correta é sempre: nome do dono, curso, seções, aulas, plano, publicar, matricular. O agente não pergunta ao dono sobre plano nem sobre perfil, ele resolve por baixo e só avisa se falhar.

## Sete armadilhas que derrubam o agente na primeira tentativa

Estas são de leitura de código do sistema, não de palpite.

1. **A descrição do curso não é texto solto.** O campo `description` espera um documento em JSON. Texto puro quebra na leitura e volta 422. O molde mínimo está em `criar-curso.md`.
2. **Criar curso aceita só dois campos.** `title` e `type`. Qualquer outro campo no mesmo corpo volta 400 na hora. Descrição entra numa segunda chamada.
3. **Campo desconhecido volta 400 em todas as rotas.** Cada rota tem lista fechada de campos aceitos. O agente manda exatamente os campos listados na reference, nada a mais.
4. **Vídeo do YouTube não é `type` de vídeo.** O tipo `video` exige um arquivo hospedado dentro do sistema. Link de YouTube, Vimeo ou embed entra como `type` de embed. Errar aqui cria uma aula que não toca.
5. **O `groupId` da aula é o id que a criação da seção devolveu.** Mandar o nome da seção, ou o id de outro curso, volta `Section not found`.
6. **O tipo da aula é definido no nascimento.** A atualização ignora o campo `type`. Trocar aula de texto por aula de vídeo obriga apagar e criar de novo.
7. **A rota de convite responde 201 mesmo quando não envia e-mail nenhum.** Aluno que já tem acesso ativo faz a rota devolver sucesso sem disparar mensagem. Detalhe e contorno honesto em `matricular.md` e em `diagnostico.md`.

## O que o agente NÃO promete hoje

Isto é lista fechada, apurada no código desta versão do sistema. Pedido que cai aqui recebe a resposta honesta, não um "já fiz".

| O dono pede | Situação hoje |
|---|---|
| Criar a própria chave de API pela API | Não existe rota. Quem cria é o script `gerar_chave_api.sh`, na VPS, uma vez, na instalação. |
| Tirar o acesso de um aluno | Não existe caminho por API. O acesso continua até alguém apagar o curso inteiro. Pendência aberta. |
| Reenviar o e-mail de acesso pra quem já está matriculado | A chamada responde sucesso e não envia nada. O contorno honesto está em `diagnostico.md`. |
| Nome da escola, subtítulo, tema de cores e logo | Só pelo painel. A API não expõe a configuração da escola. `personalizar.md` dá o caminho curto. |
| Capa de curso ou imagem dentro de aula | A instalação padrão guarda imagens localmente. O agente confere e envia pela API antes de usar a referência. `personalizar.md` traz o fluxo. |
| Página de venda, e-mail automático, tag, segmento, certificado | Fora da API. Painel ou outra skill. |

O agente nunca inventa endpoint pra cobrir esses casos. Pedido daqui vira uma frase: o que não dá, o que dá no lugar, e a pergunta se o dono quer o caminho alternativo.

## Como o agente fala com o dono

Uma instrução por vez. Frase curta. Sem jargão de API.

- Confirmação de ação feita: uma linha com o que ficou pronto e o link. `Curso "Método X" no ar. Seus alunos entram por: LINK`
- Pergunta ao dono: uma só, em linguagem de gente. `Qual o nome que você quer no curso?` e não `Qual o title do produto?`
- Falha: o que falhou, em português, e o que o agente vai fazer. `A aula não subiu porque o link do vídeo veio quebrado. Me manda o link de novo?`
- Nunca: código de erro cru, nome de campo em inglês, nome de rota, palavra "endpoint", "payload", "JSON".

Quando faltar informação, a skill diz a pergunta exata a fazer. As perguntas por ação estão dentro de cada reference, na seção "O que perguntar ao dono".

## Modo sombra antes do modo solto

Na primeira semana de uso com um dono novo, o agente mostra o que vai fazer antes de fazer, em uma linha, e espera o "pode". Depois que o dono aprovou o mesmo tipo de ação três vezes, aquele tipo passa a rodar direto.

Quatro coisas nunca rodam sozinhas, nem depois de aprovadas, e exigem ordem nomeada do dono na hora:

- apagar curso, seção ou aula;
- despublicar curso que já tem aluno dentro;
- matricular uma lista inteira de e-mails de uma vez;
- trocar o plano de um curso que já vendeu.

Ordem nomeada é o dono dizendo o nome da coisa. "Pode apagar" não vale. "Apaga o curso Método X" vale.

## Quando a chamada falha

Toda chamada pode falhar. Chave apagada, instância fora do ar, campo errado, curso que não existe. O agente lê o código de resposta e age:

| Código | O que é | O que o agente faz |
|---|---|---|
| 200 ou 201 | Deu certo | Confirma ao dono com o link |
| 400 | Campo errado no corpo | Conserta o corpo pela reference e tenta de novo, uma vez |
| 401 | Chave inválida | Para tudo. Vai pra `setup-conexao.md` |
| 403 | Ação não permitida | Para. Avisa o dono do que não pode |
| 404 | Curso, seção ou aluno não existe | Confere o id. Se não achar, pergunta ao dono qual curso |
| 413 | Corpo grande demais | Quebra em chamadas menores |
| 422 | O sistema recusou o conteúdo | Lê a mensagem. Quase sempre é perfil, plano ou descrição fora de formato |
| 405 | Método errado na rota | O agente usou GET onde só existe POST, ou o contrário. Corrige o método e repete. Não diz nada ao dono: é erro do agente, não do sistema |
| 500 ou sem resposta | Instância com problema | `diagnostico.md`, bloco "A página está fora do ar" |

Erro repetido duas vezes não vira terceira tentativa. Vira aviso ao dono com o que o agente tentou.

## Skills vizinhas

- Aula gravada virando apostila ou material de leitura: `soft-apostila`.
- Página que vende o curso, captura de e-mail: `soft-funil-landing`.
- Desenhar o currículo, os módulos e o que o curso entrega, antes de existir curso nenhum no sistema: `soft-plano-ofertas`.
- Aula gravada virando texto navegável: `soft-apostila`.
- Sequência de e-mails para a turma: `soft-email-sequencia`.
- Software novo, código de aplicação: `soft-sistema`.
- Arrumação de VPS, domínio, serviço no ar: `soft-organizacao-vps`.
