#!/usr/bin/env bash
set -euo pipefail

# pre-task-audit.sh
# Pre-Step Interceptor: valida estado do repositorio Git, ferramentas LaTeX,
# acesso a fonte de verdade ../soc-proj, protecao de arquivos centrais e
# gera snapshot inicial para boundary-guard.py.
# Uso: bash .agents/hooks/pre-task-audit.sh [--strict-clean]
# Codigos de saida:
#   0  = Pre-requisitos e fronteira validados
#   10 = Working tree suja em modo --strict-clean ou fora de repo Git
#   11 = Ferramenta obrigatoria ausente (latexmk/pdflatex/bibtex/python3)
#   12 = Fonte de verdade ../soc-proj inacessivel
#   13 = Arquivo protegido modificado sem autorizacao (ALLOW_PROTECTED=1)

STRICT_CLEAN="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

echo "[INFO][pre-task-audit] Auditando ambiente, Git e pre-requisitos em $ROOT..."

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "[ERRO][pre-task-audit] Repositorio Git nao encontrado." >&2
  exit 10
fi

for cmd in latexmk pdflatex bibtex python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERRO][pre-task-audit] Ferramenta obrigatoria ausente no PATH: $cmd" >&2
    exit 11
  fi
done

for req in "../soc-proj/README.md" "../soc-proj/utils/plan/STATUS.md" "../soc-proj/utils/plan/Matriz_de_Testes_e_Métricas.csv" "../soc-proj/utils/memory/decisions.md"; do
  if [ ! -f "$req" ]; then
    echo "[ERRO][pre-task-audit] Fonte autoritativa ausente: $req" >&2
    exit 12
  fi
done

if [ "${ALLOW_PROTECTED:-0}" != "1" ]; then
  if ! git diff --quiet -- config/estilo_seminario.sty config/00_config.tex main.tex .agents/manifest.json 2>/dev/null; then
    echo "[ERRO][pre-task-audit] Arquivos protegidos possuem alteracoes nao comitadas." >&2
    exit 13
  fi
fi

if [ "$STRICT_CLEAN" = "--strict-clean" ]; then
  STATUS="$(git status --porcelain)"
  if [ -n "$STATUS" ]; then
    echo "[ERRO][pre-task-audit] Working tree nao esta limpa (--strict-clean):" >&2
    echo "$STATUS" >&2
    exit 10
  fi
fi

mkdir -p out
python3 "$SCRIPT_DIR/boundary-guard.py" snapshot

echo "[OK][pre-task-audit] Pre-requisitos verificados e snapshot de fronteira gravado."
exit 0
