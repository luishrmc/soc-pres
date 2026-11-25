---
name: soc-evidence-lookup
description: Extrair fatos, metricas HIL, enderecos e trechos de codigo exclusivamente da Camada Autoritativa de ../soc-proj sem contaminacao por specs obsoletas.
---

# SoC Evidence Lookup

Skill de recuperacao factual para o projeto Zynq-7010 (Digilent Cora Z7-10) + ESP32 em `../soc-proj`.

## Hierarquia de Fontes

1. **Camada Autoritativa (Estado Final HIL Verificado):**
   - `../soc-proj/README.md`: parametros fisicos (`650 MHz` PS, `100 MHz` PL, `50 MHz` AXI, `28` ciclos PMU), pinagem J7/JA1, mapa BRAM e tabela consolidada dos 4 cenarios (`N=20` @ `1024 B`).
   - `../soc-proj/utils/plan/STATUS.md`: estado final (`30/30` quadros sem perdas) e confirmacao empirica do Risco R9.
   - `../soc-proj/utils/plan/Matriz_de_Testes_e_Métricas.csv`: valores exatos de latencia, ciclos ARM PMU, ciclos PL HW, razao de compressao, vazao e recursos FPGA (`8.810` LUTs, `12.048` FFs, `9` BRAMs).
   - `../soc-proj/utils/memory/decisions.md`: ADRs 012, 016, 017, 018, 019 e 020.
   - `../soc-proj/cora7z/app/hw/utils/cora_z7_io.xdc`: pinagem fisica autoritativa (`H15`, `T12`, `W15`, `F16`, `Y18`).
   - `../soc-proj/docs/hw/{LZSS_ACCEL,AES_ACCEL}.md`, `../soc-proj/docs/sw/*.md`, `../soc-proj/docs/esp32/SPI_INJECTOR.md`, `../soc-proj/docs/adr/0020-fixed-1024b-benchmark-payload.md`.
2. **Camada Historica (Apenas Contexto de Evolucao):**
   - `../soc-proj/utils/TEMA.md` e `../soc-proj/docs/SYSTEM_ARCHITECTURE.md` (proposta inicial RLE/LZ4 + ChaCha20 + AXI DMA, superada pelo ADR-017).

## Regras de Desambiguacao

- **Clock PS:** Usar `650 MHz` (BSP `APU_FREQ`, `README.md` / `STATUS.md`). Documentos intermediarios que citam `667 MHz` refletem valor nominal anterior a calibracao final.
- **Pinos SPI:** Usar `H15` (SCK), `T12` (MOSI), `W15` (MISO), `F16` (SS_N) no Header J7 e `Y18` (trigger EMIO) no PMOD JA1 (`cora_z7_io.xdc`). Nunca usar pinos antigos (`G20`, `T10`, `V15`).
- **Carga de Benchmark:** Usar `1024 B` (`1035 B` on-wire com cabecalho 8 B, CRC-16 2 B e EOF `0x5A`) conforme ADR-020.
- **Recursos Isolados (Cenarios 2 e 3):** Marcados como `Pending` na matriz; nao inventar valores.
