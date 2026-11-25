#!/usr/bin/env bash
set -euo pipefail

# loop-convergence-guard.sh
# Monitora teto de iteracoes (N <= 5), detecta estagnacao (2 falhas iguais seguidas),
# registra episodios em utils/memory/episodes/ e executa rollback seguro sem reset --hard.
# Uso: bash .agents/hooks/loop-convergence-guard.sh <section_id> <iter|status|--reset> [error_hash] [target_file]
# Codigos de saida:
#   0  = Iteracao autorizada
#   90 = Parametros invalidos
#   91 = Limite maximo excedido (N > 5) -> Rollback disparado
#   92 = Estagnacao detectada (2 ciclos com mesmo hash) -> Rollback disparado

SECTION_ID="${1:-}"
ACTION="${2:-1}"
ERROR_HASH="${3:-NONE}"
TARGET_FILE="${4:-}"

if [ -z "$SECTION_ID" ]; then
  echo "[ERRO][loop-convergence-guard] Informe <section_id>." >&2
  exit 90
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

MAX_ITER=5
STATE_DIR="$ROOT/out/state"
EPISODES_DIR="$ROOT/utils/memory/episodes"
STATE_FILE="$STATE_DIR/convergence_${SECTION_ID}.state"
EPISODE_FILE="$EPISODES_DIR/${SECTION_ID}.md"

mkdir -p "$STATE_DIR" "$EPISODES_DIR"

if [ "$ACTION" = "--reset" ]; then
  rm -f "$STATE_FILE"
  echo "[OK][loop-convergence-guard] Estado resetado para '$SECTION_ID'."
  exit 0
fi

if [ "$ACTION" = "status" ]; then
  if [ -f "$STATE_FILE" ]; then
    cat "$STATE_FILE"
  else
    echo "LAST_SECTION=$SECTION_ID"
    echo "LAST_ITER=0"
    echo "LAST_HASH=NONE"
    echo "REPEAT_COUNT=0"
  fi
  exit 0
fi

if ! [[ "$ACTION" =~ ^[0-9]+$ ]]; then
  echo "[ERRO][loop-convergence-guard] Iteracao invalida: $ACTION" >&2
  exit 90
fi

ITERATION="$ACTION"
echo "[INFO][loop-convergence-guard] Monitorando iteracao $ITERATION/$MAX_ITER para '$SECTION_ID' (Hash: $ERROR_HASH)..."

rollback_target() {
  if [ -n "$TARGET_FILE" ] && git ls-files --error-unmatch "$TARGET_FILE" >/dev/null 2>&1; then
    echo "[ALERTA][loop-convergence-guard] Executando rollback seguro: git checkout HEAD -- $TARGET_FILE" >&2
    git checkout HEAD -- "$TARGET_FILE" || true
  fi
  rm -f "$STATE_FILE"
}

if [ "$ITERATION" -gt "$MAX_ITER" ]; then
  echo "[ERRO][loop-convergence-guard] Teto maximo de $MAX_ITER iteracoes excedido para '$SECTION_ID' (N=$ITERATION)." >&2
  rollback_target
  exit 91
fi

REPEAT_COUNT=0
if [ "$ERROR_HASH" != "NONE" ] && [ -n "$ERROR_HASH" ]; then
  if [ -f "$STATE_FILE" ]; then
    PREV_HASH="$(awk -F= '/^LAST_HASH=/{print $2}' "$STATE_FILE" || echo "")"
    PREV_REPEAT="$(awk -F= '/^REPEAT_COUNT=/{print $2}' "$STATE_FILE" || echo "0")"
    if [ "$PREV_HASH" = "$ERROR_HASH" ]; then
      REPEAT_COUNT=$((PREV_REPEAT + 1))
    else
      REPEAT_COUNT=1
    fi
  else
    REPEAT_COUNT=1
  fi

  if [ ! -f "$EPISODE_FILE" ]; then
    printf "# Episodios: %s\n\n| iter | error_hash | horario |\n|---|---|---|\n" "$SECTION_ID" > "$EPISODE_FILE"
  fi
  printf "| %s | %s | %s |\n" "$ITERATION" "$ERROR_HASH" "$(date '+%Y-%m-%d %H:%M')" >> "$EPISODE_FILE"

  if [ "$REPEAT_COUNT" -ge 2 ]; then
    echo "[ERRO][loop-convergence-guard] Estagnacao detectada: hash '$ERROR_HASH' repetido $REPEAT_COUNT vezes seguidas." >&2
    rollback_target
    exit 92
  fi
fi

cat << EOF > "$STATE_FILE"
LAST_SECTION=$SECTION_ID
LAST_ITER=$ITERATION
LAST_HASH=$ERROR_HASH
REPEAT_COUNT=$REPEAT_COUNT
EOF

echo "[OK][loop-convergence-guard] Iteracao $ITERATION/$MAX_ITER autorizada para '$SECTION_ID'."
exit 0
