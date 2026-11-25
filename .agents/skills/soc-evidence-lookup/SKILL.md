---
name: soc-evidence-lookup
description: Extrair fatos, metricas HIL, enderecos e trechos de codigo exclusivamente da Camada Autoritativa de ../soc-proj sem contaminacao por specs obsoletas.
---

# SoC Evidence Lookup

Skill de recuperacao factual para o projeto Zynq-7010 (Digilent Cora Z7-10) + ESP32 auxiliar em `../soc-proj`.

## Protocolo de Consulta

1. **Ler primeiro:** `utils/memory/soc_proj_architecture_map.md` e `utils/memory/INDEX.md`.
2. **Aprofundar via `vivado-vitis-evidence`:** consultar fontes RTL/Tcl/C11 e relatorios `BENCHMARK_RESULTS.md` / `Matriz_de_Testes_e_Métricas.csv` conforme a tabela de roteamento do mapa arquitetural.
3. **Filtro de contexto:** nunca abrir PDFs externos pesados em `../soc-proj/docs/cora7z/` ou `../soc-proj/docs/esp32/`.

## Regras de Desambiguacao

- **Clock PS:** `650 MHz` (nunca `667 MHz`). **Pinos SPI:** `H15/T12/W15/F16` + `Y18` (nunca `G20/T10/V15`).
- **Trigger PMOD JA1:** `250 us` ativo-baixo (`main.c`, `BENCHMARK_RESULTS.md`), *lockout* `50 ms`, *gap* `30 ms`.
- **FPGA OOC (`BENCHMARK_RESULTS.md` §3.4):** `aes_accel_0` `2.764` LUTs / `2.274` FFs (nunca `3.410`/`2.150`), `lzss_accel_0` `667` LUTs / `457` FFs, `axi_quad_spi_0` `558` LUTs / `857` FFs / `1` BRAM; sistema completo `8.810` LUTs / `12.048` FFs / `9` BRAMs / `WNS = +0,551 ns`.
- **Secao 02 (`02_arquitetura_sistema`):** proibido citar `RLE`, `LZ4`, `ChaCha20`, `AXI DMA` ou `axis_accel_mux`.
