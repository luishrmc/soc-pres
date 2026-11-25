# Decision Log da Apresentacao (`soc-pres`, append-only)

Formato: `PRES-ADR-NNN | data | escopo | decisao | justificativa`.

## PRES-ADR-001 | 2026-11-25 | setup | Estrutura modular na raiz (`main.tex`, `config/`, `secoes/`, `figuras/`, `bib/`) com build isolado em `out/`
Justificativa: simplifica caminhos relativos via `\subfix{...}` tanto na compilacao global (`main.tex`) quanto na compilacao isolada de cada secao, mantendo todo artefato auxiliar em `out/`.

## PRES-ADR-002 | 2026-11-25 | dados | Camada Autoritativa unica em `../soc-proj` pos-ADR-017/019/020
Justificativa: `README.md`, `STATUS.md`, `Matriz_de_Testes_e_Métricas.csv`, `BENCHMARK_RESULTS.md`, `cora_z7_io.xdc` e `decisions.md` prevalecem sobre documentos intermediarios ou historicos.

## PRES-ADR-003 | 2026-11-25 | estilo | Identidade visual UFMG adaptada para VHDL-2008, C11 e diagramas TikZ PS/PL/BRAM/SPI
Justificativa: preserva o tema `Darmstadt` e paleta institucional de `../../seminar`, substituindo macros especificas de CDC/SystemVerilog por ambientes e cores funcionais do projeto SoC Zynq-7010.

## PRES-ADR-004 | 2026-11-25 | arquitetura | Modularizacao em 7 pastas de secao (`secao.tex` + 21 slides atomicos) com isolamento paralelo
Justificativa: viabiliza orquestracao simultanea por secao (`--section`, `-jobname=<sec>` em `out/`, escopo de escrita disjunto em `boundary-guard.py`), ordena o nucleo tecnico em Zynq PS -> Zynq PL -> ESP32 auxiliar, move sintese FPGA para Secao 04 e proibe historico descartado na Secao 02.
