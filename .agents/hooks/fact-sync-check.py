#!/usr/bin/env python3
"""fact-sync-check.py: valida sincronia factual dos slides contra a Camada Autoritativa de ../soc-proj.

Verificacoes deterministicas:
1. Chaves de citacao (\\cite, \\autocite, \\textcite, \\fullcite) existem em bib/referencias.bib.
2. Nenhum pino obsoleto pre-ADR-016 (G20, T10, V15) nem clock antigo (667 MHz) nem metrica
   intermediaria superada (1,56x/1.56x, 829 ciclos AES) aparece como estado final HIL.
3. Termos de escopo historico inicial (RLE, LZ4, ChaCha20, AXI DMA, axis_accel_mux) so
   podem aparecer em frames com marcacao explicita de contexto historico / pivo ADR-017.
4. Metricas criticas de silicio e HIL citadas conferem com Matriz_de_Testes_e_Métricas.csv e README.md.

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


def main() -> int:
    if not MATRIX_CSV.is_file() or not README_MD.is_file():
        print("[ERRO][fact-sync-check] Fonte autoritativa ../soc-proj nao encontrada.", file=sys.stderr)
        return 40

    targets = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else sorted((ROOT / "secoes").glob("*.tex"))
    if not targets:
        print("[ERRO][fact-sync-check] Nenhum arquivo .tex encontrado em secoes/.", file=sys.stderr)
        return 40

    bib_keys = load_bib_keys()
    _ = load_matrix_numbers()

    historical_re = re.compile(r'\b(RLE|LZ4|ChaCha20|AXI\s*DMA|axis_accel_mux)\b', re.I)
    historical_ctx_re = re.compile(
        r'(inicial|propost|substitu|piv[oô]|descart|ADR-017|hist[oó]ric|evolu|superad|abandonad|pre-ADR)',
        re.I,
    )
    obsolete_pins_re = re.compile(r'\b(G20|T10|V15)\b')
    stale_metrics_re = re.compile(r'(667\s*MHz|1[.,]56x|\b829\s*ciclos)', re.I)

    # Numeros de recursos da FPGA XC7Z010 verificados em README.md / Matriz_de_Testes_e_Métricas.csv
    allowed_lut_vals = {"8810", "8.810", "17600", "17.600", "14960", "14.960", "667", "3410", "3.410"}
    allowed_ff_vals = {"12048", "12.048", "35200", "35.200", "29920", "29.920", "457", "2150", "2.150"}
    allowed_bram_vals = {"9", "60", "51", "4", "2"}

    errors: list[tuple[int, str]] = []

    for path in targets:
        if not path.is_file():
            print(f"[ERRO][fact-sync-check] Arquivo ausente: {path}", file=sys.stderr)
            return 40
        clean = strip_comments(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT) if path.is_absolute() and str(path).startswith(str(ROOT)) else path

        # 1. Validacao de chaves BibTeX
        for m in re.finditer(r'\\(?:cite|autocite|textcite|fullcite)(?:\[[^\]]*\])?\{([^}]+)\}', clean):
            for key in [k.strip() for k in m.group(1).split(",") if k.strip()]:
                if key not in bib_keys:
                    errors.append((41, f"{rel}: chave BibTeX nao encontrada em bib/referencias.bib: '{key}'"))

        # 2. Pinos obsoletos e metricas antigas desatualizadas
        if obsolete_pins_re.search(clean):
            errors.append((42, f"{rel}: pino SPI obsoleto detectado (G20/T10/V15). Use H15/T12/W15/F16 (cora_z7_io.xdc)."))
        if stale_metrics_re.search(clean):
            errors.append((42, f"{rel}: metrica/clock desatualizado detectado (667 MHz / 1.56x / 829 ciclos). Use camada autoritativa ADR-020 (650 MHz, 1.17x-1.24x)."))

        # 3. Contexto historico obrigatorio para termos da proposta inicial
        for line_no, frame in split_frames(clean):
            hm = historical_re.search(frame)
            if hm and not historical_ctx_re.search(frame):
                errors.append((42, f"{rel}:{line_no}: termo do escopo inicial ('{hm.group(1)}') sem enquadramento historico / ADR-017."))

        # 4. Sanidade de recursos FPGA citados (LUTs / FFs / BRAMs)
        for m in re.finditer(r'(\d[\d.,]*)\s*(?:\([^)]*\)\s*)?LUTs?\b', clean):
            val = m.group(1).rstrip(".,")
            if val not in allowed_lut_vals:
                errors.append((43, f"{rel}: contagem de LUTs nao verificada na fonte autoritativa: '{val}'"))
        for m in re.finditer(r'(\d[\d.,]*)\s*(?:\([^)]*\)\s*)?FFs?\b', clean):
            val = m.group(1).rstrip(".,")
            if val not in allowed_ff_vals:
                errors.append((43, f"{rel}: contagem de FFs nao verificada na fonte autoritativa: '{val}'"))
        for m in re.finditer(r'(\d+)\s*(?:\([^)]*\)\s*)?BRAMs?\b', clean):
            val = m.group(1)
            if val not in allowed_bram_vals:
                errors.append((43, f"{rel}: contagem de BRAMs nao verificada na fonte autoritativa: '{val}'"))

    if errors:
        for _, msg in errors:
            print(f"[ERRO][fact-sync-check] {msg}", file=sys.stderr)
        return errors[0][0]

    print(f"[OK][fact-sync-check] {len(targets)} arquivo(s) sincronizado(s) com a Camada Autoritativa de ../soc-proj.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
