---
name: latex-build
description: Compilacao deterministica e nao interativa com latexmk isolando todos os artefatos auxiliares e PDFs em out/.
---

# LaTeX Build

Automacao de compilacao LaTeX para `main.tex` e `secoes/*.tex` com isolamento completo em `out/`.

## Comandos Canonicos

```bash
# Compilar apresentacao completa + secoes
bash .agents/hooks/post-write-compile.sh all

# Compilar apenas documento global (inclui BibLaTeX/bibtex)
bash .agents/hooks/post-write-compile.sh main

# Compilar subfile isolado
bash .agents/hooks/post-write-compile.sh secoes/01_abertura.tex
```

## Analise de Logs

Inspecionar `out/*.log` para:
- Erros fatais (`!` ou `-file-line-error`).
- Warnings de referencia/citacao indefinida (`Reference ... undefined`, `Citation ... undefined`).
- Contagem e severidade de `Overfull \hbox` / `Overfull \vbox`.

## Restricoes

- Nunca executar compilacao interativa.
- Nunca gerar `.aux`, `.log`, `.nav`, `.snm`, `.toc` ou `.pdf` fora de `out/`.
