# Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão e não recebe uma lista do que falta. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição (a mesma de `perfil.json` e `video-projects/`). No Windows, troque `python3` por `python`.

## 1. Rode o instalador

```
python3 <S>/instalar_ambiente.py --perfil ffmpeg --pasta <pasta>
```

Ele confere o sistema, o gerenciador de pacotes, o privilégio e a rede, e instala sozinho, na ordem certa, o que faltar. Tudo que dá para instalar sem privilégio fica dentro da pasta: node 22 oficial em `.ambiente/node`, ffmpeg e ffprobe estáticos em `.ambiente/bin`, HyperFrames 0.8.93 e GSAP 3.14.2 em `node_modules`, faster-whisper num venv em `.ambiente/venv`. O Chrome do render vai para o cache do usuário. No fim, grava `ambiente.json` na pasta, com caminho e versão de cada peça.

Na primeira vez leva de 3 a 5 minutos e baixa perto de 400 MB. Rodar de novo é seguro: sem nada faltando, termina em segundos e não muda nenhum arquivo. Para ver o plano sem executar nada, acrescente `--simular`.

## 2. Leia a tabela

A primeira tabela mostra cada peça com um estado:

| Estado | Quer dizer |
|---|---|
| `ok` | pronto, nada a fazer |
| `instalando` | o instalador resolve agora, sozinho |
| `FALTA` | só o dono da máquina resolve (pede privilégio que você não tem) |
| `aviso` | peça opcional ausente; a edição segue sem ela |

A segunda tabela, a conferência final, confirma o que ficou instalado. Depois vale o código de saída:

| Saída | O que fazer |
|---|---|
| 0 | ambiente pronto: vá para a prova de render |
| 1 | a conferência final reprovou: leia o item e o log em `<pasta>/.ambiente/logs` |
| 2 | argumento errado no comando: corrija e rode de novo |
| 3 | falta algo que só o dono faz: veja o passo 3 abaixo |
| 4 | uma instalação falhou: leia o final do log que ele mostra, rode de novo uma vez (queda de rede é o caso comum) e, se repetir, mostre ao dono o passo e o log |

## 3. Saiu 3: peça ao dono, em uma frase, e espere

O instalador imprime o motivo e o comando exato. Passe ao dono numa frase só, com o comando inteiro, e espere a resposta. Exemplo: "Para eu editar nesta máquina, preciso que você rode como administrador: `sudo apt-get update && sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y libnss3 libgbm1`. Me avise quando terminar." Quando o dono confirmar, rode o instalador de novo. Não procure outro caminho para pular esse passo.

## 4. Carregue o ambiente em todo comando

Node e ffmpeg podem ter sido instalados dentro da pasta, fora do caminho padrão do sistema. Por isso todo comando da edição começa carregando o ambiente:

- Linux e Mac: `. <pasta>/.ambiente/ativar.sh && node <S>/novo-reel.mjs ...`
- Windows (cmd): `call <pasta>\.ambiente\ativar.bat && node <S>\novo-reel.mjs ...`

O mesmo arquivo aponta a transcrição para o venv da pasta (variável `WHISPER_PYTHON`).

## 5. Rode a prova de render

```
python3 <S>/prova_render.py --perfil ffmpeg --pasta <pasta> --audio <vídeo do dono>
```

Com `--perfil hyperframes`, ela monta um projeto mínimo de 3 segundos em 1080x1920, renderiza com o HyperFrames da pasta do mesmo jeito que a skill renderiza e confere tamanho, 30 quadros por segundo, duração, áudio, arquivo íntegro, texto visível e borda direita sem faixa preta. Com `--perfil ffmpeg`, ela passa um vídeo de teste pelas codificações que a skill usa e confere cada saída. Nos dois perfis, ela transcreve os primeiros 10 segundos do vídeo do dono e exige palavras com tempo. Sem `--audio`, prova só que o motor de transcrição carrega e roda.

A última linha diz `PROVA DE RENDER: OK` (saída 0) ou `REPROVADA` (saída 1, com o item que falhou). Reprovou: não edite. Diga ao dono qual item falhou, rode o instalador de novo e repita a prova.

## 6. Só então edite

Com o instalador em 0 e a prova em OK, siga o fluxo da skill a partir do passo 1.

## Regra dura

Nunca entregue uma edição simplificada por falta de ferramenta. Se o estilo pede HyperFrames, a edição sai com HyperFrames: nada de uma versão mais pobre feita só com ffmpeg, nada de pular legenda, apoio ou animação porque uma peça não instalou. Ou o ambiente prova que renderiza, ou a skill para e diz ao dono exatamente o que falta.

## No relatório da edição

Registre a prova: a linha `PROVA DE RENDER`, o tempo, o vídeo da prova e os itens conferidos. Tudo isso está em `<pasta>/.ambiente/prova-render.json`. Registre também as versões de `ambiente.json` (HyperFrames, ffmpeg, faster-whisper) e qualquer comando que o dono precisou rodar.
