---
name: svg-slide-diagram
description: Gerar diagramas vetoriais .svg sob demanda com identidade visual UFMG/Beamer 16:9 e converter automaticamente para .pdf vetorial em figuras/<secao>/.
---

# SVG Slide Diagram Generator

Skill para criacao de diagramas arquiteturais, FSMs RTL, quadros de protocolo SPI, linhas do tempo HIL e graficos comparativos em formato vetorial `.svg` + `.pdf` para inclusao limpa via `\includegraphics`.

## 1. Identidade Visual Obrigatoria (Paleta de `config/estilo_seminario.sty`)

Todo diagrama gerado deve respeitar a paleta institucional e funcional definida em `config/estilo_seminario.sty`:
- **Institucional UFMG:** `UFMGPrimario` `#C80019`, `UFMGSecundario` `#BA181B`, `UFMGEscuro` `#660708`, `UFMGQuaternario` `#F5F3F4`, `UFMGTerciario` `#B1A7A6`, `UFMGImportante` `#161A1D`, `UFMGGrafite` `#42464A`, `UFMGDiretiva` `#006E78`.
- **Dominios SoC:**
  - `PS (Cortex-A9)`: borda `#184E77`, fundo `#ECF4FA`
  - `PL (Artix-7)`: borda `#1B663E`, fundo `#ECF7F0`
  - `BRAM Dual-Port`: borda `#945C00`, fundo `#FDF6E8`
  - `ESP32 Auxiliar`: borda `#BA181B`, fundo `#F5F3F4`
- **Tipografia e Proporcao Beamer 16:9:** usar familia sans-serif (`Sans` / `Latin Modern Sans`) e monoespacada para enderecos/sinais; fundo claro (`#FFFFFF` ou `#F5F3F4`) com alto contraste (nao usar fundo escuro que destoe dos slides Beamer); tracos `1.5px–2.5px` em proporcao compativel com quadro 16:9 (ex.: `960x540` ou `800x450` pt).

## 2. Pipeline Deterministico de Geracao `.svg` -> `.pdf`

Salvar sempre ambos os artefatos em `figuras/<section_id>/`:
1. **`<nome>.svg`**: arquivo-fonte vetorial limpo (gerado via `pycairo` `cairo.SVGSurface` ou XML SVG valido).
2. **`<nome>.pdf`**: PDF vetorial correspondente para inclusao sem erros no `pdflatex` via `\includegraphics{<nome>.pdf}`.

Metodos verificados no ambiente atual:
- **Preferencial (programatico via `pycairo`):** desenhar com uma funcao `draw(ctx)` compartilhada gravando simultaneamente `cairo.SVGSurface("<nome>.svg", w, h)` e `cairo.PDFSurface("<nome>.pdf", w, h)`.
- **Conversao de `.svg` standalone:** quando o `.svg` for escrito em XML, converter com `google-chrome --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="<nome>.pdf"` (usando HTML wrapper com `@page { size: <w>px <h>px; margin: 0; }`) ou renderizar via script `pycairo`.

## 3. Regras de Qualidade

- Zero numeros estimados ou obsoletos (`667 MHz`, `3.410`, `1,56x`, `G20/T10/V15`).
- Rotulos curtos, legiveis ao escalar no slide (`>= 11 pt` equivalentes), sem sobreposicao de setas ou caixas.
- Nunca gravar na raiz de `figuras/` ou em `figuras/comuns/` durante fluxo paralelo de secao: gravar exclusivamente em `figuras/<section_id>/`.
