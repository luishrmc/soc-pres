---
name: beamer-soc-design
description: Redigir e diagramar slides atomicos em secoes/<secao>/<NN>_<slug>.tex usando o estilo UFMG, listagens VHDL/C e diagramas TikZ.
---

# Beamer SoC Design

Guia de redacao modular por slide atomico em LaTeX Beamer 16:9 para o projeto SoC Zynq-7010.

## Convencoes Estruturais

- Cada pasta `secoes/<secao>/` possui um agregador `secao.tex` (`\documentclass[../../main.tex]{subfiles}`) que chama `\iniciarSecao` e inclui os slides via `\input{\subfix{secoes/<secao>/<NN>_<slug>}}`.
- Cada arquivo atomico `<NN>_<slug>.tex` contem apenas o(s) `\begin{frame}...\end{frame}` correspondente(s).
- Imagens de cada secao residem em `figuras/<secao>/` (e compartilhadas em `figuras/comuns/`), sendo resolvidas pelo `\graphicspath` de `secao.tex` com `\includegraphics{arquivo}`.
- Todo frame tecnico deve incluir `\fonte{...}` no rodape; frames com `vhdlcode`/`ccode`/`scriptcode` exigem `[fragile]`.

## Regras Especificas de Secao

- `02_arquitetura_sistema`: **proibida** qualquer mencao a historico descartado (`RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux`).
- `05_ferramenta_auxiliar_esp32`: maximo 2 slides enfatizando papel auxiliar de bancada.

## Limites de Densidade e Estilo

- Maximo de **6 bullets** por `itemize` (1 a 2 linhas por item).
- Proibido travessao Unicode (`—` ou `–`) em prosa e jargoes promocionais vazios.
