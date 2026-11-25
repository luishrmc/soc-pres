---
name: memory-protocol
description: Manter memoria acumulativa em utils/memory/ (INDEX.md, soc_proj_architecture_map.md, user_feedback_log.md, lessons.md, sections/, modules/, handoff/, decisions.md, episodes/) com gates pre e pos-secao.
---

# Memory Protocol (Aprendizado Acumulativo)

Protocolo obrigatorio de memoria incremental para evitar repeticao de erros e preservar preferencias do usuario entre secoes.

## 1. Estrutura em `utils/memory/`

- `INDEX.md` (<= 40 linhas): visao geral da memoria e secoes ativas.
- `soc_proj_architecture_map.md`: mapa canonico pre-indexado de `../soc-proj`.
- `user_feedback_log.md` (<= 120 linhas): correcoes/preferencias do usuario (`UF-NNN`) e regras derivadas.
- `lessons.md` (<= 80 linhas): licoes categorizadas em `(a) LaTeX/Beamer`, `(b) Diagramas SVG/TikZ`, `(c) Rigor Tecnico`, `(d) Controle de Escopo`.
- `sections/<NN_secao>.md` (<= 80 linhas): status, decisoes de layout, figuras geradas e pendencias da secao.
- `decisions.md`: registro append-only (`PRES-ADR-NNN`).
- `modules/<secao>.md` (<= 60 linhas) e `handoff/<secao>.md` (<= 50 linhas): estado intra-secao.
- `episodes/<secao>.md`: historico de falhas gravado pelo `loop-convergence-guard.sh`.

## 2. Gates Obrigatorios de Execucao

1. **`PRE-FLIGHT MEMORY GATE` (antes de `content-retriever` ou `slide-author`):**
   - Ler obrigatoriamente `utils/memory/soc_proj_architecture_map.md`, `utils/memory/lessons.md`, `utils/memory/user_feedback_log.md` e os logs `utils/memory/sections/*.md` das secoes ja concluidas.
2. **`MULTI-AGENT CONVERGENCE LOOP`:**
   - Iterar `content-retriever` -> `slide-author` <-> `diagram-svg-agent` -> `technical-fidelity-critic` + `design-critic` -> `compiler` + hooks (`post-write-compile.sh`, `slide-style-linter.sh`, `fact-sync-check.py`) ate `0` erros, `0` `Overfull \hbox/\vbox` e `APPROVE` unanime.
3. **`POST-SECTION RETRO & FEEDBACK GATE` (ao concluir secao ou receber feedback do usuario):**
   - Registrar novas licoes tecnicas/visuais em `utils/memory/lessons.md`.
   - Registrar feedback literal e regra derivada em `utils/memory/user_feedback_log.md` (em execucao paralela, consolidar de forma serializada no fechamento).
   - Atualizar `utils/memory/sections/<NN_secao>.md` com status, decisoes de layout, figuras geradas e pendencias.
   - Validar com `python3 .agents/hooks/memory-check.py`.
