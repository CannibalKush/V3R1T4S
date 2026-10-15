# Run it yourself

From this folder, in a fresh shell (any OS with sh and Python 3.8+):

    sh verify-it-yourself/run_checks.sh

Expected output: one JSON line with "format": "5x5x5", "rank": 93, "total": 358, "tensor_CT_mismatches": 0, "random_fail_CT": 0,
"pass": true, then `format 5x5x5 rank 93 additions 358 exact True`, then `PASS`.

Optional calibration against the record: download Perminov's schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json and run
`python3 -I verify-it-yourself/indep_check.py <that file>`; expected total 383 (= its stated complexity.reduced).

Rebuild: how-we-built-it/ holds the search code (numpy, numba) and the PREREG files of the runs involved. The search is
randomized; rerunning finds programs of similar length, not necessarily this exact file.
