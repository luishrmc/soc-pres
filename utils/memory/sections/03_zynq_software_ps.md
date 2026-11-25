# Log Incremental da Secao: `03_zynq_software_ps`

- **Status:** `SKELETON_READY` (aguardando geracao completa via orquestrador)
- **Slides Alvo:** `01_orquestrador_pipeline_mgr.tex`, `02_instrumentacao_pmu_sec01.tex`, `03_modelos_referencia_sw.tex` (`S08`--`S10`)

## Decisoes de Layout
- Ordem causal (`UF-002`): apresentar PS antes de PL por gerenciar `PCFG_DONE`, CSRs e buffers BRAM.
- `S08`: `is_pl_programmed()` (`0xF800700C` bit 2), `axi_spi_receiver` (`0x41E00000`), `watchdog` e `ccode` `[fragile]`.
- `S09`: `PMCCNTR` (`650 MHz`, `28` ciclos subtraidos) + derivacao de IV `SEC-01` com `seq_id`.
- `S10`: `lzss_sw.c` (cache L1 `32 KB`) e `aes_ctr_sw.c` (NIST F.5.1) como linha de base C1 e oraculo bit-a-bit.

## Figuras Geradas / Alocadas
- `figuras/comuns/soc_final_bd_addressing_view.pdf` disponivel para apoio de enderecamento `M_AXI_GP0`.
- Avaliar diagrama vetorial PS -> CSR/BRAM em `figuras/03_zynq_software_ps/`.

## Pendencias de Revisao
- Enriquecer diagramacao visual e validar sincronia literal com `pipeline_mgr.h` e `main.c`.
- Executar ciclo completo (`PRE-FLIGHT` -> `MULTI-AGENT CONVERGENCE LOOP` -> `POST-SECTION RETRO`).
