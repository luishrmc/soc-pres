# Registro Canonico de Feedback do Usuario (`user_feedback_log.md`)

Toda correcao ou preferencia expressa pelo usuario durante a construcao das secoes deve ser registrada aqui imediatamente no `POST-SECTION RETRO & FEEDBACK GATE` e lida obrigatoriamente no `PRE-FLIGHT MEMORY GATE` das secoes seguintes.

| ID | Secao Origem | Correcao / Preferencia do Usuario | Regra Operacional Derivada | Escopo |
|---|---|---|---|---|
| `UF-001` | `02_arquitetura_sistema` | Cortar integralmente evolucao historica e opcoes descartadas da Secao 02. | Proibir mencoes a `RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux` e contagens pre-pivo na Secao 02; apresentar apenas a arquitetura final (`LZSS + AES-128-CTR + BRAM Dual-Port`). | `Especifico (Secao 02)` |
| `UF-002` | `03` / `04` / `05` | Ordenar nucleo tecnico como Zynq PS -> Zynq PL -> ESP32 auxiliar, com sintese FPGA na Secao 04 e ESP32 limitado a 1-2 slides. | Explicar PS antes de PL por dependencia de inicializacao/CSRs; alocar ocupacao e timing XC7Z010 em `04_zynq_hardware_pl`; restringir ESP32 a 2 slides de estimulo auxiliar na Secao 05. | `Global` |
| `UF-003` | `Global` | Modularizar `secoes/` e `figuras/` em 7 pastas espelhadas com arquivos atomicos por slide. | Cada worker edita apenas `secoes/<sec>/**`, `figuras/<sec>/**` e `utils/memory/sections/<sec>.md`, preservando `figuras/comuns/` e `secao.tex`. | `Global` |
| `UF-004` | `Global` | Manter apenas PDFs finais na raiz de `out/`, segregando auxiliares, logs e estados. | Compilar exclusivamente via `post-write-compile.sh` (`-emulate-aux-dir -outdir=out -auxdir=out/aux`) e inspecionar `out/aux/<sec>.log` para garantir zero `Overfull \hbox/\vbox`. | `Global` |
| `UF-005` | `02` / `03` / `04` | Aproveitar as 9 vistas vetoriais do Block Design Vivado em `figuras/comuns/soc_final_bd_*.pdf`. | Priorizar `\includegraphics{soc_final_bd_<vista>.pdf}` quando adequado ao tema da secao antes de desenhar diagramas redundantes. | `Global` |
