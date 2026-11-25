---
name: soc-evidence-lookup
description: Extrair fatos, metricas HIL, enderecos e trechos de codigo exclusivamente da Camada Autoritativa de ../soc-proj sem contaminacao por specs obsoletas.
---

# SoC Evidence Lookup

Skill de recuperacao factual para o projeto Zynq-7010 (Digilent Cora Z7-10) + ESP32 auxiliar em `../soc-proj`.

## Hierarquia de Fontes

1. **Camada Autoritativa (Estado Final HIL Verificado):**
   - `../soc-proj/README.md`, `../soc-proj/utils/plan/STATUS.md`, `../soc-proj/utils/plan/Matriz_de_Testes_e_Métricas.csv`, `../soc-proj/utils/plan/Riscos_e_Bloqueios.csv`.
   - `../soc-proj/cora7z/test_results/{TEST_PLAN.md,BENCHMARK_RESULTS.md,benchmark_matrix_consolidated.csv}` (inclui OOC FPGA §3.4 e captura zero-drop §2.4).
   - `../soc-proj/utils/memory/decisions.md` (ADRs 012, 016, 017, 018, 019 e 020).
   - `../soc-proj/cora7z/app/hw/utils/cora_z7_io.xdc` (pinagem `H15/T12/W15/F16` e `Y18`).
   - `../soc-proj/docs/hw/{LZSS_ACCEL,AES_ACCEL}.md`, `../soc-proj/docs/sw/*.md`, `../soc-proj/docs/esp32/SPI_INJECTOR.md`, `../soc-proj/docs/adr/*.md`.
   - Fontes RTL/C11 (`lzss_accel.vhdl`, `aes_accel.vhdl`, `pipeline_mgr.h`, `main.c`) como prova final de offsets CSR (`0x00..0x30`) e pulso EMIO (`250 us`).

## Regras de Desambiguacao

- **Clock PS:** `650 MHz` (nunca `667 MHz`). **Pinos SPI:** `H15/T12/W15/F16` + `Y18` (nunca `G20/T10/V15`).
- **Trigger PMOD JA1:** `250 us` ativo-baixo (`main.c`, `BENCHMARK_RESULTS.md`), com *lockout* de `50 ms` e *inter-frame gap* de `30 ms`.
- **FPGA OOC (`BENCHMARK_RESULTS.md` §3.4):** `aes_accel_0` `2.764` LUTs / `2.274` FFs (nunca `3.410`/`2.150`), `lzss_accel_0` `667` LUTs / `457` FFs, `axi_quad_spi_0` `558` LUTs / `857` FFs / `1` BRAM; sistema completo `8.810` LUTs / `12.048` FFs / `9` BRAMs / `WNS = +0,551 ns`.
- **Secao 02 (`02_arquitetura_sistema`):** proibido citar `RLE`, `LZ4`, `ChaCha20`, `AXI DMA` ou `axis_accel_mux`.
