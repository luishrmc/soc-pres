---
name: slide-visual-review
description: Auditoria adversarial somente leitura de densidade visual, legibilidade e fidelidade factual dos slides contra ../soc-proj.
---

# Slide Visual Review

Rubrica utilizada pelo `design-critic-agent` no Outer Loop.

## Checklist de Auditoria

1. **Fidelidade Factual (`../soc-proj`):**
   - Metricas HIL (`N=20`, `1024 B`) conferem 1:1 com `Matriz_de_Testes_e_Métricas.csv` e `README.md`.
   - Recursos FPGA (`8.810` LUTs, `12.048` FFs, `9` BRAMs, `WNS = +0,551 ns`) conferem exatamente.
   - `RLE`, `LZ4`, `ChaCha20` e `AXI DMA` estao rotulados apenas como escopo inicial substituido pelo ADR-017.
2. **Legibilidade e Layout Beamer 16:9:**
   - Nenhum bloco `itemize` excede 6 itens.
   - Zero `Overfull \hbox` critico no log de compilacao em `out/`.
   - Tabelas e diagramas usam fontes legiveis (`\scriptsize`/`\footnotesize`) sem sobreposicao visual.
3. **Estilo Linguistico:**
   - Texto tecnico conciso em portugues; zero travessoes (`—`/`–`) em prosa; zero adjetivos promocionais vazios.
   - Presenca de `\fonte{...}` em todos os slides tecnicos.

## Saida Obrigatoria

Emitir JSON estrito com `verdict` (`"APPROVE"` ou `"REJECT"`), `critical_findings` e `minor_suggestions`.
