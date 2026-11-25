#!/usr/bin/env bash
set -euo pipefail

# post-write-compile.sh
# Compilador deterministico com isolamento de artefatos em out/.
# Uso: bash .agents/hooks/post-write-compile.sh [main|all|secoes/<arquivo>.tex]
# Codigos de saida:
#   0  = Compilacao concluida sem erros
#   50 = Alvo nao encontrado
#   51 = Falha na compilacao LaTeX

TARGET="${1:-all}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
OUT_DIR="$ROOT/out"

mkdir -p "$OUT_DIR"

compile_one() {
  local tex_rel="$1"
  local tex_abs="$ROOT/$tex_rel"
  local stem
  stem="$(basename "$tex_rel" .tex)"
  local log_file="$OUT_DIR/compile_${stem}.log"

  if [ ! -f "$tex_abs" ]; then
    echo "[ERRO][post-write-compile] Arquivo nao encontrado: $tex_rel" >&2
    exit 50
  fi

  echo "[INFO][post-write-compile] Compilando $tex_rel -> out/${stem}.pdf..."
  if latexmk -cd -pdf -file-line-error -interaction=nonstopmode -halt-on-error \
      -outdir="$OUT_DIR" -auxdir="$OUT_DIR" "$tex_abs" > "$log_file" 2>&1; then
    local overfull_count=0
    local undef_refs=0
    local latex_log="$OUT_DIR/${stem}.log"
    if [ -f "$latex_log" ]; then
      overfull_count="$(grep -c 'Overfull \\hbox' "$latex_log" || true)"
      undef_refs="$(grep -Ec 'LaTeX Warning: (Reference|Citation).*undefined' "$latex_log" || true)"
    fi
    echo "[OK][post-write-compile] $tex_rel -> out/${stem}.pdf (Overfull hbox: $overfull_count, Refs/Cites indefinidas: $undef_refs)"
    if [ "$overfull_count" -gt 0 ]; then
      grep 'Overfull \\hbox' "$latex_log" | head -n 5 || true
    fi
  else
    echo "[ERRO][post-write-compile] Falha ao compilar $tex_rel. Ultimas linhas do log:" >&2
    tail -n 30 "$log_file" >&2
    exit 51
  fi
}

case "$TARGET" in
  main|main.tex)
    compile_one "main.tex"
    ;;
  all)
    compile_one "main.tex"
    for sec in "$ROOT"/secoes/*.tex; do
      compile_one "secoes/$(basename "$sec")"
    done
    ;;
  *)
    compile_one "$TARGET"
    ;;
esac

echo "[OK][post-write-compile] Compilacao finalizada com exito (artefatos isolados em out/)."
exit 0
