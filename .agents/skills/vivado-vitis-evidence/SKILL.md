---
name: vivado-vitis-evidence
description: Extrair e validar evidencias tecnicas de scripts Tcl Vivado, relatorios de sintese/timing XC7Z010, CSRs RTL, firmware bare-metal Vitis C11 e licoes aprendidas de ../soc-proj.
---

# Vivado & Vitis Evidence Extraction

Skill especializada para interpretar artefatos reais de engenharia em `../soc-proj` sem executar builds pesados de Vivado ou Vitis.

## 1. Ponto de Entrada Obrigatorio

Consultar `utils/memory/soc_proj_architecture_map.md` antes de abrir qualquer fonte em `../soc-proj`.

## 2. Fontes Vivado (Hardware PL & Block Design)

- **`../soc-proj/cora7z/app/hw/scripts/configure_block_design.tcl`:**
  - PS7: `FCLK_CLK0 = 50 MHz` (`M_AXI_GP0` / `axi_quad_spi_0`), `FCLK_CLK1 = 100 MHz` (`lzss_accel_0`, `aes_accel_0`, `axi_bram_ctrl_*`, `bmg_*` Porta B, `ext_spi_clk`). *(Nota: o comentario na linha 9 cita 667 MHz; usar `650 MHz` conforme BSP/PMU em `README.md`.)*
  - `axi_quad_spi_0`: `USE_BOARD_FLOW=false`, `Master_mode=0`, `C_FIFO_DEPTH=256`, `spi_ss_i` conectado a `ss_i` e `spisel` (ADR-016).
  - EMIO GPIO: `PCW_EN_EMIO_GPIO=1`, `xlslice` `DIN_FROM=0` -> porta `esp32_trigger_o` (`Y18`).
  - Enderecos BD: `lzss_accel_0` `0x43C00000`, `aes_accel_0` `0x43C10000`, 4 BRAMs `0x40000000/2000` e `0x40010000/2000`.
- **`../soc-proj/cora7z/app/hw/scripts/build_bitstream.tcl`:**
  - Fluxo: `update_module_reference [get_ips *accel*]`, `validate_bd_design`, `synth_1`, `impl_1 -to_step write_bitstream`, `report_utilization`, `report_timing_summary`, `report_drc`, `write_hw_platform -fixed -include_bit -force`.
- **`../soc-proj/cora7z/app/hw/src/{compression/lzss_accel.vhdl,crypto/aes_accel.vhdl}`:**
  - Offsets CSR reais: `0x00` CTRL, `0x04` STATUS, `0x08` SRC_LEN, `0x0C` DST_LEN, `0x10` CYCLE_COUNT; em `aes_accel`: `0x14..0x20` `KEY_0..3`, `0x24..0x2C` `IV_0..2`, `0x30` `COUNTER_INIT`.
- **`../soc-proj/cora7z/test_results/BENCHMARK_RESULTS.md` (§3.4 & §5):**
  - Sistema completo (`XC7Z010`): `8.810` LUTs (`50,06%`), `12.048` FFs (`34,23%`), `9` BRAMs (`15,00%`), `0` DSPs, `WNS = +0,551 ns` @ `100 MHz`, `WHS = +0,008 ns`, `0/33.838` falhas.
  - OOC por IP: `aes_accel_0` (`2.764` LUTs, `2.274` FFs), `lzss_accel_0` (`667` LUTs, `457` FFs), `axi_quad_spi_0` (`558` LUTs, `857` FFs, `1` BRAM), `bmg_*` (`40` LUTs, `48` FFs, `8` BRAMs).
- **`figuras/comuns/soc_final_bd_*.pdf` (Vistas Reais do Block Design Vivado):**
  - Exportacoes vetoriais autenticas de `soc_final_bd_1` disponiveis para inclusao direta nos slides (ver `figuras/README.md`): `addressing_view` (enderecos AXI), `clock_and_reset_view` (dominios `50/100 MHz` e resets), `interface_view` (portas BRAM/AXI/SPI), `color_coded`, `grouping_and_no_loops`, `no_loops`, `reduce_jogs` e `default_view`/`soc_final_bd_1`.

## 3. Fontes Vitis / Firmware Bare-Metal C11 (PS)

- **`../soc-proj/cora7z/app/sw/src/pipeline/{main.c,pipeline_mgr.h,pipeline_mgr.c}`:**
  - Seguranca de barramento: `is_pl_programmed()` le `DEVCFG` (`0xF800700C` bit 2 `PCFG_DONE`).
  - Calibracao PMU: acesso CP15 a `PMCCNTR` @ `650 MHz` com subtracao de `28` ciclos (`calc_calibrated_cycles()`).
  - Nonce SEC-01: `pipeline_generate_frame_iv()` vincula `seq_id` aos 64 bits superiores do IV.
  - Trigger EMIO (`main.c`): pulso ativo-baixo de `250 us` em `PMOD JA1` (`Y18`) + buffer estatico `s_burst_buf[30]` para captura zero-drop (`60/60`).

## 4. Licoes Aprendidas Criticas (`../soc-proj/utils/memory/lessons.md`)

- `spisel`: `shield_spi` da placa travava `spisel='1'`; resolvido com portas discretas e `.cs_ena_pretrans=2` no ESP32.
- `bram_wait_r` (ADR-019): latencia sincrona de 1 ciclo na BRAM exigiu estados `*_WAIT` em `lzss_accel.vhdl`.
- Risco R9: busca sequencial na BRAM Porta B (`100 MHz`, `201k–745k` ciclos) + copia `M_AXI_GP0` (`50 MHz`) perde para `lzss_sw` em cache L1 (`32 KB`, `650 MHz`).
