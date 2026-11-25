# Log Incremental da Secao: `06_metodologia_e_resultados_hil`

- **Status:** `SKELETON_READY` (aguardando geracao completa via orquestrador)
- **Slides Alvo:** `01_fidelidade_compressao.tex`, `02_matriz_experimental_hil.tex`, `03_analise_causal_gargalos.tex` (`S17`--`S19`)

## Decisoes de Layout
- `S17`: fidelidade de compressao (`+55,74%`, `+2,54%`, `-12,64%`, *max match* `<= 15 B <= 16 B`, folga BRAM `2048 B`).
- `S18`: matriz 12 celulas (`N=20`), destacando Cenario 3 (`1,24x` / `1,19x` / `1,17x`) e explicitando C2 (`0,63x`) e C4 (`0,69x–0,72x`).
- `S19`: analise causal AES $10 + 11\lceil N/16\rceil + 3\lceil N/4\rceil$ vs. Risco R9 (`201k–745k` ciclos PL, `>96%` latencia C4, $\Delta\text{CPU}/\Delta\text{PL} \approx 15{,}6\times$).

## Figuras Geradas / Alocadas
- Gerar graficos vetoriais `.svg`+`.pdf` comparativos (latencia ms / speedup C1..C4) em `figuras/06_metodologia_e_resultados_hil/` via `diagram-svg-agent` (nao usar `benchmark_matrix_flow.svg` legado com `667 MHz`).

## Pendencias de Revisao
- Blindar contra vies interpretativo (veto `technical-fidelity-critic-agent`).
- Executar ciclo completo (`PRE-FLIGHT` -> `MULTI-AGENT CONVERGENCE LOOP` -> `POST-SECTION RETRO`).
