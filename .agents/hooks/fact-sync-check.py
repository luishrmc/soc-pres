#!/usr/bin/env python3
"""fact-sync-check.py: valida sincronia factual dos slides contra a Camada Autoritativa de ../soc-proj.

Verificacoes deterministicas:
1. Chaves de citacao existem em bib/referencias.bib.
2. Bloqueia pinos obsoletos pre-ADR-016 (G20, T10, V15), clock 667 MHz e metricas
   desatualizadas (1,56x/1.56x, 829 ciclos, 3.410/2.150 pre-ADR-020).
3. Proibe qualquer mencao a historico descartado (RLE, LZ4, ChaCha20, AXI DMA,
   axis_accel_mux, 18.591/11.906/12.709 LUTs) em secoes/02_arquitetura_sistema/.
4. Em outras secoes, exige enquadramento historico explicito caso termos descartados aparecam.
5. Audita contagens de recursos FPGA (LUTs / FFs / BRAMs) contra sistema completo e OOC
   de BENCHMARK_RESULTS.md (§3.4) e Matriz_de_Testes_e_Métricas.csv.

Codigos de saida: 0 = aprovado, 40 = arquivo ausente, 41 = citacao invalida,
                  42 = contaminacao historica/obsoleta, 43 = metrica inconsistente.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOC_PROJ = ROOT.parent / "soc-proj"
MATRIX_CSV = SOC_PROJ / "utils" / "plan" / "Matriz_de_Testes_e_Métricas.csv"
README_MD = SOC_PROJ / "README.md"
BENCH_MD = SOC_PROJ / "cora7z" / "test_results" / "BENCHMARK_RESULTS.md"
BIB_FILE = ROOT / "bib" / "referencias.bib"


def load_bib_keys() -> set[str]:
    if not BIB_FILE.is_file():
        return set()
    text = BIB_FILE.read_text(encoding="utf-8")
    return set(re.findall(r'^\s*@[a-zA-Z]+\s*\{\s*([^,\s]+)\s*,', text, flags=re.M))


def load_matrix_numbers() -> set[str]:
    nums: set[str] = set()
    if MATRIX_CSV.is_file():
        with MATRIX_CSV.open("r", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                for val in row.values():
                    if not val:
                        continue
                    for tok in re.findall(r'-?\d+(?:[.,]\d+)?', val):
                        nums.add(tok.replace(",", "."))
    return nums


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r'(?<!\\)%.*$', '', line) for line in text.splitlines())


def split_frames(text: str) -> list[tuple[int, str]]:
    frames: list[tuple[int, str]] = []
    pattern = re.compile(r'\\begin\{frame\}.*?\\end\{frame\}', re.S)
    for m in pattern.finditer(text):
        line_no = text[:m.start()].count("\n") + 1
        frames.append((line_no, m.group(0)))
    return frames


def expand_targets(args: list[str]) -> list[Path]:
    if not args:
        return sorted((ROOT / "secoes").rglob("*.tex"))
    targets: list[Path] = []
    for raw in args:
        p = Path(raw)
        if not p.is_absolute():
            p = ROOT / raw
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.tex")))
        else:
            targets.append(p)
    return targets


def main() -> int:
    if not MATRIX_CSV.is_file() or not README_MD.is_file() or not BENCH_MD.is_file():
        print("[ERRO][fact-sync-check] Fonte autoritativa ../soc-proj nao encontrada.", file=sys.stderr)
        return 40

    targets = expand_targets(sys.argv[1:])
    if not targets:
        print("[ERRO][fact-sync-check] Nenhum arquivo .tex encontrado.", file=sys.stderr)
        return 40

    bib_keys = load_bib_keys()
    _ = load_matrix_numbers()

    historical_re = re.compile(r'\b(RLE|LZ4|ChaCha20|AXI\s*DMA|axis_accel_mux|18\.?591|11\.?906|12\.?709)\b', re.I)
    historical_ctx_re = re.compile(
        r'(inicial|propost|substitu|piv[oô]|descart|ADR-017|hist[oó]ric|evolu|superad|abandonad|pre-ADR)',
        re.I,
    )
    obsolete_pins_re = re.compile(r'\b(G20|T10|V15)\b')
    stale_metrics_re = re.compile(r'(667\s*MHz|1[.,]56x|\b829\s*ciclos|3\.?410\s*LUTs|2\.?150\s*FFs)', re.I)

    # Numeros verificados (Sistema Completo + OOC BENCHMARK_RESULTS.md §3.4)
    allowed_lut_vals = {
        "8810", "8.810", "17600", "17.600", "14960", "14.960",
        "2764", "2.764", "667", "558", "40", "4781", "4.781",
    }
    allowed_ff_vals = {
        "12048", "12.048", "35200", "35.200", "29920", "29.920",
        "2274", "2.274", "457", "857", "48", "8412", "8.412",
    }
    allowed_bram_vals = {"9", "60", "51", "8", "4", "2", "1"}

    errors: list[tuple[int, str]] = []

    for path in targets:
        if not path.is_file():
            print(f"[ERRO][fact-sync-check] Arquivo ausente: {path}", file=sys.stderr)
            return 40
        clean = strip_comments(path.read_text(encoding="utf-8"))
        rel = str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path)

        for m in re.finditer(r'\\(?:cite|autocite|textcite|fullcite)(?:\[[^\]]*\])?\{([^}]+)\}', clean):
            for key in [k.strip() for k in m.group(1).split(",") if k.strip()]:
                if key not in bib_keys:
                    errors.append((41, f"{rel}: chave BibTeX nao encontrada em bib/referencias.bib: '{key}'"))

        if obsolete_pins_re.search(clean):
            errors.append((42, f"{rel}: pino SPI obsoleto detectado (G20/T10/V15). Use H15/T12/W15/F16."))
        if stale_metrics_re.search(clean):
            errors.append((42, f"{rel}: metrica/clock desatualizado detectado (667 MHz / 1.56x / 829 ciclos / 3.410 LUTs / 2.150 FFs)."))

        is_sec02 = "02_arquitetura_sistema" in rel
        for line_no, frame in split_frames(clean):
            hm = historical_re.search(frame)
            if hm:
                if is_sec02:
                    errors.append((42, f"{rel}:{line_no}: mencao a historico descartado ('{hm.group(1)}') proibida na Secao 02."))
                elif not historical_ctx_re.search(frame):
                    errors.append((42, f"{rel}:{line_no}: termo historico ('{hm.group(1)}') sem enquadramento explicito."))

        for m in re.finditer(r'(\d[\d.,]*)\s*(?:\([^)]*\)\s*)?LUTs?\b', clean):
            val = m.group(1).rstrip(".,")
            if val not in allowed_lut_vals:
                errors.append((43, f"{rel}: contagem de LUTs nao verificada: '{val}'"))
        for m in re.finditer(r'(\d[\d.,]*)\s*(?:\([^)]*\)\s*)?FFs?\b', clean):
            val = m.group(1).rstrip(".,")
            if val not in allowed_ff_vals:
                errors.append((43, f"{rel}: contagem de FFs nao verificada: '{val}'"))
        for m in re.finditer(r'(\d+)\s*(?:\([^)]*\)\s*)?BRAMs?\b', clean):
            val = m.group(1)
            if val not in allowed_bram_vals:
                errors.append((43, f"{rel}: contagem de BRAMs nao verificada: '{val}'"))

    if errors:
        for _, msg in errors:
            print(f"[ERRO][fact-sync-check] {msg}", file=sys.stderr)
        return errors[0][0]

    print(f"[OK][fact-sync-check] {len(targets)} arquivo(s) sincronizado(s) com a Camada Autoritativa de ../soc-proj.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
