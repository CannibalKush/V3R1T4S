#!/usr/bin/env python3
"""
Campaign driver for Lens 1 (c-evaluator-optimizer).
Compiles code/maxdet_search.c, builds Paley Class I and Williamson Hadamard cores
for unclosed n == 1 (mod 4) orders (including n = 105, 109, 117 and smaller orders
n = 45, 49, 69, 73, 81), runs high-throughput C Iterated Local Search (1-flip +
2-flip steepest ascent + multi-radius Basin Hopping kicks) + Sherman-Morrison
determinant polish, and verifies every record matrix via verify_maxdet.py.
"""

import itertools
import json
import os
import subprocess
import sys


def find_williamson_m29_quadruples(max_quads=5):
    """
    Find distinct Williamson quadruples (A, B, C, D) of symmetric circulant {-1, +1}
    matrices of order m = 29 with row sums (9, 5, -3, 1), satisfying
    A^2 + B^2 + C^2 + D^2 = 116 I_29.
    """
    def get_paf_map(k):
        res = {}
        for comb in itertools.combinations(range(1, 15), k):
            seq = [1] * 29
            for idx in comb:
                seq[idx] = -1
                seq[29 - idx] = -1
            paf = tuple(sum(seq[i] * seq[(i + s) % 29] for i in range(29)) for s in range(1, 15))
            if paf not in res:
                res[paf] = seq
        return res

    t5 = get_paf_map(5)   # sum = 9
    t6 = get_paf_map(6)   # sum = 5
    t8 = get_paf_map(8)   # sum = -3
    t7 = get_paf_map(7)   # sum = 1

    sum_AB = {}
    for p5, s5 in t5.items():
        for p6, s6 in t6.items():
            psum = tuple(p5[i] + p6[i] for i in range(14))
            if psum not in sum_AB:
                sum_AB[psum] = (s5, s6)

    quads = []
    for p8, s8 in t8.items():
        for p7, s7 in t7.items():
            need = tuple(-(p8[i] + p7[i]) for i in range(14))
            if need in sum_AB:
                s5, s6 = sum_AB[need]
                quads.append((s5, s6, s8, s7))
                if len(quads) >= max_quads:
                    return quads
    return quads


def build_williamson_hadamard(m, quad):
    """Assemble a 4m x 4m Hadamard matrix from a Williamson quadruple of length m."""
    def circ(seq):
        return [[seq[(j - i) % m] for j in range(m)] for i in range(m)]

    A, B, C, D = [circ(s) for s in quad]
    H = [[0] * (4 * m) for _ in range(4 * m)]
    blocks = [
        [(1, A), (1, B), (1, C), (1, D)],
        [(-1, B), (1, A), (-1, D), (1, C)],
        [(-1, C), (1, D), (1, A), (-1, B)],
        [(-1, D), (-1, C), (1, B), (1, A)],
    ]
    for bi in range(4):
        for bj in range(4):
            sgn, blk = blocks[bi][bj]
            for i in range(m):
                for j in range(m):
                    H[bi * m + i][bj * m + j] = sgn * blk[i][j]
    return H


def save_matrix(path, mat):
    with open(path, "w", encoding="utf-8") as f:
        for row in mat:
            f.write(" ".join(str(x) for x in row) + "\n")


def main():
    attempt_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_dir = os.path.dirname(os.path.dirname(attempt_dir))
    code_dir = os.path.join(attempt_dir, "code")
    results_dir = os.path.join(run_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    c_src = os.path.join("code", "maxdet_search.c")
    c_bin = os.path.join("code", "maxdet_search")
    print("[1] Compiling C optimizer code/maxdet_search.c ...")
    subprocess.run(["clang", "-O3", "-march=native", c_src, "-o", c_bin, "-lm"],
                   cwd=attempt_dir, check=True)

    with open(os.path.join(run_dir, "data", "maxdet_table.json"), "r", encoding="utf-8") as f:
        table = json.load(f)

    # 1. Audit smaller Paley Class I orders n in {45, 49, 69, 73, 81}
    print("\n[2] Auditing smaller unclosed Paley Class I orders (n = 45, 49, 69, 73, 81) ...")
    for n in [45, 49, 69, 73, 81]:
        k = (n - 1) // 4
        rec_D = int(table[str(n)]["exact_norm_det"])
        rec_factor = rec_D // (k ** (2 * k - 1))
        res = subprocess.run(
            [c_bin, str(n), "150", "40", "paley1"],
            cwd=attempt_dir, capture_output=True, text=True, check=True
        )
        print(f"  {res.stdout.strip()} | standing_record_factor={rec_factor}")

    # 2. Campaign on n = 105 (m = 104, p = 103 Paley Class I)
    print("\n[3] Running high-intensity C optimization on n = 105 (m = 104, Paley Class I) ...")
    cand_105 = os.path.join(code_dir, "cand_105.txt")
    res_105 = subprocess.run(
        [c_bin, "105", "300", "80", "paley1", cand_105],
        cwd=attempt_dir, capture_output=True, text=True, check=True
    )
    print(" ", res_105.stdout.strip())

    # 3. Campaign on n = 109 (m = 108, p = 107 Paley Class I)
    print("\n[4] Running high-intensity C optimization on n = 109 (m = 108, Paley Class I) ...")
    cand_109 = os.path.join(code_dir, "cand_109.txt")
    res_109 = subprocess.run(
        [c_bin, "109", "300", "80", "paley1", cand_109],
        cwd=attempt_dir, capture_output=True, text=True, check=True
    )
    print(" ", res_109.stdout.strip())

    # 4. Campaign on n = 117 (m = 116 = 4 * 29, Williamson quadruples)
    print("\n[5] Generating Williamson m = 29 Hadamard matrices H_116 and optimizing n = 117 ...")
    quads = find_williamson_m29_quadruples(max_quads=5)
    print(f"  Found {len(quads)} distinct Williamson m=29 quadruples.")
    best_117_factor = -1
    cand_117 = os.path.join(code_dir, "cand_117.txt")
    for idx, quad in enumerate(quads):
        H116 = build_williamson_hadamard(29, quad)
        h_path = os.path.join(code_dir, f"H116_williamson_{idx}.txt")
        out_path = os.path.join(code_dir, f"cand_117_{idx}.txt")
        save_matrix(h_path, H116)
        res = subprocess.run(
            [c_bin, "117", "250", "60", h_path, out_path],
            cwd=attempt_dir, capture_output=True, text=True, check=True
        )
        line = res.stdout.strip()
        print(f"  Williamson #{idx}: {line}")
        for tok in line.split():
            if tok.startswith("factor="):
                fac = int(tok.split("=")[1])
                if fac > best_117_factor:
                    best_117_factor = fac
                    with open(out_path, "r", encoding="utf-8") as src, open(cand_117, "w", encoding="utf-8") as dst:
                        dst.write(src.read())

    # 5. Exact verification and archival of new record matrices
    print("\n[6] Running independent exact verification (Bareiss + Multi-Prime CRT) via verify_maxdet.py ...")
    sys.path.insert(0, run_dir)
    import verify_maxdet

    for n, cand_path in [(105, cand_105), (109, cand_109), (117, cand_117)]:
        X = verify_maxdet.parse_pm1_matrix(cand_path)
        det_b = verify_maxdet.det_bareiss(X)
        det_c = verify_maxdet.det_crt(X, max_abs_entry=1)
        assert det_b == det_c, f"Mismatch on n={n}!"
        D_norm = abs(det_b) >> (n - 1)
        rec_D = int(table[str(n)]["exact_norm_det"])
        assert D_norm > rec_D, f"Not a record for n={n}"
        final_name = f"M{n}_{D_norm}.txt"
        final_path = os.path.join(results_dir, final_name)
        with open(cand_path, "r", encoding="utf-8") as src, open(final_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())
        print(f"\n--- Verified New Record Saved: results/{final_name} ---")
        subprocess.run(
            ["python3", "verify_maxdet.py", os.path.join("results", final_name)],
            cwd=run_dir, check=True
        )


if __name__ == "__main__":
    main()
