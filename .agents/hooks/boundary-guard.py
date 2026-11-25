#!/usr/bin/env python3
"""boundary-guard.py: garante isolamento de escrita por agente e por secao (modo paralelo).

Uso:
  python3 .agents/hooks/boundary-guard.py snapshot [--section SEC_ID]
  python3 .agents/hooks/boundary-guard.py check --agent NOME [--section SEC_ID]

Quando --section SEC_ID e informado:
  - o snapshot e gravado em out/boundary_snapshot_<SEC_ID>.json (zero colisao paralela);
  - apenas alteracoes em secoes/<SEC_ID>/**, utils/memory/modules/<SEC_ID>.md e
    utils/memory/handoff/<SEC_ID>.md sao permitidas (bloqueia escrita em outras secoes
    e em arquivos compartilhados serializados como bib/referencias.bib).

Codigos de saida: 0 = ok, 1 = violacao de fronteira, 2 = erro de uso.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / ".agents" / "manifest.json"


def snap_path(section_id: str | None) -> Path:
    name = f"boundary_snapshot_{section_id}.json" if section_id else "boundary_snapshot.json"
    return ROOT / "out" / name


def glob_to_regex(pat: str) -> re.Pattern[str]:
    out, i = "", 0
    while i < len(pat):
        c = pat[i]
        if pat[i:i + 3] == "**/":
            out += "(?:.*/)?"
            i += 3
        elif pat[i:i + 2] == "**":
            out += ".*"
            i += 2
        elif c == "*":
            out += "[^/]*"
            i += 1
        elif c == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(c)
            i += 1
    return re.compile("^" + out + "$")


def matches(path: str, globs: list[str]) -> bool:
    return any(glob_to_regex(g).match(path) for g in globs)


def changed_files() -> dict[str, str]:
    res = subprocess.run(
        ["git", "status", "--porcelain", "-uall"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    files: dict[str, str] = {}
    for line in res.stdout.splitlines():
        path = line[3:].split(" -> ")[-1].strip().strip('"')
        if path.startswith("out/"):
            continue
        p = ROOT / path
        if p.is_dir():
            continue
        files[path] = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "DELETED"
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["snapshot", "check"])
    ap.add_argument("--agent")
    ap.add_argument("--section")
    args = ap.parse_args()

    snap = snap_path(args.section)

    if args.action == "snapshot":
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_text(json.dumps(changed_files(), indent=2), encoding="utf-8")
        print(f"[OK][boundary-guard] Snapshot gravado em {snap.relative_to(ROOT)}.")
        return 0

    if not args.agent:
        print("[ERRO][boundary-guard] --agent e obrigatorio para check.", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    agent = next((x for x in manifest["agents"] if x["name"] == args.agent), None)
    if agent is None:
        print(f"[ERRO][boundary-guard] Agente desconhecido: {args.agent}", file=sys.stderr)
        return 2

    section_globs: list[str] | None = None
    if args.section:
        sec_entry = next((s for s in manifest["pipeline_sequence"] if s["step_id"] == args.section), None)
        if sec_entry is None:
            print(f"[ERRO][boundary-guard] Secao desconhecida: {args.section}", file=sys.stderr)
            return 2
        section_globs = sec_entry.get("write_scope", [f"secoes/{args.section}/**"])

    base = json.loads(snap.read_text(encoding="utf-8")) if snap.exists() else {}
    now = changed_files()
    delta = [p for p, h in now.items() if base.get(p) != h]
    delta += [p for p in base if p not in now]

    # Em modo --section paralelo, ignora alteracoes alheias a secao que ja existiam ou ocorreram em outra secao?
    # Nao: reporta exatamente o delta desta secao/snapshot fora do escopo autorizado.
    protected_ok = os.environ.get("ALLOW_PROTECTED") == "1"
    bad: list[tuple[str, str]] = []
    for p in sorted(set(delta)):
        if matches(p, manifest["protected"]):
            if not protected_ok:
                bad.append((p, "arquivo protegido"))
        elif not matches(p, agent["write"]):
            bad.append((p, "fora dos globs de escrita do agente"))
        elif section_globs is not None and not matches(p, section_globs):
            bad.append((p, f"fora do escopo paralelo da secao {args.section}"))

    if bad:
        for p, why in bad:
            print(f"[ERRO][boundary-guard] {args.agent}: {p} ({why})", file=sys.stderr)
        return 1

    scope_label = f" (secao {args.section})" if args.section else ""
    print(f"[OK][boundary-guard] {args.agent}{scope_label}: {len(delta)} arquivo(s) alterado(s), todos dentro da fronteira.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
