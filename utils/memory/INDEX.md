# Memory Index

Leia este arquivo e `GEMINI.md` antes de iniciar qualquer secao. Limite: 40 linhas.

## Estrutura

| Caminho | Finalidade | Responsavel |
|---|---|---|
| `decisions.md` | Registro append-only de decisoes (`PRES-ADR-NNN`) | `orchestrator-agent` |
| `lessons.md` | Erros recorrentes de LaTeX/hooks e solucoes (<= 80 linhas) | `orchestrator-agent` |
| `modules/<sec>.md` | Digest por secao Beamer (<= 60 linhas) | `slide-author-agent` |
| `handoff/<sec>.md` | Estado entre iteracoes da secao (<= 50 linhas) | `slide-author-agent` |
| `episodes/<sec>.md` | Historico automatico de falhas (`loop-convergence-guard.sh`) | hook |

## Secoes Ativas (7 Pastas, 21 Slides)

- `01_abertura`: `secao.tex` + `01_capa..04_alternativas_roteiro.tex` (S01-S04)
- `02_arquitetura_sistema`: `secao.tex` + `01_pipeline..03_desacoplamento_bram.tex` (S05-S07)
- `03_zynq_software_ps`: `secao.tex` + `01_orquestrador..03_modelos_referencia_sw.tex` (S08-S10)
- `04_zynq_hardware_pl`: `secao.tex` + `01_coprocessador_lzss..04_sintese_ocupacao_fpga.tex` (S11-S14)
- `05_ferramenta_auxiliar_esp32`: `secao.tex` + `01_injetor_spi..02_sincronismo_hil_zerodrop.tex` (S15-S16)
- `06_metodologia_e_resultados_hil`: `secao.tex` + `01_fidelidade..03_analise_causal_gargalos.tex` (S17-S19)
- `99_conclusao`: `secao.tex` + `01_sintese_licoes_futuro..02_referencias.tex` (S20-S21)

## Handoffs Ativos

Arquitetura refatorada (aguardando atualizacao de `main.tex` para build global).
