#!/usr/bin/env python3
"""memory-check.py: valida limites, integridade e logs acumulados em utils/memory/.

Verifica:
  * Limites de linhas de INDEX.md, lessons.md, user_feedback_log.md, sections/*.md,
    modules/*.md e handoff/*.md conforme .agents/manifest.json.
  * Existencia de utils/memory/user_feedback_log.md, soc_proj_architecture_map.md e
    de todos os logs utils/memory/sections/<step_id>.md declarados em manifest.json.
  * Frescor de hashes sha256 em modules/*.md (`--update <secao|all>`).

Codigos de saida: 0 = integro, 1 = desatualizado, ausente ou acima do limite.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM = ROOT / "utils" / "memory"
MANIFEST = json.loads((ROOT / ".agents" / "manifest.json").read_text(encoding="utf-8"))
LIM = MANIFEST["limits"]
SRC_RE = re.compile(r"^\s+-\s+(\S+)\s+sha256=(\S*)\s*$")
REQ_SECTION_HEADINGS = ("## Decisoes de Layout", "## Figuras Geradas", "## Pendencias de Revisao")


def sha(rel_path: str) -> str:
    return hashlib.sha256((ROOT / rel_path).read_bytes()).hexdigest()


def line_count(p: Path) -> int:
    return len(p.read_text(encoding="utf-8").splitlines())


def update_hashes(target: str) -> None:
    files = sorted((MEM / "modules").glob("*.md")) if target == "all" else [MEM / "modules" / f"{target}.md"]
    for f in files:
        if not f.is_file():
            print(f"[AVISO][memory-check] Digest nao encontrado: {f.relative_to(ROOT)}", file=sys.stderr)
            continue
        out = []
        for line in f.read_text(encoding="utf-8").splitlines():
            m = SRC_RE.match(line)
            if m and (ROOT / m.group(1)).is_file():
                line = f"  - {m.group(1)} sha256={sha(m.group(1))}"
            out.append(line)
        f.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"[OK][memory-check] Hashes atualizados em {f.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update")
    args = ap.parse_args()

    if args.update:
        update_hashes(args.update)

    problems: list[str] = []

    for req_file in ("INDEX.md", "lessons.md", "user_feedback_log.md", "soc_proj_architecture_map.md"):
        if not (MEM / req_file).is_file():
            problems.append(f"{req_file}: arquivo obrigatorio ausente em utils/memory/")

    for d in sorted((MEM / "modules").glob("*.md")):
        if line_count(d) > LIM["digest_max_lines"]:
            problems.append(f"{d.name}: excede {LIM['digest_max_lines']} linhas")
        for line in d.read_text(encoding="utf-8").splitlines():
            m = SRC_RE.match(line)
            if not m:
                continue
            path, want = m.groups()
            if not (ROOT / path).is_file():
                problems.append(f"{d.name}: arquivo ausente {path}")
            elif want != sha(path):
                problems.append(f"{d.name}: STALE {path}")

    for h in sorted((MEM / "handoff").glob("*.md")):
        if line_count(h) > LIM["handoff_max_lines"]:
            problems.append(f"{h.name}: handoff excede {LIM['handoff_max_lines']} linhas")

    sec_max = LIM.get("section_log_max_lines", 80)
    for step in MANIFEST.get("pipeline_sequence", []):
        sec_id = step["step_id"]
        sec_file = MEM / "sections" / f"{sec_id}.md"
        if not sec_file.is_file():
            problems.append(f"sections/{sec_id}.md: log incremental ausente")
            continue
        if line_count(sec_file) > sec_max:
            problems.append(f"sections/{sec_id}.md: excede {sec_max} linhas")
        txt = sec_file.read_text(encoding="utf-8")
        for heading in REQ_SECTION_HEADINGS:
            if heading not in txt:
                problems.append(f"sections/{sec_id}.md: falta secao '{heading}'")

    for fname, key, default_lim in (
        ("INDEX.md", "index_max_lines", 40),
        ("lessons.md", "lessons_max_lines", 80),
        ("user_feedback_log.md", "feedback_max_lines", 120),
    ):
        f = MEM / fname
        limit = LIM.get(key, default_lim)
        if f.exists() and line_count(f) > limit:
            problems.append(f"{fname}: excede {limit} linhas (compactar)")

    if problems:
        for p in problems:
            print(f"[ERRO][memory-check] {p}", file=sys.stderr)
        return 1

    print("[OK][memory-check] Memoria acumulativa, feedbacks e logs de secao consistentes e dentro dos limites.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
