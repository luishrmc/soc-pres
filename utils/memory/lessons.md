# Lessons Learned (`soc-pres`)

Registro acionavel de licoes tecnicas e visuais (maximo 80 linhas). Lido no `PRE-FLIGHT MEMORY GATE`.

## (a) LaTeX/Beamer & Layout Visual
- **Compilacao modular `subfiles` + `out/`:** usar `post-write-compile.sh <sec>` (`-emulate-aux-dir -jobname=<sec>`) e `\input{\subfix{<slide>}}` em `secao.tex`; `subfix` dentro de subfile e relativo a propria pasta.
- **Resolucao de figuras por secao:** `\graphicspath` em `secao.tex` inclui `config/`, `figuras/<sec>/` e `figuras/comuns/`; usar `\includegraphics{arquivo.pdf}` sem caminho absoluto.
- **Overflow e tabelas:** tabelas longas em colunas estreitas (`05_ferramenta_auxiliar_esp32`) causam `Overfull \hbox`; usar colunas `p{...}` e checar `Overfull \hbox` e `Overfull \vbox` em `out/aux/<sec>.log`.
- **Estilo:** maximo 6 bullets por `itemize`, zero travessoes Unicode (`—`/`–`) em prosa, zero jargoes promocionais, e `[fragile]` obrigatorio em frames com `vhdlcode`/`ccode`/`scriptcode`.

## (b) Diagramas SVG/TikZ & Identidade Institucional
- **Pipeline vetorial no host:** `rsvg-convert`/`inkscape` nao estao instalados; gerar `.svg` + `.pdf` vetorial com `pycairo` (`SVGSurface` + `PDFSurface`) ou converter `.svg` com `google-chrome --headless --no-pdf-header-footer --print-to-pdf`.
- **SVGs legados (`../soc-proj/utils/imgs/`):** trazem rotulos pre-ADR-020 (`667 MHz`, `256/512 B`, `XSpiPs`, `Zero-DMA`) e `pdflatex` nao embute `.svg`; nunca inclui-los diretamente — substituir por TikZ ou novo `.svg`+`.pdf` com paleta clara UFMG.
- **Vistas Vivado prontas:** usar `figuras/comuns/soc_final_bd_*.pdf` (`color_coded`, `interface_view`, `clock_and_reset_view`, `addressing_view`, `grouping_and_no_loops`).

## (c) Rigor Tecnico & Rastreabilidade `../soc-proj`
- **Desambiguacoes criticas:** PS = `650 MHz` (nao `667 MHz`); pinos SPI = `H15/T12/W15/F16` + `Y18` (nao `G20/T10/V15`); pulso EMIO = `250 us` (`main.c`, nao `30 ms`); PMU = `28` ciclos; payload = `1024 B` (`1035 B` no fio).
- **CSRs e FPGA:** offsets reais em VHDL/C sao `0x08` `SRC_LEN`, `0x0C` `DST_LEN`, `0x10` `CYCLE_COUNT` e `0x14..0x30` Key/IV/Counter; OOC `aes_accel_0` = `2.764` LUTs / `2.274` FFs (nao `3.410`/`2.150`); Cenario 3 = `1,17x–1,24x` (nao `1,56x`/`829` ciclos).
- **Interpretacao R9:** `lzss_accel` perde para `lzss_sw` (`0,63x` C2, `0,69x–0,72x` C4) por busca sequencial em BRAM Porta B (`100 MHz`) + copia `M_AXI_GP0` (`50 MHz`).

## (d) Controle de Escopo por Secao
- **`02_arquitetura_sistema`:** proibida qualquer mencao a `RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux` ou LUTs pre-pivo.
- **`05_ferramenta_auxiliar_esp32`:** estritamente 2 slides como ferramenta auxiliar de bancada; proibido detalhar `ESP-IDF`/`240 MHz`/`GPIO 32` fora da Secao 05.
