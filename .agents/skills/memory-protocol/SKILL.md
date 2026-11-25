---
name: memory-protocol
description: Manter memoria persistente em utils/memory/ (INDEX.md, modules/, handoff/, decisions.md, lessons.md, episodes/) enxuta e atualizada.
---

# Memory Protocol

Protocolo de memoria persistente entre iteracoes de secao para evitar releitura integral do repositorio.

## Estrutura em `utils/memory/`

- `INDEX.md` (<= 40 linhas): visao geral de secoes, handoffs ativos e digests.
- `modules/<secao>.md` (<= 60 linhas): digest tecnico da secao, fontes de `../soc-proj` e sha256 dos arquivos locais.
- `handoff/<secao>.md` (<= 50 linhas): estado da iteracao em curso (objetivo, alteracoes, status dos gates, proximo passo).
- `decisions.md`: registro append-only de decisoes da apresentacao (`PRES-ADR-NNN`).
- `lessons.md` (<= 80 linhas): erros recorrentes de LaTeX/hooks e solucoes.
- `episodes/<secao>.md`: historico automatico gravado pelo `loop-convergence-guard.sh`.

## Verificacao

```bash
python3 .agents/hooks/memory-check.py
python3 .agents/hooks/memory-check.py --update all
```
