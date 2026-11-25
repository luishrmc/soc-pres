#!/usr/bin/env python3
"""memory-check.py: valida limites de linhas e frescor de hashes em utils/memory/.

Uso:
  python3 .agents/hooks/memory-check.py [--update <secao|all>]
Codigos de saida: 0 = integro, 1 = desatualizado ou acima do limite.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM = ROOT / "utils" / "memory"
LIM = json.loads((ROOT / ".agents" / "manifest.json").read_text(encoding="utf-8"))["limits"]
SRC_RE = re.compile(r"^\s+-\s+(\S+)\s+sha256=(\S*)\s*$")


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

    for fname, key in (("INDEX.md", "index_max_lines"), ("lessons.md", "lessons_max_lines")):
        f = MEM / fname
        if f.exists() and line_count(f) > LIM[key]:
            problems.append(f"{fname}: excede {LIM[key]} linhas (compactar)")

    if problems:
        for p in problems:
            print(f"[ERRO][memory-check] {p}", file=sys.stderr)
        return 1

    print("[OK][memory-check] Memoria consistente e dentro dos limites.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
