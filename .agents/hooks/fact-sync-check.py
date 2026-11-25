#!/usr/bin/env python3
"""fact-sync-check.py: gate deterministico anti-desvio contra a Camada Autoritativa de ../soc-proj.

Verificacoes:
1. Chaves de citacao existem em bib/referencias.bib.
2. Bloqueia pinos obsoletos (G20, T10, V15), clock 667 MHz e metricas superadas
   (1,56x/1.56x, 829 ciclos, 3.410 LUTs, 2.150 FFs).
3. Proibe qualquer mencao a historico descartado (RLE, LZ4, ChaCha20, AXI DMA,
   axis_accel_mux, 18.591/11.906/12.709) em secoes/02_arquitetura_sistema/.
4. Bloqueia detalhamento de protagonismo do ESP32 (ESP-IDF, 240 MHz, spi_injector_master,
   trigger_gpio, GPIO 32, lockout) fora de secoes/05_ferramenta_auxiliar_esp32/.
5. Audita contagens de recursos FPGA (LUTs / FFs / BRAMs) e presenca de enderecos AXI validos.

Codigos de saida: 0 = aprovado, 40 = arquivo ausente, 41 = citacao invalida,
                  42 = contaminacao historica/escopo/obsoleta, 43 = metrica inconsistente.
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
ARCH_MAP = ROOT / "utils" / "memory" / "soc_proj_architecture_map.md"
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
    if not MATRIX_CSV.is_file() or not README_MD.is_file() or not BENCH_MD.is_file() or not ARCH_MAP.is_file():
        print("[ERRO][fact-sync-check] Fonte autoritativa ../soc-proj ou mapa local ausente.", file=sys.stderr)
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
    esp32_detail_re = re.compile(r'\b(ESP-IDF|240\s*MHz|spi_injector_master|trigger_gpio|GPIO\s*32|lockout)\b', re.I)

    allowed_lut_vals = {
        "8810", "8.810", "17600", "17.600", "14960", "14.960",
        "2764", "2.764", "667", "558", "40", "4781", "4.781",
    }
    allowed_ff_vals = {
        "12048", "12.048", "35200", "35.200", "29920", "29.920",
        "2274", "2.274", "457", "857", "48", "8412", "8.412",
    }
    allowed_bram_vals = {"9", "60", "51", "8", "4", "2", "1"}
    valid_axi_addrs = {
        "0x40000000", "0x40002000", "0x40010000", "0x40012000",
        "0x41E00000", "0x43C00000", "0x43C10000", "0xF800700C",
    }

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
        is_sec05 = "05_ferramenta_auxiliar_esp32" in rel

        if not is_sec05:
            em = esp32_detail_re.search(clean)
            if em:
                errors.append((42, f"{rel}: detalhe interno de ESP32 ('{em.group(1)}') fora da Secao 05 (desvio de escopo)."))

        for line_no, frame in split_frames(clean):
            hm = historical_re.search(frame)
            if hm:
                if is_sec02:
                    errors.append((42, f"{rel}:{line_no}: mencao a historico descartado ('{hm.group(1)}') proibida na Secao 02."))
                elif not historical_ctx_re.search(frame):
                    errors.append((42, f"{rel}:{line_no}: termo historico ('{hm.group(1)}') sem enquadramento explicito."))

        for m in re.finditer(r'0x[0-9A-Fa-f]{8}\b', clean):
            addr = "0x" + m.group(0)[2:].upper()
            if addr not in valid_axi_addrs:
                errors.append((43, f"{rel}: endereco 32 bits nao listado no mapa canonico: '{m.group(0)}'"))

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
