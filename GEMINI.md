# Diretrizes do Sistema: Apresentação SoC Zynq-7010 (`soc-pres`)

Este repositório hospeda a apresentação técnica em LaTeX Beamer (16:9) do projeto final de Sistemas em Chip (SoC) desenvolvido em `../soc-proj`, estruturada em **7 pastas de seção** com **arquivos atômicos por slide** e **aprendizado incremental acumulativo** entre seções.

---

## 1. Mapa do Workspace

| Caminho | Finalidade | Propriedade / Proteção |
|---|---|---|
| `main.tex` | Documento raiz Beamer 16:9 (`\subfile{secoes/<sec>/secao}`) e bibliografia | Protegido (`ALLOW_PROTECTED=1`) |
| `config/` | `00_config.tex`, `estilo_seminario.sty`, `logo.png`, `logo_ufmg.png`, `capa.png` | Protegido |
| `secoes/<sec>/` | 7 módulos: `01_abertura`, `02_arquitetura_sistema`, `03_zynq_software_ps`, `04_zynq_hardware_pl`, `05_ferramenta_auxiliar_esp32`, `06_metodologia_e_resultados_hil`, `99_conclusao` | Escrita isolada por `<sec>` (`slide-author-agent`) |
| `secoes/<sec>/secao.tex` | Agregador `subfiles` da seção (compilação isolada em `out/<sec>.pdf`) | Escopo da seção `<sec>` |
| `secoes/<sec>/<NN>_<slug>.tex` | Arquivo atômico por slide (`21` slides no total: `S01`–`S21`) | Escopo da seção `<sec>` |
| `figuras/` | Subdiretórios espelhando as 7 seções (`figuras/<sec>/`) + `figuras/comuns/` (`soc_final_bd_*.pdf`, `README.md`) | Escrita isolada em `figuras/<sec>/` (`diagram-svg` / `slide-author`) |
| `bib/referencias.bib` | Base bibliográfica BibLaTeX/BibTeX (edição serializada) | Serializado na consolidação |
| `utils/memory/` | `INDEX.md`, `soc_proj_architecture_map.md`, `user_feedback_log.md`, `lessons.md`, `sections/*.md`, `decisions.md`, `modules/`, `handoff/`, `episodes/` | `orchestrator-agent` / hooks |
| `.agents/` | Manifesto (`v3.0.0`), agentes, skills e hooks determinísticos | Protegido (`manifest.json`) |
| `out/` | PDFs finais na raiz (`main.pdf`, `<sec>.pdf`), auxiliares em `out/aux/`, logs em `out/logs/` e estados em `out/state/` | `compiler-agent` |

---

## 2. Protocolo de Leitura e Fonte da Verdade (`../soc-proj`)

1. **Entrada Primária Obrigatória (`PRE-FLIGHT MEMORY GATE`):** antes de abrir qualquer arquivo em `../soc-proj` ou editar slides, ler `utils/memory/soc_proj_architecture_map.md`, `utils/memory/INDEX.md`, `utils/memory/lessons.md`, `utils/memory/user_feedback_log.md` e os logs `utils/memory/sections/*.md` das seções já concluídas.
2. **Hierarquia de Decisão:**
   - Instrução explícita do usuário e regras registradas em `user_feedback_log.md`;
   - Camada Autoritativa de `../soc-proj` (`README.md`, `STATUS.md`, `Matriz_de_Testes_e_Métricas.csv`, `BENCHMARK_RESULTS.md`, `TEST_PLAN.md`, ADRs 012–020, `cora_z7_io.xdc`, fontes RTL/C/Tcl);
   - Invariantes de estilo Beamer e cortes temáticos deste `GEMINI.md`.
3. **Filtro de Contexto:** nunca ler datasheets externos pesados em `../soc-proj/docs/cora7z/` (`UG585.pdf`, `ds187-*.pdf`, manuais Digilent) nem `../soc-proj/docs/esp32/*.pdf`.
4. **Desambiguação obrigatória:** usar `650 MHz` para o Cortex-A9 PS (não `667 MHz`), pinos `H15/T12/W15/F16` + `Y18` (não `G20/T10/V15`), pulso EMIO `250 us` (`main.c`), payload `1024 B` (ADR-020), speedup Cenário 3 `1,17x` a `1,24x` (não `1,56x` ou `829` ciclos) e OOC `aes_accel_0` `2.764` LUTs / `2.274` FFs (não `3.410`/`2.150`).
5. **Regras temáticas de seção:**
   - `02_arquitetura_sistema`: **proibida** qualquer menção a histórico descartado (`RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux`, contagens pré-pivô).
   - `05_ferramenta_auxiliar_esp32`: estritamente `2` slides enfatizando papel auxiliar de bancada (proibido protagonismo do ESP32 fora da Seção 05).

---

## 3. Orquestração Incremental e Loop em 3 Gates por Seção

Cada seção executa obrigatoriamente os 3 gates abaixo (com isolamento `--section <sec>`):

1. **`PRE-FLIGHT MEMORY GATE`:**
   - `pre-task-audit.sh --section <sec>` (snapshot em `out/state/boundary_snapshot_<sec>.json`);
   - Leitura obrigatória de `soc_proj_architecture_map.md`, `lessons.md`, `user_feedback_log.md` e `sections/*.md` concluídos.
2. **`MULTI-AGENT CONVERGENCE LOOP`:**
   - `content-retriever-agent` (`soc-evidence-lookup` + `vivado-vitis-evidence`) $\rightarrow$ `slide-author-agent` $\leftrightarrow$ `diagram-svg-agent` (`svg-slide-diagram`, `.svg` + `.pdf` em `figuras/<sec>/`);
   - Inner Loop determinístico: `boundary-guard.py`, `slide-style-linter.sh`, `fact-sync-check.py`, `post-write-compile.sh <sec>` (`compiler-agent`) até **0 erros**, **0 `Overfull \hbox/\vbox`** em `out/aux/<sec>.log`;
   - Outer Loop adversarial (`read-only`): `technical-fidelity-critic-agent` (poder de veto anti-desvio) + `design-critic-agent` até aprovação unânime.
3. **`POST-SECTION RETRO & FEEDBACK GATE`:**
   - Atualizar `utils/memory/sections/<sec>.md`, consolidar novas lições em `utils/memory/lessons.md`, registrar correções/preferências em `utils/memory/user_feedback_log.md`, validar com `python3 .agents/hooks/memory-check.py` e pausar no **Gate Humano**.

- **Arquivos compartilhados serializados:** `main.tex`, `bib/referencias.bib`, `figuras/comuns/**`, `utils/memory/INDEX.md`, `soc_proj_architecture_map.md`, `user_feedback_log.md`, `decisions.md` e `lessons.md`.

---

## 4. Topologia Multiagente (`Gemini 4 Hydrogen`)

| Agente | Thinking Level | Papel | Escrita Autorizada |
|---|---|---|---|
| `orchestrator-agent` | `HIGH` | Coordena os 3 gates, memória acumulativa, convergência (`N <= 5`) e Gate Humano | `utils/memory/` (nunca edita `.tex`) |
| `content-retriever-agent` | `LOW/MEDIUM` | Extrai evidências de `../soc-proj` via `soc_proj_architecture_map.md` e skills Vivado/Vitis | Nenhuma (`read-only`) |
| `slide-author-agent` | `HIGH` | Redige slides atômicos em `secoes/<sec>/<NN>_<slug>.tex` | `secoes/<sec>/**`, `figuras/<sec>/**`, `modules/<sec>.md`, `handoff/<sec>.md` |
| `diagram-svg-agent` | `MEDIUM/HIGH` | Gera diagramas `.svg` + conversão vetorial `.pdf` com paleta UFMG | `figuras/<sec>/**` |
| `technical-fidelity-critic-agent` | `HIGH` | Revisor adversarial com poder de veto contra desvios numéricos/escopo de `../soc-proj` | Nenhuma (`read-only`) |
| `design-critic-agent` | `HIGH` | Revisor adversarial de densidade visual, legibilidade e narrativa Beamer | Nenhuma (`read-only`) |
| `compiler-agent` | `LOW` | Compila com `-emulate-aux-dir -jobname=<sec>` em `out/` | `out/**` |

---

## 5. Comandos Canônicos e Invariantes

```bash
bash .agents/hooks/pre-task-audit.sh --section 01_abertura
python3 .agents/hooks/boundary-guard.py check --agent slide-author-agent --section 01_abertura
bash .agents/hooks/slide-style-linter.sh secoes/01_abertura
python3 .agents/hooks/fact-sync-check.py secoes/01_abertura
bash .agents/hooks/post-write-compile.sh 01_abertura
bash .agents/hooks/post-write-compile.sh all
bash .agents/hooks/loop-convergence-guard.sh 01_abertura 1 NONE
python3 .agents/hooks/memory-check.py
```

- **Idioma:** texto dos slides, agentes, skills e hooks em **português** (identificadores de código, sinais e ADRs originais preservados).
- **Fidelidade Factual:** zero números inventados; zero histórico descartado na Seção 02; zero desvio interpretativo sobre Risco R9 ou protagonismo do ESP32.
- **Isolamento de Build:** todo artefato auxiliar e PDF reside exclusivamente em `out/`.
- **Estilo Beamer:** máximo de `6` bullets por `itemize`, zero travessões Unicode (`—`/`–`) em prosa e zero jargões promocionais vazios.
- **Fronteira e Segurança Git:** nunca editar fora de `soc-pres`; nunca executar `git commit` automático, `git reset --hard`, `git clean -fd` ou `--no-verify`.
