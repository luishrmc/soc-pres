# Lessons Learned (`soc-pres`)

Registro conciso de armadilhas tecnicas e correcoes (maximo 80 linhas).

- **Desambiguacao `../soc-proj`:** `docs/hw/INTERFACES.md` e `utils/memory/modules/interfaces.md` listam pinos antigos (`G20/T10/V15`); usar `cora_z7_io.xdc` (`H15/T12/W15/F16`, `Y18`). Offsets CSR reais em `lzss_accel.vhdl`/`aes_accel.vhdl` sao `0x08` `SRC_LEN`, `0x0C` `DST_LEN`, `0x10` `CYCLE_COUNT` e `0x14..0x30` para chave/IV/contador.
- **Clock PS, pulso EMIO e OOC FPGA:** usar `650 MHz` (nao `667 MHz`), pulso EMIO de `250 us` (`main.c`, nao `30 ms`), speedup Cenario 3 `1,17x` a `1,24x` (nao `1,56x`/`829` ciclos) e OOC `aes_accel_0` `2.764` LUTs / `2.274` FFs (`BENCHMARK_RESULTS.md` §3.4, nao `3.410`/`2.150`).
- **Compilacao paralela com `secao.tex`:** todos os agregadores chamam-se `secao.tex`; sempre invocar `latexmk -jobname=<sec_id> -outdir=out -auxdir=out` via `post-write-compile.sh` e referenciar imagens com `\subfix{figuras/...}` ou `\DefinirCaminhoLogo{\subfix{config/logo}}`.
