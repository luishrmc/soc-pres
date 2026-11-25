# Lessons Learned (`soc-pres`)

Registro conciso de armadilhas tecnicas e correcoes (maximo 80 linhas).

- **Desambiguacao `../soc-proj`:** `docs/hw/INTERFACES.md` e `utils/memory/modules/interfaces.md` ainda listam pinos antigos (`G20/T10/V15`) e DMA/ChaCha20 do ADR-008; sempre consultar `cora_z7_io.xdc` (`H15/T12/W15/F16`, `Y18`) e `README.md`.
- **Clock PS e metricas HIL:** usar `650 MHz` (BSP `APU_FREQ`) e matriz final `N=20` @ `1024 B` (`1,17x` a `1,24x` no Cenario 3), evitando numeros intermediarios (`667 MHz`, `1,56x`, `829` ciclos) de documentos anteriores ao ADR-020.
- **Compilacao com `subfiles` + `out/`:** executar sempre `latexmk -cd -outdir=... -auxdir=...` (via `post-write-compile.sh` ou `.vscode/settings.json`) para que `\subfix{...}` resolva caminhos e o `bibtex` encontre `out/main.aux`.
