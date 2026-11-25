---
name: bib-validator
description: Verificar integridade referencial entre citacoes em secoes/*.tex e entradas em bib/referencias.bib.
---

# Bib Validator

Valida sincronia entre chaves citadas (`\cite`, `\autocite`, `\textcite`, `\fullcite`) em `secoes/*.tex` e entradas definidas em `bib/referencias.bib`.

## Verificacao Rapida

1. Extrair todas as chaves citadas em `secoes/*.tex`.
2. Extrair todas as entradas `@<tipo>{<chave>,` de `bib/referencias.bib`.
3. Reportar:
   - **Citacoes ausentes:** chaves usadas nos slides e inexistentes no `.bib` (falha critica).
   - **Entradas orfas:** chaves no `.bib` nao citadas nos slides (aviso se `99_conclusao.tex` nao usar `\nocite{*}`).
4. Confirmar compilacao limpa de `bibtex out/main` via `latexmk` quando `main.tex` e compilado.
