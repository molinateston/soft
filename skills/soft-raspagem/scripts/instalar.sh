#!/usr/bin/env bash
# instalar.sh: confere e instala os 3 programas de raspagem (Instaloader, yt-dlp, gallery-dl).
#
# Pode rodar quantas vezes quiser: o que ja existe so tem a versao impressa.
# Ordem de instalacao do que falta, sem pedir senha de administrador:
#   1. pipx
#   2. pip do usuario (python3 -m pip install --user)
#   3. ambiente proprio em ~/.local/share/soft-raspagem/venv, com atalho em ~/.local/bin
#
# Uso:
#   bash scripts/instalar.sh              confere e instala o que faltar
#   bash scripts/instalar.sh --conferir   so confere, nao instala nada
#   bash scripts/instalar.sh --atualizar  atualiza os 3 para a versao oficial atual
#
# Saida: uma linha por programa (OK, INSTALADO, ATUALIZADO ou FALTA) e o resumo no fim.
# Codigo de saida: 0 = os 3 prontos; 1 = falta pelo menos um.

set -u

MODO="instalar"
case "${1:-}" in
  --conferir) MODO="conferir" ;;
  --atualizar) MODO="atualizar" ;;
  "" ) ;;
  -h|--help) sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) echo "Opcao desconhecida: $1 (use --conferir, --atualizar ou nada)"; exit 1 ;;
esac

BASE="${SOFT_RASPAGEM_HOME:-$HOME/.local/share/soft-raspagem}"
VENV="$BASE/venv"
BIN_USUARIO="$HOME/.local/bin"

# nome do comando = nome do pacote no PyPI, nos tres casos
PROGRAMAS="instaloader yt-dlp gallery-dl"

achar() {
  # devolve o caminho do programa: PATH, depois ~/.local/bin, depois o ambiente proprio
  local nome="$1" c
  c="$(command -v "$nome" 2>/dev/null)" && { echo "$c"; return 0; }
  for c in "$BIN_USUARIO/$nome" "$VENV/bin/$nome"; do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}

versao() {
  "$1" --version 2>/dev/null | head -n 1
}

PY=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done

via_pipx() {
  command -v pipx >/dev/null 2>&1 || return 1
  if [ "$MODO" = "atualizar" ]; then
    pipx upgrade "$1" >/dev/null 2>&1 || pipx install --force "$1" >/dev/null 2>&1
  else
    pipx install "$1" >/dev/null 2>&1
  fi
}

via_pip_usuario() {
  [ -n "$PY" ] || return 1
  "$PY" -m pip --version >/dev/null 2>&1 || return 1
  "$PY" -m pip install --user --upgrade --quiet "$1" >/dev/null 2>&1
}

via_venv() {
  [ -n "$PY" ] || return 1
  if [ ! -x "$VENV/bin/python" ]; then
    mkdir -p "$BASE" || return 1
    "$PY" -m venv "$VENV" >/dev/null 2>&1 || { rm -rf "$VENV"; return 1; }
  fi
  "$VENV/bin/python" -m pip install --upgrade --quiet "$1" >/dev/null 2>&1 || return 1
  mkdir -p "$BIN_USUARIO" && ln -sf "$VENV/bin/$1" "$BIN_USUARIO/$1"
}

instalar_um() {
  # tenta as 3 formas, na ordem; diz qual funcionou
  local nome="$1"
  if via_pipx "$nome" && achar "$nome" >/dev/null; then FORMA="pipx"; return 0; fi
  if via_pip_usuario "$nome" && achar "$nome" >/dev/null; then FORMA="pip do usuario"; return 0; fi
  if via_venv "$nome" && achar "$nome" >/dev/null; then FORMA="ambiente proprio"; return 0; fi
  return 1
}

atualizar_um() {
  # atualiza pelo mesmo caminho em que o programa foi instalado
  local nome="$1" caminho="$2" real
  real="$(readlink -f "$caminho" 2>/dev/null || echo "$caminho")"
  case "$real" in
    "$VENV"/*) "$VENV/bin/python" -m pip install --upgrade --quiet "$nome" >/dev/null 2>&1 && { FORMA="ambiente proprio"; return 0; } ;;
    */pipx/venvs/*) via_pipx "$nome" && { FORMA="pipx"; return 0; } ;;
    "$HOME"/*) via_pip_usuario "$nome" && { FORMA="pip do usuario"; return 0; } ;;
  esac
  return 1
}

FALTAM=0
echo "== Programas de raspagem =="
for nome in $PROGRAMAS; do
  FORMA=""
  if caminho="$(achar "$nome")"; then
    if [ "$MODO" = "atualizar" ]; then
      antes="$(versao "$caminho")"
      if atualizar_um "$nome" "$caminho"; then
        caminho="$(achar "$nome")"
        echo "ATUALIZADO  $nome  $antes -> $(versao "$caminho")  ($caminho, por $FORMA)"
      else
        echo "OK          $nome  $antes  ($caminho)  [instalado pelo sistema: atualize pelo gerenciador de pacotes]"
      fi
    else
      echo "OK          $nome  $(versao "$caminho")  ($caminho)"
    fi
    continue
  fi
  if [ "$MODO" = "conferir" ]; then
    echo "FALTA       $nome  (rode sem --conferir para instalar)"
    FALTAM=$((FALTAM + 1))
    continue
  fi
  if instalar_um "$nome"; then
    caminho="$(achar "$nome")"
    echo "INSTALADO   $nome  $(versao "$caminho")  ($caminho, por $FORMA)"
  else
    echo "FALTA       $nome  (nao consegui instalar por pipx, pip do usuario nem ambiente proprio)"
    FALTAM=$((FALTAM + 1))
  fi
done

echo
echo "== Apoio =="
if [ -n "$PY" ]; then
  echo "OK          python  $("$PY" --version 2>&1)"
else
  echo "FALTA       python3 (sem ele nada instala; peca ao dono: sudo apt install -y python3 python3-venv python3-pip)"
fi
if command -v ffmpeg >/dev/null 2>&1; then
  echo "OK          ffmpeg  $(ffmpeg -version 2>/dev/null | head -n 1 | cut -d' ' -f3)"
else
  echo "AVISO       ffmpeg ausente: dados, legendas e imagens funcionam; juntar video com audio em alta qualidade e extrair mp3 nao. Peca ao dono: sudo apt install -y ffmpeg"
fi
if command -v deno >/dev/null 2>&1 || command -v node >/dev/null 2>&1; then
  echo "OK          motor de JavaScript (deno ou node) para o YouTube"
else
  echo "AVISO       sem deno nem node: o YouTube pode entregar menos formatos de video. Dados e legendas costumam funcionar."
fi
case ":$PATH:" in
  *":$BIN_USUARIO:"*) ;;
  *) [ -d "$BIN_USUARIO" ] && echo "AVISO       $BIN_USUARIO nao esta no PATH. O coletar.py acha os programas mesmo assim; para chamar na mao: export PATH=\"$BIN_USUARIO:\$PATH\"" ;;
esac

echo
if [ "$FALTAM" -eq 0 ]; then
  echo "RESUMO: os 3 programas estao prontos."
  exit 0
fi
echo "RESUMO: falta(m) $FALTAM programa(s)."
if [ "$MODO" != "conferir" ]; then
  echo "O que costuma resolver, com o dono rodando uma vez como administrador:"
  echo "  sudo apt install -y python3 python3-venv python3-pip pipx"
  echo "Depois rode este instalador de novo."
fi
exit 1
