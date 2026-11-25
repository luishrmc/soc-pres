# Organizacao Modular de Figuras (`figuras/`)

Os ativos visuais espelham exatamente a hierarquia das 7 pastas de `secoes/`, permitindo que cada `slide-author-agent` gere ou edite figuras apenas no subdiretorio da sua secao sem conflitos paralelos.

| Diretorio | Secao / Papel | Ativos Atuais |
|---|---|---|
| `figuras/comuns/` | Ativos compartilhados (somente leitura aos workers) | `.gitkeep` (logos/capa ficam em `config/`) |
| `figuras/01_abertura/` | Secao 01 (`S01`--`S04`) | `.gitkeep` |
| `figuras/02_arquitetura_sistema/` | Secao 02 (`S05`--`S07`) | `cora7z_top.png`, `cora7z_soc_architecture.pdf`, `system_topology.svg`*, `system_execution_domains.svg`*, `bram_store_forward_contract.svg`* |
| `figuras/03_zynq_software_ps/` | Secao 03 (`S08`--`S10`) | `.gitkeep` |
| `figuras/04_zynq_hardware_pl/` | Secao 04 (`S11`--`S14`) | `bram_pipeline_architecture.svg`* |
| `figuras/05_ferramenta_auxiliar_esp32/` | Secao 05 (`S15`--`S16`) | `.gitkeep` |
| `figuras/06_metodologia_e_resultados_hil/` | Secao 06 (`S17`--`S19`) | `benchmark_matrix_flow.svg`* |
| `figuras/99_conclusao/` | Secao 99 (`S20`--`S21`) | `.gitkeep` |

> *Nota sobre os `.svg` importados de `../soc-proj/utils/imgs/`:* o compilador `pdflatex` nao embute `.svg` diretamente e esses arquivos trazem rotulos pre-ADR-020 (`667 MHz`, `256/512 B`, `XSpiPs`, `Zero-DMA`). Para uso nos slides finais, preferir diagramas nativos em TikZ/PGFPlots ou exportar versoes atualizadas em `.pdf`/`.png` dentro do respectivo diretorio `figuras/<sec>/`.
