# Licenças do que vem dentro desta skill

Conferido em 15/10/2026 pela tabela `name` de cada arquivo de fonte (campos 0, copyright, e 13 ou 14, licença) e por `fc-scan`.

## Fontes (em `template/fonts/`)

| Arquivo | Família | Copyright | Licença | Texto da licença |
|---|---|---|---|---|
| `Inter-SemiBold.ttf`, `Inter-Medium.ttf` | Inter 3.019 | 2020 The Inter Project Authors | SIL Open Font License 1.1 | `OFL-Inter.txt` |
| `InstrumentSerif-Italic.woff2` | Instrument Serif 1.000 | 2022 The Instrument Serif Project Authors | SIL Open Font License 1.1 | `OFL-InstrumentSerif.txt` |
| `Caveat-Bold.woff2` | Caveat 2.000 | 2014 The Caveat Project Authors | SIL Open Font License 1.1 | `OFL-Caveat.txt` |

As três vão sem modificação. A OFL permite levar junto com software, desde que o aviso de copyright e a licença acompanhem cada cópia (por isso os arquivos `OFL-*.txt` ao lado) e que a fonte não seja vendida sozinha. "Inter" é marca registrada do autor; a skill só usa o arquivo original.

Fonte que o dono declarar no `perfil.json` (`fonte_texto`, `fonte_destaque`) é copiada só para o projeto dele, nunca para dentro da skill. A licença dela é responsabilidade do dono.

## Imagens

Nenhuma. A origem não trazia foto, avatar, print de exemplo nem emoji, e esta versão não acrescenta. Prints, capas e avatar vêm do dono, com origem anotada em cada projeto.

## Scripts

| Arquivo | Origem | Licença |
|---|---|---|
| `scripts/*.mjs`, `scripts/transcrever.py` | adaptados do pacote de estilos de edição repassado ao dono da operação (declaração de direito dele, não verificada por nós) | uso conforme essa declaração |
| `scripts/lint_copy.py`, `scripts/checar_titulos.py` | régua da casa | uso interno da operação e dos clientes dela |

## O que NÃO vem dentro (instalado pelo cliente, ver "Primeiros passos" do SKILL.md)

| Item | Versão | Licença |
|---|---|---|
| HyperFrames | 0.8.93 | Apache 2.0 |
| GSAP | 3.14.2 | licença padrão gratuita da GSAP (não é código aberto; por isso vem do npm na máquina do cliente e não dentro da skill) |
| Chrome sem janela do render (chrome-headless-shell) | baixado pelo HyperFrames | licença do Chromium (BSD e componentes) |
| ffmpeg | a do sistema | LGPL ou GPL, conforme a compilação |
| faster-whisper e o modelo de transcrição | a do pip | MIT |
