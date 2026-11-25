# Log Incremental da Secao: `05_ferramenta_auxiliar_esp32`

- **Status:** `SKELETON_READY` (aguardando geracao completa via orquestrador)
- **Slides Alvo:** `01_injetor_spi_carga_adr020.tex`, `02_sincronismo_hil_zerodrop.tex` (`S15`--`S16`)

## Decisoes de Layout
- **Limite estrito (`UF-002`):** exatamente 2 slides enfatizando papel auxiliar de estimulo de bancada (sem protagonismo).
- `S15`: `TelemetryFrame` `1035 B`, payload `1024 B` (`64 x 16 B` `<IhhhhHH`), `seed=42`, VSPI `2 MHz`, perfis `Quiescent/Dynamic/Chaotic`.
- `S16`: superacao de `40%` de perda (`stride=2/3`) com pulso `250 us` em `Y18`, `GPIO 32` (*lockout* `50 ms`), ACK `< 50 us` e `s_burst_buf[30]` (`60/60` quadros).

## Figuras Geradas / Alocadas
- Nenhuma figura gerada em `figuras/05_ferramenta_auxiliar_esp32/` ainda; gerar diagrama do quadro `1035 B` e linha do tempo zero-drop via `diagram-svg-agent`.

## Pendencias de Revisao
- Garantir zero `Overfull \hbox` nas tabelas e diagramas de quadro SPI.
- Executar ciclo completo (`PRE-FLIGHT` -> `MULTI-AGENT CONVERGENCE LOOP` -> `POST-SECTION RETRO`).
