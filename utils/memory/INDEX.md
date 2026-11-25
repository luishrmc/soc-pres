# Memory Index

Leia este arquivo e `GEMINI.md` antes de iniciar qualquer secao. Limite: 40 linhas.

## Estrutura

| Caminho | Finalidade | Responsavel |
|---|---|---|
| `decisions.md` | Registro append-only de decisoes da apresentacao (`PRES-ADR-NNN`) | `orchestrator-agent` |
| `lessons.md` | Erros recorrentes de LaTeX/hooks e solucoes (<= 80 linhas) | `orchestrator-agent` |
| `modules/<secao>.md` | Digest por secao Beamer (<= 60 linhas) | `slide-author-agent` |
| `handoff/<secao>.md` | Estado entre iteracoes (<= 50 linhas) | `slide-author-agent` |
| `episodes/<secao>.md` | Historico automatico de falhas (`loop-convergence-guard.sh`) | hook |

## Secoes Planejadas (DAG)

- `01_abertura`: Capa UFMG, agenda, motivacao e objetivos na Cora Z7-10 (`secoes/01_abertura.tex`)
- `02_arquitetura_e_evolucao`: Topologia PS/PL + ESP32, pivo ADR-012/017, Compress-then-Encrypt (`secoes/02_arquitetura_e_evolucao.tex`)
- `03_subssistemas_hw_sw`: VHDL-2008 (`lzss_accel`, `aes_accel`), C11 bare-metal e ESP32 (`secoes/03_subssistemas_hw_sw.tex`)
- `04_metodologia_e_resultados_hil`: Matriz ADR-020, resultados HIL `N=20`, FPGA XC7Z010, Risco R9 (`secoes/04_metodologia_e_resultados_hil.tex`)
- `99_conclusao`: Sintese comparativa, licoes aprendidas, trabalhos futuros e referencias (`secoes/99_conclusao.tex`)

## Handoffs Ativos

Nenhum (template inicializado e validado).
