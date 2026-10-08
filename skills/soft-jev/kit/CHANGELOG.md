# Changelog de lições da calibração

Lista curta de lições que a calibração deste sistema já aprendeu sobre julgar
pergunta versus ordem e sobre o que ele pode afirmar sozinho. Toda lição nova
entra por acréscimo; nenhuma remove uma checagem anterior.

## Pergunta versus ordem

- Frase com "eu quero X" ou "quero que X" é ORDEM, não pergunta — desejo
  expresso já conta como pedir para executar.
- Pedido de ação seguido de confirmação solta no final ("beleza?", "né?")
  continua ORDEM: execute e responda a confirmação junto, sem tratar a
  mensagem inteira como pergunta.
- Instrução que corrige a conduta do próprio agente ou impõe uma regra de
  comportamento também é ordem a executar, mesmo escrita como pergunta.
- Quando a mensagem cita um texto anterior e traz uma linha nova do usuário
  depois, julgue só o texto novo — a citação é contexto, não instrução.

## Afirmar sem provar

- Nunca afirme "publicado", "commitado", "testado" ou "concluído" sem ter
  rodado, no mesmo turno, a checagem que provaria isso (comando de
  versionamento, chamada real, execução do teste). Sem essa verificação, a
  afirmação vira aviso registrado, não passa em silêncio.

## Mudar o texto de uma pergunta

- Antes de trocar o texto de uma pergunta calibrada, meça a versão antiga e a
  nova no mesmo conjunto de casos; só promova a nova se empatar ou ganhar,
  sem piorar nenhum caso que já funcionava.
- Mudança de texto nunca muda o tipo de resposta, as opções ou os limiares já
  calibrados — só a redação muda, e só depois de medida.

## Regra geral

- Toda melhoria é um acréscimo: checagem nova, pergunta nova ou aviso novo.
  Nenhuma calibração desliga ou enfraquece uma checagem que já existe; se
  algo não funciona bem, o caminho é ajustar texto ou limiar com medição,
  nunca remover a checagem.
