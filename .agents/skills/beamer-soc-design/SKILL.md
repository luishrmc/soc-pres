---
name: beamer-soc-design
description: Redigir e diagramar frames Beamer 16:9 em secoes/*.tex usando o estilo UFMG, listagens VHDL/C e diagramas TikZ PS/PL/BRAM/SPI.
---

# Beamer SoC Design

Guia de redacao modular de slides em LaTeX Beamer 16:9 para o projeto SoC Zynq-7010.

## Convencoes Estruturais

- Todo arquivo em `secoes/*.tex` deve iniciar com `\documentclass[../main.tex]{subfiles}`, `\begin{document}` e terminar com `\end{document}`.
- Secoes tematicas (`02` a `99`) iniciam com `\iniciarSecao[Rotulo Curto]{Titulo Completo}`.
- Todo frame tecnico deve incluir `\fonte{<referencia em ../soc-proj>}` no rodape.
- Frames com `vhdlcode`, `ccode` ou `scriptcode` exigem `\begin{frame}[fragile]`.

## Recursos Disponiveis em `config/estilo_seminario.sty`

- **Blocos:** `pontoschave`, `block`, `alertblock`, `exampleblock`, `bloco`.
- **Codigo:** `vhdlcode`, `ccode`, `scriptcode`, `\vhdlin{...}`, `\cin{...}`.
- **TikZ:** estilos `soc ps`, `soc pl`, `soc bram`, `soc esp32`, `soc caixa`, `soc dominio`, `soc seta`, `soc seta bidir`, `pics/bramdp`.
- **Figuras locais:** `figuras/cora7z_top.png`, `figuras/cora7z_soc_architecture.pdf` e SVGs/diagramas em `figuras/`.

## Limites de Densidade e Estilo

- Maximo de **6 bullets** por ambiente `itemize` (1 a 2 linhas por item).
- Proibido travessao Unicode (`—` ou `–`) em prosa e jargoes promocionais vazios.
- Negrito (`\textbf{}`) restrito a 1 ou 2 termos-ancora por item.
