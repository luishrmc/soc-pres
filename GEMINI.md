# Diretrizes do Sistema: Apresentação SoC Zynq-7010 (`soc-pres`)

Este repositório hospeda a apresentação técnica em LaTeX Beamer (16:9) do projeto final de Sistemas em Chip (SoC) desenvolvido em `../soc-proj`, unificando a identidade visual UFMG e o fluxo multiagente Dual-Loop de `../../seminar` com a governança de memória e fronteira de `../soc-proj`.

---

## 1. Mapa do Workspace

| Caminho | Finalidade | Propriedade / Proteção |
|---|---|---|
| `main.tex` | Documento raiz Beamer 16:9 (`subfiles`) e bibliografia | Protegido (`ALLOW_PROTECTED=1`) |
| `config/` | `00_config.tex`, `estilo_seminario.sty`, `logo.png`, `logo_ufmg.png`, `capa.png` | Protegido |
| `secoes/` | Módulos temáticos: `01_abertura`, `02_arquitetura_e_evolucao`, `03_subssistemas_hw_sw`, `04_metodologia_e_resultados_hil`, `99_conclusao` | Escrita exclusiva de `slide-author-agent` |
| `figuras/` | Diagramas portáveis (`cora7z_top.png`, `cora7z_soc_architecture.pdf`, SVGs) | Leitura / adição controlada |
| `bib/referencias.bib` | Base bibliográfica BibLaTeX/BibTeX | `slide-author-agent` |
| `utils/memory/` | Memória persistente: `INDEX.md`, `decisions.md`, `lessons.md`, `modules/`, `handoff/`, `episodes/` | `orchestrator-agent` / hooks |
| `.agents/` | Manifesto, definições de agentes, skills e hooks determinísticos | Protegido (`manifest.json`) |
| `out/` | Diretório isolado para PDFs e artefatos auxiliares LaTeX (ignorado no Git) | `compiler-agent` |

---

## 2. Hierarquia de Decisão e Fonte da Verdade (`../soc-proj`)

Ordem estrita de precedência (em conflito, interromper e consultar o operador humano):

1. **Instrução explícita do usuário.**
2. **Camada Autoritativa de `../soc-proj` (Estado Final HIL Verificado):**
   - `../soc-proj/README.md`
   - `../soc-proj/utils/plan/STATUS.md`
   - `../soc-proj/utils/plan/Matriz_de_Testes_e_Métricas.csv`
   - `../soc-proj/utils/plan/Checklist_de_Entregaveis.csv`
   - `../soc-proj/utils/memory/INDEX.md` e `../soc-proj/utils/memory/decisions.md` (ADRs 012, 016, 017, 018, 019 e 020)
   - `../soc-proj/cora7z/app/hw/utils/cora_z7_io.xdc` (pinagem física autoritativa)
   - `../soc-proj/docs/hw/{LZSS_ACCEL,AES_ACCEL}.md`, `../soc-proj/docs/sw/*.md`, `../soc-proj/docs/esp32/SPI_INJECTOR.md`, `../soc-proj/docs/adr/0020-fixed-1024b-benchmark-payload.md`
3. **Invariantes de estilo Beamer e validação deste `GEMINI.md`.**
4. **Contexto Histórico Inicial (`../soc-proj/utils/TEMA.md`, `../soc-proj/docs/SYSTEM_ARCHITECTURE.md`):**
   - Descrevem a proposta original (`RLE`, `LZ4`, `ChaCha20`, `AXI DMA`, `axis_accel_mux`) substituída pelo **ADR-017**. Só podem ser citados explicitamente como evolução arquitetural.
   - **Desambiguação obrigatória:** usar `650 MHz` para o Cortex-A9 PS (não `667 MHz`), pinos `H15/T12/W15/F16` + `Y18` (não `G20/T10/V15`), payload `1024 B` (ADR-020) e matriz HIL `N=20` com speedup `1,17x` a `1,24x` no Cenário 3 (não métricas intermediárias como `1,56x` ou `829` ciclos).

---

## 3. Protocolo de Leitura de Sessão

Ao iniciar qualquer tarefa sobre uma seção, ler nesta ordem:
1. Este `GEMINI.md` e `utils/memory/INDEX.md`.
2. `utils/memory/decisions.md` e `utils/memory/lessons.md`.
3. `utils/memory/handoff/<secao>.md` (se existir).
4. Documentos autoritativos relevantes de `../soc-proj` (via `content-retriever-agent` e skill `soc-evidence-lookup`).

---

## 4. Topologia Multiagente e Arquitetura Dual-Loop

Definida em `.agents/manifest.json` sob o perfil **Gemini 4 Hydrogen**:

| Agente | Thinking Level | Papel | Escrita Autorizada |
|---|---|---|---|
| `orchestrator-agent` | `HIGH` | Controla DAG modular, memória, convergência (`N <= 5`) e Gate Humano | `utils/memory/` (nunca edita `.tex`) |
| `content-retriever-agent` | `LOW/MEDIUM` | Extrai fatos e métricas da Camada Autoritativa de `../soc-proj` | Nenhuma (`read-only`) |
| `slide-author-agent` | `HIGH` | Redige e diagrama frames Beamer 16:9 em `secoes/*.tex` | `secoes/**`, `bib/referencias.bib`, `figuras/**`, `handoff/*` |
| `design-critic-agent` | `HIGH` | Auditor adversarial no Outer Loop; emite JSON `APPROVE` ou `REJECT` | Nenhuma (`read-only`) |
| `compiler-agent` | `LOW` | Compila de forma isolada em `out/` e reporta warnings | `out/**` |

Dinâmica dos loops:
- **Inner Loop (Determinístico):** `slide-author-agent` edita a seção e dispara `boundary-guard.py`, `slide-style-linter.sh`, `fact-sync-check.py` e `post-write-compile.sh` (`compiler-agent`). Falhas retornam ao autor sem acionar o revisor.
- **Outer Loop (Adversarial + Gate Humano):** somente após código de saída `0` em todos os hooks do Inner Loop, o `design-critic-agent` audita fidelidade a `../soc-proj` e legibilidade visual. Após `APPROVE`, o fluxo pausa no **Gate Humano** antes de qualquer commit autorizado via `git-safety-guard`.
- **Convergência:** máximo de `5` iterações por seção e parada por estagnação após `2` falhas consecutivas com mesmo hash (`loop-convergence-guard.sh`), disparando rollback seguro (`git checkout HEAD -- <alvo>`).

---

## 5. Catálogo de Skills e Hooks Determinísticos

### Skills (`.agents/skills/`)
- `soc-evidence-lookup`: extração rastreável da Camada Autoritativa de `../soc-proj`.
- `beamer-soc-design`: diagramação Beamer 16:9, estilos TikZ e listagens VHDL/C.
- `slide-visual-review`: rubrica adversarial do `design-critic-agent`.
- `latex-build`: compilação determinística em `out/` e análise de logs.
- `bib-validator`: integridade referencial entre slides e `bib/referencias.bib`.
- `memory-protocol`: manutenção enxuta de `utils/memory/`.
- `git-safety-guard`: validação de staging e gatekeeper único de commit.

### Hooks (`.agents/hooks/`)
- `pre-task-audit.sh`: verifica Git, ferramentas LaTeX, acesso a `../soc-proj`, arquivos protegidos e grava snapshot de fronteira.
- `boundary-guard.py`: garante respeito aos globs de escrita de cada agente em `manifest.json`.
- `slide-style-linter.sh`: verifica limite de `<= 6` bullets por `itemize`, proíbe travessões Unicode (`—`/`–`), proíbe jargões promocionais e checa `[fragile]`.
- `fact-sync-check.py`: valida chaves BibTeX, bloqueia pinos/métricas obsoletas (`G20/T10/V15`, `667 MHz`, `1,56x`), exige contexto histórico para `RLE/LZ4/ChaCha20/AXI DMA` e audita recursos FPGA.
- `post-write-compile.sh`: compila com `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error -outdir=out -auxdir=out` e reporta `Overfull \hbox`.
- `loop-convergence-guard.sh`: controla `N <= 5`, estagnação (`= 2`), episódios e rollback seguro.
- `memory-check.py`: audita limites de linhas e hashes SHA-256 em `utils/memory/`.

---

## 6. Comandos Canônicos

```bash
bash .agents/hooks/pre-task-audit.sh
python3 .agents/hooks/boundary-guard.py check --agent slide-author-agent
bash .agents/hooks/slide-style-linter.sh --all
python3 .agents/hooks/fact-sync-check.py
bash .agents/hooks/post-write-compile.sh all
bash .agents/hooks/loop-convergence-guard.sh 01_abertura 1 NONE
python3 .agents/hooks/memory-check.py
```

---

## 7. Invariantes de Tolerância Zero

- **Idioma:** toda documentação de agentes, `GEMINI.md`, skills, hooks e texto dos slides deve estar em **português** (mantendo identificadores originais de código, sinais, ADRs e termos técnicos consagrados).
- **Fidelidade Factual:** nunca inventar ou estimar números de desempenho; nunca apresentar a proposta inicial (`RLE/LZ4/ChaCha20/AXI DMA`) como arquitetura final.
- **Isolamento de Build:** todo artefato auxiliar e PDF compilado deve residir exclusivamente em `out/`.
- **Estilo Beamer:** máximo de `6` bullets por bloco `itemize`, frases curtas e técnicas, zero travessões Unicode (`—`/`–`) em prosa e zero jargões promocionais vazios (`revolucionário`, `divisor de águas`, `crucial`, `fundamental`, `impressionante`, `vital`).
- **Fronteira de Escrita:** nunca modificar arquivos fora de `soc-pres` (`../soc-proj` e `../../seminar` são estritamente somente leitura).
- **Segurança Git:** nunca executar `git commit` automático, `git reset --hard`, `git clean -fd` ou `--no-verify`.
