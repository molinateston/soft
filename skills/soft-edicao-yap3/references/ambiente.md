# Antes de editar: ambiente pronto, instalado por você

Quem prepara a máquina é você, o agente. O dono não instala nada na mão e não recebe uma lista do que falta. Nos comandos, `<S>` é a pasta `scripts` desta skill e `<pasta>` é a pasta de trabalho da edição (a mesma de `perfil.json` e `video-projects/`). No Windows, troque `python3` por `python`.

## 1. Rode o instalador

```
python3 <S>/instalar_ambiente.py --perfil ffmpeg --pasta <pasta>
```

Ele confere o sistema, o gerenciador de pacotes, o privilégio e a rede, e instala sozinho, na ordem certa, o que faltar. Tudo que dá para instalar sem privilégio fica dentro da pasta: node 22 oficial em `.ambiente/node`, ffmpeg e ffprobe estáticos em `.ambiente/bin`, HyperFrames 0.8.93 e GSAP 3.14.2 em `node_modules`, faster-whisper e os pacotes Python dos scripts desta skill (numpy, Pillow e OpenCV, com versão mínima) num venv em `.ambiente/venv`. O Chrome do render vai para o cache do usuário. No fim, grava `ambiente.json` na pasta, com caminho e versão de cada peça.

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

O mesmo arquivo aponta a transcrição para o venv da pasta (variável `WHISPER_PYTHON`) e põe na frente do caminho um `python3` que usa esse venv, onde o instalador pôs e provou, importando, os pacotes que os scripts desta skill importam. Sem carregar o ambiente, os scripts de GIF e de variação param no import.

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

## Dependências externas do fluxo YAP3 (variações, espelho e GIF)

O que vem dentro da skill e o que precisa vir de fora. Caminhos dos scripts são sempre por argumento ou relativos ao plano; nenhum script depende de pasta fixa da máquina.

| Item | Onde fica | Observação |
|---|---|---|
| Modelo de rosto YuNet | `assets/modelos/face_detection_yunet_2023mar.onnx` | Incluído (OpenCV Zoo, licença MIT, texto em `assets/modelos/LICENSE-YuNet.txt`). Precisa de OpenCV 4.8 ou mais novo (`cv2.FaceDetectorYN`): o instalador põe `opencv-python-headless` no venv da pasta. |
| Kalam Bold | `assets/fontes/Kalam-Bold.ttf` | Incluída com a licença `OFL-Kalam.txt`. SHA256 `2f6576601db015d4f6c08678120277fc8510b98c06e932ce7a6a9cbff4cbdded`. |
| Advercase Bold (título) | não incluída | Licença de redistribuição não encontrada. Coloque o arquivo na pasta `fontes` do plano. SHA256 esperado `0a18220556c2f22ee128dedf7322d9d11cd4c7aefa1fade731dfbff12ad32cc5`; confira com `python3 scripts/reproduzir_molde.py --fontes <pasta> --so Advercase-Bold.ttf`. Sem ela, `variar_gancho.py` para com "falta a fonte". |
| Modelo de transcrição large-v3 | baixado na primeira vez | `faster-whisper` com `large-v3` (cerca de 3 GB). Baixe uma vez com rede; depois `transcrever_tomadas.py` roda com `HF_HUB_OFFLINE=1`. |
| Sons do GIF e do gancho | `assets/sons-gif/`, `assets/sfx-gancho/` | Sintetizados localmente, obra própria (CC0). |
| Registro de memes usados | fora da skill | Semente só leitura em `assets/memes-usados.json`. O registro do dono fica em `YAP_MEMES_USADOS`, senão `$LEON_DATA_DIR/soft-edicao-yap3/memes-usados.json`, senão `~/.leon/dados/soft-edicao-yap3/memes-usados.json`. `scripts/memes_usados.py` lê os dois e grava só no registro. |
| ffmpeg com libx265 10 bits | sistema | HEVC Main10 HLG BT.2020. `cor_hlg.py` define o encoder (preset fast, crf 16, GOP 30, sem B-frames) igual ao da V3, o que permite concatenar com `-c:v copy`. |
| Motor que gera a V3 | não incluído | A V3 normal, o espelho da V3, o corpo com letra branca e as correções do EP3 e EP4 foram feitos por um motor próprio de cada projeto. A skill parte desses arquivos prontos (campos `v3_final`, `v3_espelho`, `correcoes`, `corpo_normal`, `ponte_normal` do plano). Em episódio novo, a V3 sai pela "Ordem de edição" da skill. |
| Provas e molde do perfil Manuscrito (ep2) | não incluídos | `references/perfil-tipografico.json` registra os arquivos do lote aprovado com caminho relativo à pasta dele (`lote-aprovado/...`) e `references/texto-legenda-elementos.md` cita só o nome dos prints de evidência e do MP4 do molde do gancho. São registro de origem; nada roda a partir deles. `reproduzir_molde.py` procura as fontes pelo nome, em `--fontes`, e confere o lote com `--origem <pasta do lote aprovado>`. |
| Resumo do curso de YAP | não incluído | A skill traz só o resumo em `references/revisao-fluidez-elementos-camera-2026-10-15.md`; a pasta original de resumos do curso fica fora. |

Diferença conhecida: nos projetos originais a ponte (quadros `k_p` até `KG-1`) era renderizada pelo motor da V3. Aqui ela é decodificada do arquivo pronto e recodificada, com perda de geração pequena (PSNR em torno de 46 dB ou mais, acima do limite de 40 do `auditar_variacao.py`). O corpo continua por cópia de pacote, bit a bit igual.
