#!/usr/bin/env bash
# Instalador da skill na pasta de skills do agente.
# Uso: bash install.sh   (rode de dentro da pasta do repo, OU clone direto no destino)
set -e
DEST="$HOME/.claude/skills/soft-editor-video"
HERE="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$HOME/.claude/skills"
if [ "$HERE" != "$DEST" ]; then
  echo "Copiando skill para $DEST ..."
  mkdir -p "$DEST"
  cp -R "$HERE/." "$DEST/"
fi
echo "OK! Skill instalada em $DEST"
echo "Abra o agente e mande um vídeo pra editar. Na 1a vez ele pede suas chaves e entrevista seus personagens."

# checagem rápida de dependências
command -v ffmpeg >/dev/null || echo "AVISO: instale o ffmpeg (brew install ffmpeg / apt install ffmpeg)"
command -v python3 >/dev/null || echo "AVISO: instale o python3"
