# Organizacao Modular de Figuras (`figuras/`)

Os ativos visuais espelham exatamente a hierarquia das 7 pastas de `secoes/`, permitindo que cada `slide-author-agent` e `diagram-svg-agent` gere ou edite figuras apenas no subdiretorio da sua secao sem conflitos paralelos.

| Diretorio | Secao / Papel | Ativos Atuais |
|---|---|---|
| `figuras/comuns/` | Ativos compartilhados (somente leitura aos workers) | 9 vistas vetoriais do Block Design Vivado (`soc_final_bd_*.pdf`) |
| `figuras/01_abertura/` | Secao 01 (`S01`--`S04`) | `.gitkeep` |
| `figuras/02_arquitetura_sistema/` | Secao 02 (`S05`--`S07`) | `cora7z_top.png`, `cora7z_soc_architecture.pdf`, `system_topology.svg`*, `system_execution_domains.svg`*, `bram_store_forward_contract.svg`* |
| `figuras/03_zynq_software_ps/` | Secao 03 (`S08`--`S10`) | `.gitkeep` |
| `figuras/04_zynq_hardware_pl/` | Secao 04 (`S11`--`S14`) | `bram_pipeline_architecture.svg`* |
| `figuras/05_ferramenta_auxiliar_esp32/` | Secao 05 (`S15`--`S16`) | `.gitkeep` |
| `figuras/06_metodologia_e_resultados_hil/` | Secao 06 (`S17`--`S19`) | `benchmark_matrix_flow.svg`* |
| `figuras/99_conclusao/` | Secao 99 (`S20`--`S21`) | `.gitkeep` |

## Vistas do Block Design Vivado em `figuras/comuns/`

Todos os arquivos abaixo sao PDFs vetoriais diretamente incluiveis via `\includegraphics{<arquivo>.pdf}` a partir de qualquer secao (via `\graphicspath` de `secao.tex`):

| Arquivo em `figuras/comuns/` | Foco Visual da Vista | Uso Recomendado |
|---|---|---|
| `soc_final_bd_1.pdf` / `soc_final_bd_default_view.pdf` | Visao padrao completa do Block Design (`soc_final_bd_1`) | Visao geral / referencia completa |
| `soc_final_bd_color_coded.pdf` | Blocos e conexoes diferenciados por cor | Secao 02 (`02_topologia_zynq.tex`) |
| `soc_final_bd_grouping_and_no_loops.pdf` | Agrupamento limpo sem lacos de roteamento | Secao 02 / Secao 04 (visao estrutural limpa) |
| `soc_final_bd_interface_view.pdf` | Interfaces AXI, BRAM Porta A/B e portas SPI discretas | Secao 02 (`03_desacoplamento_bram.tex`) e Secao 04 |
| `soc_final_bd_clock_and_reset_view.pdf` | Dominios `FCLK_CLK0` (50 MHz), `FCLK_CLK1` (100 MHz) e resets | Secao 02 / Secao 04 (`04_sintese_ocupacao_fpga.tex`) |
| `soc_final_bd_addressing_view.pdf` | Mapa de enderecamento AXI (`0x40000000`, `0x41E00000`, `0x43C0/10000`) | Secao 02 / Secao 03 (`01_orquestrador_pipeline_mgr.tex`) |
| `soc_final_bd_no_loops.pdf` | Topologia sem lacos visuais | Alternativa de layout limpo |
| `soc_final_bd_reduce_jogs.pdf` | Roteamento com desvios minimizados | Alternativa de layout compacto |

> *Nota sobre os `.svg` importados de `../soc-proj/utils/imgs/` (`*`):* o compilador `pdflatex` nao embute `.svg` diretamente e esses arquivos trazem rotulos pre-ADR-020 (`667 MHz`, `256/512 B`, `XSpiPs`, `Zero-DMA`). Para diagramas novos ou anotados nos slides, acionar `diagram-svg-agent` para gerar `.svg` + `.pdf` em `figuras/<sec>/`.
