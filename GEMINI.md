# Diretrizes do Sistema: Apresentação SoC Zynq-7010 (`soc-pres`)

Este repositório hospeda a apresentação técnica em LaTeX Beamer (16:9) do projeto final de Sistemas em Chip (SoC) desenvolvido em `../soc-proj`, estruturada em **7 pastas de seção** com **arquivos atômicos por slide** para permitir orquestração paralela sem conflitos de escrita.

---

## 1. Mapa do Workspace

| Caminho | Finalidade | Propriedade / Proteção |
|---|---|---|
| `main.tex` | Documento raiz Beamer 16:9 (`\subfile{secoes/<sec>/secao}`) e bibliografia | Protegido (`ALLOW_PROTECTED=1`) |
| `config/` | `00_config.tex`, `estilo_seminario.sty`, `logo.png`, `logo_ufmg.png`, `capa.png` | Protegido |
| `secoes/<sec>/` | 7 módulos: `01_abertura`, `02_arquitetura_sistema`, `03_zynq_software_ps`, `04_zynq_hardware_pl`, `05_ferramenta_auxiliar_esp32`, `06_metodologia_e_resultados_hil`, `99_conclusao` | Escrita isolada por `<sec>` (`slide-author-agent`) |
| `secoes/<sec>/secao.tex` | Agregador `subfiles` da seção (permite compilação isolada em `out/<sec>.pdf`) | Escopo da seção `<sec>` |
| `secoes/<sec>/<NN>_<slug>.tex` | Arquivo atômico por slide (`21` slides no total: `S01`–`S21`) | Escopo da seção `<sec>` |
| `figuras/` | Subdiretórios espelhando as 7 seções (`figuras/<sec>/`) + `figuras/comuns/` (`README.md`) | Escrita isolada em `figuras/<sec>/`; `comuns/` serializado |
| `bib/referencias.bib` | Base bibliográfica BibLaTeX/BibTeX (edição serializada) | Serializado na consolidação |
| `utils/memory/` | Memória persistente: `INDEX.md`, `decisions.md`, `lessons.md`, `modules/`, `handoff/`, `episodes/` | `orchestrator-agent` / hooks |
| `.agents/` | Manifesto, definições de agentes, skills e hooks determinísticos | Protegido (`manifest.json`) |
| `out/` | Diretório isolado para PDFs e artefatos auxiliares (`-jobname=<sec>`) | `compiler-agent` |

---

## 2. Hierarquia de Decisão e Fonte da Verdade (`../soc-proj`)

1. **Instrução explícita do usuário.**
2. **Camada Autoritativa de `../soc-proj` (Estado Final HIL Verificado):**
   - `../soc-proj/README.md`, `../soc-proj/utils/plan/{STATUS.md,Matriz_de_Testes_e_Métricas.csv,Checklist_de_Entregaveis.csv,Riscos_e_Bloqueios.csv}`
   - `../soc-proj/cora7z/test_results/{TEST_PLAN.md,BENCHMARK_RESULTS.md,benchmark_matrix_consolidated.csv}`
   - `../soc-proj/utils/memory/{INDEX.md,decisions.md,lessons.md}` (ADRs 012, 016, 017, 018, 019 e 020)
   - `../soc-proj/cora7z/app/hw/utils/cora_z7_io.xdc` e fontes RTL/C (`lzss_accel.vhdl`, `aes_accel.vhdl`, `pipeline_mgr.h`, `main.c`)
   - `../soc-proj/docs/hw/{LZSS_ACCEL,AES_ACCEL}.md`, `../soc-proj/docs/sw/*.md`, `../soc-proj/docs/esp32/SPI_INJECTOR.md`, `../soc-proj/docs/adr/0020-fixed-1024b-benchmark-payload.md`
3. **Invariantes de estilo Beamer e regras de corte por seção deste `GEMINI.md`.**
4. **Desambiguação obrigatória:** usar `650 MHz` para o Cortex-A9 PS (não `667 MHz`), pinos `H15/T12/W15/F16` + `Y18` (não `G20/T10/V15`), pulso EMIO `250 us` (`main.c`), payload `1024 B` (ADR-020), speedup Cenário 3 `1,17x` a `1,24x` (não `1,56x` ou `829` ciclos) e OOC `aes_accel_0` `2.764` LUTs / `2.274` FFs (não `3.410`/`2.150`).
5. **Regras temáticas de seção:**
   - `02_arquitetura_sistema`: **proibida** qualquer menção a histórico descartado (`RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux`, contagens pré-pivô).
   - `05_ferramenta_auxiliar_esp32`: estritamente `2` slides enfatizando papel auxiliar de bancada.

---

## 3. Orquestração Paralela Livre de Conflitos

Cada seção pode ser conduzida por um `orchestrator-agent` dedicado em paralelo:
- **Snapshot e fronteira isolados:** `--section <sec>` grava `out/boundary_snapshot_<sec>.json` e restringe escritas a `secoes/<sec>/**`, `figuras/<sec>/**`, `utils/memory/modules/<sec>.md` e `utils/memory/handoff/<sec>.md`.
- **Compilação isolada:** `post-write-compile.sh <sec>` usa `-jobname=<sec>` em `out/`, gerando `out/<sec>.pdf` e `out/<sec>.log` sem colisão de `secao.pdf`/`secao.aux`.
- **Arquivos compartilhados serializados:** `main.tex`, `bib/referencias.bib`, `utils/memory/INDEX.md`, `decisions.md` e `lessons.md` nunca são editados concorrentemente por workers de seção.

---

## 4. Topologia Multiagente (`Gemini 4 Hydrogen`)

| Agente | Thinking Level | Papel | Escrita Autorizada |
|---|---|---|---|
| `orchestrator-agent` | `HIGH` | Coordena seção/DAG, memória, convergência (`N <= 5`) e Gate Humano | `utils/memory/` (nunca edita `.tex`) |
| `content-retriever-agent` | `LOW/MEDIUM` | Extrai fatos e métricas da Camada Autoritativa de `../soc-proj` | Nenhuma (`read-only`) |
| `slide-author-agent` | `HIGH` | Redige slides atômicos em `secoes/<sec>/<NN>_<slug>.tex` | `secoes/<sec>/**`, `modules/<sec>.md`, `handoff/<sec>.md` |
| `design-critic-agent` | `HIGH` | Revisor adversarial no Outer Loop; emite JSON `APPROVE` ou `REJECT` | Nenhuma (`read-only`) |
| `compiler-agent` | `LOW` | Compila com `-jobname=<sec>` em `out/` e coleta warnings | `out/**` |

---

## 5. Comandos Canônicos

```bash
bash .agents/hooks/pre-task-audit.sh --section 01_abertura
python3 .agents/hooks/boundary-guard.py check --agent slide-author-agent --section 01_abertura
bash .agents/hooks/slide-style-linter.sh secoes/01_abertura
python3 .agents/hooks/fact-sync-check.py secoes/01_abertura
bash .agents/hooks/post-write-compile.sh 01_abertura
bash .agents/hooks/post-write-compile.sh sections
bash .agents/hooks/post-write-compile.sh all
bash .agents/hooks/loop-convergence-guard.sh 01_abertura 1 NONE
python3 .agents/hooks/memory-check.py
```

---

## 6. Invariantes de Tolerância Zero

- **Idioma:** documentação, hooks/skills e texto dos slides em **português** (mantendo identificadores originais de código, sinais e ADRs).
- **Fidelidade Factual:** nunca inventar ou estimar números; nunca incluir histórico descartado na Seção 02.
- **Isolamento de Build:** todo artefato auxiliar e PDF compilado reside exclusivamente em `out/`.
- **Estilo Beamer:** máximo de `6` bullets por `itemize`, zero travessões Unicode (`—`/`–`) em prosa e zero jargões promocionais vazios.
- **Fronteira de Escrita:** nunca modificar arquivos fora de `soc-pres`.
- **Segurança Git:** nunca executar `git commit` automático, `git reset --hard`, `git clean -fd` ou `--no-verify`.
