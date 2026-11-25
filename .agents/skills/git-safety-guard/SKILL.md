---
name: git-safety-guard
description: Gatekeeper de seguranca Git que valida staging, bloqueia artefatos em out/ e exige aprovacao humana antes de qualquer commit.
---

# Git Safety Guard

Protocolo de integridade Git do workspace `soc-pres`.

## Regras Inviolaveis

1. Nunca executar `git commit` automaticamente sem aprovacao explicita do operador humano (Gate Humano) e veredito `APPROVE` do `design-critic-agent`.
2. Nunca usar `git reset --hard`, `git clean -fd`, `--no-verify` ou `rm -rf` fora de `out/`.
3. Antes de qualquer commit autorizado pelo usuario:
   - Verificar que nenhum arquivo de `out/` ou temporario LaTeX (`*.aux`, `*.log`, `*.pdf` fora de `figuras/`) esteja em stage.
   - Executar `bash .agents/hooks/slide-style-linter.sh --all`, `python3 .agents/hooks/fact-sync-check.py` e `bash .agents/hooks/post-write-compile.sh main` com codigo de saida `0`.
4. Rollback seguro em falha de convergencia: usar exclusivamente `git checkout HEAD -- <arquivo_alvo>`.
