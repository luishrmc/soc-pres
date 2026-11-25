# Log Incremental da Secao: `04_zynq_hardware_pl`

- **Status:** `SKELETON_READY` (aguardando geracao completa via orquestrador)
- **Slides Alvo:** `01_coprocessador_lzss.tex`, `02_coprocessador_aes.tex`, `03_verificacao_vunit.tex`, `04_sintese_ocupacao_fpga.tex` (`S11`--`S14`)

## Decisoes de Layout
- `S11`: `lzss_accel.vhdl` (`0x43C00000`), janela 256/16 e correcao `bram_wait_r` (ADR-019) em `vhdlcode` `[fragile]`.
- `S12`: `aes_accel.vhdl` (`0x43C10000`), 10 rodadas, `11` ciclos/bloco, `GF(2^8)` sem DSPs, cauda `1154 B` (`bram_out_we="0011"`).
- `S13`: tabela `booktabs` de verificacao VUnit/GHDL (`12/12 PASS`), `vhdl-lint`, `c-lint` e mocks C11.
- `S14`: sintese `XC7Z010` migrada para Secao 04 (`8.810` LUTs, `12.048` FFs, `9` BRAMs, `WNS = +0,551 ns` + OOC `2.764/667/558` LUTs).

## Figuras Geradas / Alocadas
- `figuras/comuns/soc_final_bd_clock_and_reset_view.pdf`, `figuras/comuns/soc_final_bd_interface_view.pdf`.
- Avaliar diagrama vetorial `.svg`+`.pdf` de datapath/FSM e barras de utilizacao OOC em `figuras/04_zynq_hardware_pl/`.

## Pendencias de Revisao
- Conferir offsets CSR `0x00..0x30` diretamente nos `.vhdl` e substituir o `.svg` legado se necessario.
- Executar ciclo completo (`PRE-FLIGHT` -> `MULTI-AGENT CONVERGENCE LOOP` -> `POST-SECTION RETRO`).
