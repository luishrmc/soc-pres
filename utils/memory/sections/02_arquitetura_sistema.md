# Log Incremental da Secao: `02_arquitetura_sistema`

- **Status:** `SKELETON_READY` (aguardando geracao completa via orquestrador)
- **Slides Alvo:** `01_pipeline_compress_encrypt.tex`, `02_topologia_zynq.tex`, `03_desacoplamento_bram.tex` (`S05`--`S07`)

## Decisoes de Layout
- **Corte obrigatorio (`UF-001`):** zero mencao a `RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux` ou LUTs pre-pivo.
- `S05` apresenta os algoritmos finais (`LZSS` 256/16 + `AES-128-CTR`) e os 4 cenarios `C1..C4`.
- `S06` integra vista real do Block Design Vivado (`soc_final_bd_color_coded.pdf` ou `grouping_and_no_loops.pdf`).
- `S07` ilustra desacoplamento via 4 BRAMs Dual-Port (`0x40000000/2000`, `0x40010000/2000`) e contrato 5 passos.

## Figuras Geradas / Alocadas
- `figuras/comuns/soc_final_bd_color_coded.pdf`, `figuras/comuns/soc_final_bd_interface_view.pdf`, `figuras/02_arquitetura_sistema/cora7z_top.png`.
- *Aviso:* `.svg` legados em `figuras/02_arquitetura_sistema/` contem `667 MHz`/`XSpiPs`; nao incluir diretamente.

## Pendencias de Revisao
- Substituir `cora7z_top.png` (marcacao WIP) por `soc_final_bd_color_coded.pdf` e/ou diagrama `.svg`+`.pdf` limpo em `figuras/02_arquitetura_sistema/`.
- Executar ciclo completo (`PRE-FLIGHT` -> `MULTI-AGENT CONVERGENCE LOOP` -> `POST-SECTION RETRO`).
