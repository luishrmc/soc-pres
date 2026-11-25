# Mapa Arquitetural Canonico de `../soc-proj` (`soc_proj_architecture_map.md`)

Base de conhecimento pre-indexada para consulta primaria dos agentes de `soc-pres` antes de abrir arquivos em `../soc-proj`. Todos os valores abaixo pertencem a **Camada Autoritativa pos-ADR-017/019/020** (estado final HIL verificado).

---

## 1. Mapa Estrutural de `../soc-proj`

| Caminho em `../soc-proj` | Finalidade | Status de Fidelidade |
|---|---|---|
| `README.md` | Visao geral, especificacoes fisicas, pinagem, matriz HIL | **Autoritativo** |
| `utils/plan/STATUS.md`, `Matriz_de_Testes_e_Métricas.csv`, `Riscos_e_Bloqueios.csv`, `Checklist_de_Entregaveis.csv` | Status final, matriz 12 celulas `N=20`, Risco R9 | **Autoritativo** |
| `cora7z/test_results/{TEST_PLAN.md,BENCHMARK_RESULTS.md,benchmark_matrix_consolidated.csv}` | Metodologia ADR-020, captura zero-drop, modelo de ciclos AES, OOC FPGA | **Autoritativo** |
| `utils/memory/{INDEX.md,decisions.md,lessons.md}` | ADRs 001..020 e licoes praticas de Vivado, Vitis, RTL e HIL | **Autoritativo** |
| `cora7z/app/hw/src/{compression/lzss_accel.vhdl,crypto/aes_accel.vhdl}` | RTL VHDL-2008 e mapa CSR exato (`0x00..0x30`) | **Autoritativo (fonte)** |
| `cora7z/app/hw/test/{tb_lzss_accel.vhdl,tb_aes_accel.vhdl}` | Testbenches VUnit/GHDL (`12/12 PASS`) | **Autoritativo (fonte)** |
| `cora7z/app/hw/scripts/{configure_block_design.tcl,build_bitstream.tcl}` | Integracao BD Vivado, sintese, bitstream e XSA | **Autoritativo (fonte)** |
| `cora7z/app/hw/utils/cora_z7_io.xdc` | Pinagem fisica real (`H15/T12/W15/F16`, `Y18`) | **Autoritativo (fonte)** |
| `cora7z/app/sw/src/{pipeline/main.c,pipeline/pipeline_mgr.{c,h},comms/{axi_spi_receiver.c,spi_frame.h},compression/lzss_sw.c,crypto/aes_ctr_sw.c}` | Firmware C11, `PCFG_DONE`, PMU (`28` ciclos), `250 us` pulse, `s_burst_buf[30]` | **Autoritativo (fonte)** |
| `esp32/main/{main.c,spi_injector_master.c,trigger_gpio.c,spi_frame.h}`, `esp32/scripts/{generate_telemetry.py,telemetry_profiles.py}` | Injetor ESP32 (`2 MHz`, `GPIO 32`, `seed=42`, `1035 B`) | **Autoritativo (fonte)** |
| `docs/hw/{LZSS_ACCEL.md,AES_ACCEL.md}`, `docs/sw/*.md`, `docs/esp32/SPI_INJECTOR.md`, `docs/adr/0020-fixed-1024b-benchmark-payload.md` | Documentacao de modulos (atentar a ressalvas abaixo) | **Apoio (conferir fonte)** |
| `utils/TEMA.md`, `docs/SYSTEM_ARCHITECTURE.md`, `docs/hw/INTERFACES.md`, `utils/memory/modules/{rle,lz4,chacha20,aes_ctr}_engine.md` | Proposta inicial (`RLE/LZ4/ChaCha20/AXI DMA`), pinos `G20/T10/V15`, `667 MHz` | **Historico / Superado** |

> **Desambiguacao Obrigatoria:** usar `650 MHz` PS (nao `667 MHz` de `SYSTEM_ARCHITECTURE.md`/`LZSS_SW.md`/`configure_block_design.tcl` comentario); usar pinos `H15/T12/W15/F16` + `Y18` (nao `G20/T10/V15` de `INTERFACES.md`); usar pulso EMIO `250 us` (`main.c`, nao `30 ms`); usar `0x08 SRC_LEN`, `0x0C DST_LEN`, `0x10 CYCLE_COUNT` e `0x14..0x30` Key/IV/Counter (nao diagrama antigo de `AES_ACCEL.md` §2); usar OOC `aes_accel_0` `2.764 LUTs / 2.274 FFs` e speedup Cenario 3 `1,17x–1,24x` (nao `3.410/2.150`, `1,56x` ou `829` ciclos).

---

## 2. Tabela Mestre de Arquitetura (Digilent Cora Z7-10 `xc7z010clg400-1` + ESP32 Auxiliar)

- **Dominios de Clock:** PS Cortex-A9 Core 0 `650 MHz` (`XPAR_CPU_CORE_CLOCK_FREQ_HZ`, `512 MB` DDR3, `32 KB` L1 I/D, `512 KB` L2); `FCLK_CLK0` = `50 MHz` (`M_AXI_GP0` e `axi_quad_spi_0` `s_axi_aclk`); `FCLK_CLK1` = `100 MHz` (`lzss_accel_0`, `aes_accel_0`, `axi_bram_ctrl_*`, `bmg_*` Porta B, `axi_quad_spi_0/ext_spi_clk`); SPI externo = `2 MHz` (Modo 0, suporte ate `25 MHz`).
- **Mapa de Enderecos (`M_AXI_GP0`):**
  - `DEVCFG` (`PCFG_DONE`): `0xF800700C` bit 2 (`is_pl_programmed()` obrigatorio antes de MMIO em PL).
  - `axi_quad_spi_0`: `0x41E00000` (escravo Modo 0, FIFO `256 B`, `spisel` ligado a `spi_ss_i` com `PULLUP` — ADR-016).
  - `bmg_lzss_in`: `0x40000000` (`8 KB`, `2048 B` uteis) | `bmg_lzss_out`: `0x40002000` (`8 KB`, `2048 B` uteis).
  - `bmg_aes_in`: `0x40010000` (`8 KB`, `2048 B` uteis) | `bmg_aes_out`: `0x40012000` (`8 KB`, `2048 B` uteis).
  - `lzss_accel_0`: `0x43C00000` (`0x00` CTRL, `0x04` STATUS, `0x08` SRC_LEN, `0x0C` DST_LEN, `0x10` CYCLE_COUNT).
  - `aes_accel_0`: `0x43C10000` (`0x00..0x10` comuns + `0x14..0x20` KEY_0..3, `0x24..0x2C` IV_0..2, `0x30` COUNTER_INIT).
- **Pinagem Fisica (`cora_z7_io.xdc`):** `spi_sck_i=H15` (`J7.3` / `ESP32 GPIO 18`), `spi_mosi_i=T12` (`J7.4` / `GPIO 23`), `spi_miso_o=W15` (`J7.1` / `GPIO 19`), `spi_ss_i=F16` (`J7.5` / `GPIO 5`), `esp32_trigger_o=Y18` (`PMOD JA1` / `GPIO 32`, pulso `250 us` ativo-baixo, *lockout* `50 ms`, *gap* `30 ms`).
- **Contrato `TelemetryFrame` (`1035 B`, ADR-020):** `[0]` `0xA5` | `[1]` `0x02` | `[2..3]` `BE16 seq_id` | `[4..5]` `BE16 len=1024` | `[6..7]` `0x0000` pad | `[8..1031]` `1024 B` (`64 x 16 B` `<IhhhhHH`) | `[1032..1033]` `CRC-16-CCITT (0x1021)` | `[1034]` `0x5A` EOF.

---

## 3. Matriz Consolidada HIL (`N = 20` / Perfil, `60/60` Quadros Zero-Drop, `28` Ciclos PMU Subtraidos)

| Cenario | Perfil | Latencia (ms) | Ciclos PMU (Media +- DP) | Ciclos PL (100 MHz) | CR (%) | Vazao (MB/s) | Speedup |
|---|---|---:|---:|---:|---:|---:|---:|
| **C1: SW/SW** | Quiescent | 3,796 | 2.467.688 +- 57.741 | 0 | +55,7% | 0,26 | 1,00x |
| **C1: SW/SW** | Dynamic | 10,188 | 6.621.969 +- 20.324 | 0 | +2,5% | 0,10 | 1,00x |
| **C1: SW/SW** | Chaotic | 12,907 | 8.389.708 +- 15.135 | 0 | -12,6% | 0,08 | 1,00x |
| **C2: PL LZSS + SW AES** | Quiescent | 5,990 | 3.893.369 +- 89.334 | 200.972 | +55,7% | 0,16 | 0,63x |
| **C2: PL LZSS + SW AES** | Dynamic | 16,112 | 10.473.009 +- 36.864 | 573.622 | +2,5% | 0,06 | 0,63x |
| **C2: PL LZSS + SW AES** | Chaotic | 20,563 | 13.366.113 +- 21.824 | 744.661 | -12,6% | 0,05 | 0,63x |
| **C3: SW LZSS + PL AES** | Quiescent | **3,068** | **1.994.017 +- 53.850** | **668** | +55,7% | **0,32** | **1,24x** |
| **C3: SW LZSS + PL AES** | Dynamic | **8,579** | **5.576.620 +- 22.043** | **1.452** | +2,5% | **0,11** | **1,19x** |
| **C3: SW LZSS + PL AES** | Chaotic | **11,039** | **7.175.201 +- 10.382** | **1.679** | -12,6% | **0,09** | **1,17x** |
| **C4: PL/PL** | Quiescent | 5,260 | 3.419.303 +- 85.605 | 201.639 | +55,7% | 0,19 | 0,72x |
| **C4: PL/PL** | Dynamic | 14,503 | 9.427.015 +- 37.116 | 575.075 | +2,5% | 0,07 | 0,70x |
| **C4: PL/PL** | Chaotic | 18,694 | 12.150.877 +- 17.163 | 746.340 | -12,6% | 0,05 | 0,69x |

- **Fidelidade de Compressao (`1024 B`):** Quiescent `440–469 B` (`453,20 +- 8,58 B`, `+55,74%`), Dynamic `994–1005 B` (`998,00 +- 3,24 B`, `+2,54%`), Chaotic `1152–1154 B` (`1153,40 +- 0,68 B`, `-12,64%`); *max match* `<= 15 B <= 16 B` (paridade 100% SW/PL).
- **Modelo AES PL:** $C_{\text{PL, AES}}(N) = 10 + 11\lceil N/16\rceil + 3\lceil N/4\rceil$.
- **Sintese FPGA (`XC7Z010-1CLG400C`):**
  - Sistema completo (`soc_final_bd_1_wrapper`, C4): `8.810 / 17.600` LUTs (`50,06%`), `12.048 / 35.200` FFs (`34,23%`), `9 / 60` BRAMs (`15,00%` = `8 RAMB36E1 + 2 RAMB18E1`), `0 / 80` DSPs, `0` latches, `0 / 33.838` falhas, `clk_fpga_1 (100 MHz): WNS = +0,551 ns / WHS = +0,008 ns`, `clk_fpga_0 (50 MHz): WNS = +8,299 ns / WHS = +0,024 ns`.
  - OOC por IP: `aes_accel_0` (`2.764` LUTs / `2.274` FFs), `lzss_accel_0` (`667` LUTs / `457` FFs), `axi_quad_spi_0` (`558` LUTs / `857` FFs / `1` BRAM), `bmg_*` (`40` LUTs / `48` FFs / `8` BRAMs). C2 e C3 isolados: `Pending`.

---

## 4. Indice de Roteamento Rapido ("Para escrever sobre X -> ler arquivo Y")

| Assunto da Secao / Slide | Arquivos Canonicos em `../soc-proj` |
|---|---|
| Escopo academico, requisitos e alternativas | `utils/Projeto Final.pdf`, `utils/TEMA.md`, `README.md` |
| Arquitetura final, pinos, clocks e BRAM Dual-Port | `README.md`, `cora7z/app/hw/utils/cora_z7_io.xdc`, `cora7z/app/hw/scripts/configure_block_design.tcl`, `utils/memory/decisions.md` (ADRs 012, 016, 017) |
| Firmware PS (`pipeline_mgr`, `PCFG_DONE`, PMU, SEC-01, modelos SW) | `cora7z/app/sw/src/pipeline/{main.c,pipeline_mgr.h,pipeline_mgr.c}`, `docs/sw/{PIPELINE_MGR,AXI_SPI_RECEIVER,LZSS_SW,AES_CTR_SW}.md` |
| RTL `lzss_accel` (ADR-019) e `aes_accel`, VUnit e sintese | `cora7z/app/hw/src/{compression/lzss_accel.vhdl,crypto/aes_accel.vhdl}`, `docs/hw/{LZSS_ACCEL,AES_ACCEL}.md`, `cora7z/app/hw/scripts/build_bitstream.tcl`, `cora7z/test_results/BENCHMARK_RESULTS.md` (§3.4, §5) |
| Ferramenta auxiliar ESP32, carga ADR-020 e captura zero-drop | `docs/esp32/SPI_INJECTOR.md`, `cora7z/app/sw/src/comms/spi_frame.h`, `cora7z/test_results/{TEST_PLAN,BENCHMARK_RESULTS}.md` (§2.2, §2.4) |
| Resultados HIL `N=20`, Cenario 3 e analise causal Risco R9 | `utils/plan/{Matriz_de_Testes_e_Métricas.csv,STATUS.md,Riscos_e_Bloqueios.csv}`, `cora7z/test_results/{BENCHMARK_RESULTS.md,benchmark_matrix_consolidated.csv}` |
| Licoes aprendidas e armadilhas de toolchain | `utils/memory/lessons.md`, `BENCHMARK_RESULTS.md` (§4) |
