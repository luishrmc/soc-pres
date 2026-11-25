#!/usr/bin/env bash
set -euo pipefail

# slide-style-linter.sh
# Post-Step Verifier: valida invariantes de estilo Beamer em secoes/<sec>/*.tex.
# Uso: bash .agents/hooks/slide-style-linter.sh [--all | secoes/<sec> | caminho/arquivo.tex]
# Codigos de saida:
#   0  = Aprovado
#   30 = Arquivo ou diretorio alvo nao encontrado
#   31 = Travessao proibido (em-dash/en-dash Unicode) detectado em prosa
#   32 = Excesso de densidade visual (> 6 bullets por bloco itemize)
#   33 = Jargao promocional ou adjetivo vago proibido detectado
#   34 = Erro de sintaxe de frame (desbalanceado ou listagem sem [fragile])

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

TARGET="${1:---all}"
FILES=()

if [ "$TARGET" = "--all" ]; then
  while IFS= read -r f; do
    FILES+=("$f")
  done < <(find secoes -type f -name '*.tex' | sort)
elif [ -d "$TARGET" ]; then
  while IFS= read -r f; do
    FILES+=("$f")
  done < <(find "$TARGET" -type f -name '*.tex' | sort)
elif [ -f "$TARGET" ]; then
  FILES=("$TARGET")
else
  echo "[ERRO][slide-style-linter] Alvo nao encontrado: $TARGET" >&2
  exit 30
fi

if [ "${#FILES[@]}" -eq 0 ]; then
  echo "[ERRO][slide-style-linter] Nenhum arquivo .tex encontrado em: $TARGET" >&2
  exit 30
fi

echo "[INFO][slide-style-linter] Auditando ${#FILES[@]} arquivo(s) Beamer..."

python3 - "${FILES[@]}" << 'EOF'
import re
import sys

files = sys.argv[1:]

jargon_pattern = re.compile(
    r'\b(revolucion[aá]ri[oa]s?|divisor(?:es)? de [aá]guas?|crucia(?:l|is)|fundamental|'
    r'conflu[eê]ncia interdisciplinar|ecossistema din[aâ]mico|astron[oô]mic[oa]s?|'
    r'impressionante|paradigma transformador|vital|disruptiv[oa]s?|inovador sem precedentes)\b',
    re.IGNORECASE,
)

code_envs = ("vhdlcode", "ccode", "scriptcode", "lstlisting")

for target in files:
    with open(target, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    itemize_stack = []
    in_frame = False
    frame_start = 0
    frame_fragile = False
    in_code = False

    for idx, raw in enumerate(lines, 1):
        clean = re.sub(r'(?<!\\)%.*$', '', raw)

        if any(rf"\begin{{{env}}}" in clean for env in code_envs):
            if in_frame and not frame_fragile:
                print(f"[ERRO][slide-style-linter] {target}:{idx}: ambiente de codigo em frame sem [fragile] (frame aberto na linha {frame_start}).", file=sys.stderr)
                sys.exit(34)
            in_code = True
        if any(rf"\end{{{env}}}" in clean for env in code_envs):
            in_code = False

        m_frame = re.search(r'\\begin\{frame\}(\[[^\]]*\])?', clean)
        if m_frame:
            if in_frame:
                print(f"[ERRO][slide-style-linter] {target}:{idx}: \\begin{{frame}} aninhado sem \\end{{frame}} anterior.", file=sys.stderr)
                sys.exit(34)
            in_frame = True
            frame_start = idx
            opts = m_frame.group(1) or ""
            frame_fragile = "fragile" in opts

        if r'\end{frame}' in clean:
            if not in_frame:
                print(f"[ERRO][slide-style-linter] {target}:{idx}: \\end{{frame}} sem \\begin{{frame}} correspondente.", file=sys.stderr)
                sys.exit(34)
            in_frame = False
            frame_fragile = False

        if not in_code and re.search(r'[—–]', clean):
            print(f"[ERRO][slide-style-linter] {target}:{idx}: travessao Unicode proibido (— ou –):", file=sys.stderr)
            print(f"  > {raw.strip()}", file=sys.stderr)
            sys.exit(31)

        if r'\begin{itemize}' in clean:
            itemize_stack.append([idx, 0])
        elif itemize_stack:
            itemize_stack[-1][1] += len(re.findall(r'\\item\b', clean))
            if r'\end{itemize}' in clean:
                s_line, count = itemize_stack.pop()
                if count > 6:
                    print(f"[ERRO][slide-style-linter] {target}:{s_line}: bloco itemize com {count} itens (maximo: 6).", file=sys.stderr)
                    sys.exit(32)

        if not in_code:
            prose = re.sub(r'\\(cite|autocite|textcite|fullcite|label|fonte|includegraphics)\{[^}]*\}', '', clean)
            match = jargon_pattern.search(prose)
            if match:
                print(f"[ERRO][slide-style-linter] {target}:{idx}: jargao promocional proibido (\"{match.group(0)}\"):", file=sys.stderr)
                print(f"  > {raw.strip()}", file=sys.stderr)
                sys.exit(33)

    if in_frame:
        print(f"[ERRO][slide-style-linter] {target}:{frame_start}: \\begin{{frame}} sem \\end{{frame}} de fechamento.", file=sys.stderr)
        sys.exit(34)

print(f"[OK][slide-style-linter] {len(files)} arquivo(s) em conformidade (bullets <= 6, sem travessoes, sem jargoes, frames validos).")
EOF
