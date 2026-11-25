---
name: latex-build
description: Compilacao deterministica e nao interativa com latexmk isolando todos os artefatos em out/ com -jobname unico por secao.
---

# LaTeX Build

Automacao de compilacao LaTeX para `main.tex` e agregadores `secoes/<secao>/secao.tex` com isolamento completo em `out/` para builds paralelos sem colisao.

## Comandos Canonicos

```bash
# Compilar uma secao isolada em paralelo (gera out/<section_id>.pdf)
bash .agents/hooks/post-write-compile.sh 01_abertura

# Compilar todas as secoes isoladamente (sem exigir main.tex)
bash .agents/hooks/post-write-compile.sh sections

# Compilar documento global (inclui BibLaTeX/bibtex -> out/main.pdf)
bash .agents/hooks/post-write-compile.sh main

# Compilar main.tex + todas as 7 secoes
bash .agents/hooks/post-write-compile.sh all
```

## Restricoes

- Nunca executar compilacao interativa.
- Nunca gerar `.aux`, `.log`, `.nav`, `.snm`, `.toc` ou `.pdf` fora de `out/`.
- Sempre usar `-jobname=<section_id>` ao compilar `secoes/<section_id>/secao.tex` para impedir colisao de `secao.pdf`/`secao.aux` entre secoes paralelas.
