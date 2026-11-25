# Memory Index

Leia `GEMINI.md`, `soc_proj_architecture_map.md`, `lessons.md` e `user_feedback_log.md` antes de iniciar qualquer secao. Limite: 40 linhas.

## Estrutura de Memoria Acumulativa

| Caminho | Finalidade | Responsavel |
|---|---|---|
| `soc_proj_architecture_map.md` | Mapa canonico pre-indexado de `../soc-proj` | `orchestrator-agent` |
| `user_feedback_log.md` | Feedbacks do usuario e regras derivadas (lido no pre-flight) | `orchestrator-agent` |
| `lessons.md` | Licoes acionaveis em 4 categorias (<= 80 linhas) | `orchestrator-agent` |
| `decisions.md` | Registro append-only de decisoes (`PRES-ADR-NNN`) | `orchestrator-agent` |
| `sections/<sec>.md` | Log incremental por secao (status, layout, figuras, pendencias) | `orchestrator-agent` |
| `modules/<sec>.md` | Digest por secao (<= 60 linhas) | `slide-author-agent` |
| `handoff/<sec>.md` | Estado intra-secao entre iteracoes (<= 50 linhas) | `slide-author-agent` |
| `episodes/<sec>.md` | Historico automatico de falhas (`loop-convergence-guard.sh`) | hook |

## Secoes Ativas (`utils/memory/sections/*.md`)

- `01_abertura` (`S01-S04`) | `02_arquitetura_sistema` (`S05-S07`) | `03_zynq_software_ps` (`S08-S10`)
- `04_zynq_hardware_pl` (`S11-S14`) | `05_ferramenta_auxiliar_esp32` (`S15-S16`) | `06_metodologia_e_resultados_hil` (`S17-S19`)
- `99_conclusao` (`S20-S21`)
