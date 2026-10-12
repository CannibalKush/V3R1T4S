#!/usr/bin/env python3
"""
official_validate.py -- run the competition's OWN validator, unmodified, on the two shipped VNN-LIB 2.0 witnesses.

Downloads SCORING/counterexamples_v2.py and the two modules it imports (benchmark_instances.py, cex_checks.py) from
github.com/VNN-COMP/vnncomp2026_results at a pinned commit (sha256 checked), downloads the benchmark files exactly as
vnncheck.py does, and calls

    counterexamples_v2.validate_vnnlib2_counterexample(benchmark_dir, network_field, property_field, ce_path,
                                                       abs_tol, rel_tol, result_type)

with abs_tol = 1e-4 (the competition setting, SCORING/settings.py COUNTEREXAMPLE_ATOL) and again with abs_tol = 0.
Only the result-type enum (a plain class with the six names the validator uses) is supplied here; the validator
replays the network itself with onnxruntime and ignores the Y block of the witness.

Requirements: python3, numpy, onnx, onnxruntime, and the VNN-LIB reference parser `pip install vnnlib==1.0.2`
(the competition pins numpy 2.2.6, onnx 1.21.0, onnxruntime 1.26.0, vnnlib 1.0.2 in SCORING/requirements.txt).
This executes code downloaded from the VNN-COMP results repository; read it first if you prefer.

  python3 official_validate.py [--cache DIR]
Expected: for each instance `('correct', '... all assertions hold with input_tolerance=0.0, output_tolerance=0.0')`.
"""
import argparse, os, sys, tempfile, urllib.request, hashlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vnncheck as vc  # noqa: E402  (pins, downloader)

RESULTS_REPO = 'VNN-COMP/vnncomp2026_results'
RESULTS_COMMIT = 'eea564f5d0a8751d8321a409214db14d03f452b8'   # main on 2026-10-12T03:36Z (pushed 2026-08-03)
SCORING = {
    'counterexamples_v2.py': '5ab7a4df717ed1c80ec0477372eb394a4a2a460a5060f0eebe030a76d219faab',
    'benchmark_instances.py': '5873d78347aee9b96359521c486fef2516378c27f89b89b53f4336804406d229',
    'cex_checks.py': '695fcd436ddf354d6dd206fdac64f7c52a045bfb56edf0f2bfaa8b30e7dacfc5',
}


class ResultType:
    CORRECT = 'correct'
    CORRECT_UP_TO_TOLERANCE = 'correct_up_to_tolerance'
    SPEC_NOT_VIOLATED = 'spec_not_violated'
    NO_CE = 'no_ce'
    MALFORMED_CE = 'malformed_ce'
    UNSUPPORTED = 'unsupported'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', default=None)
    a = ap.parse_args()
    cache = a.cache or tempfile.mkdtemp(prefix='vnn-official-')
    sdir = os.path.join(cache, 'SCORING')
    os.makedirs(sdir, exist_ok=True)
    ok = True
    for name, want in SCORING.items():
        p = os.path.join(sdir, name)
        if not os.path.isfile(p):
            url = f'https://raw.githubusercontent.com/{RESULTS_REPO}/{RESULTS_COMMIT}/SCORING/{name}'
            print(f'GET {url}')
            req = urllib.request.Request(url, headers={'User-Agent': vc.UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(p, 'wb') as f:
                f.write(r.read())
        got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        print(f'SCORING/{name} sha256 {got} {"(pinned)" if got == want else "MISMATCH"}')
        ok &= got == want
    if not ok:
        sys.exit('validator files do not match the pinned sha256; stopping')
    vc.fetch(f'{vc.BENCH_DIR}/onnx/{vc.NETWORK}.onnx.gz', cache)
    sys.path.insert(0, sdir)
    import counterexamples_v2 as cv2
    bench = Path(cache) / vc.BENCH_DIR
    root = os.path.dirname(vc.HERE)
    for k, inst in vc.INSTANCES.items():
        vc.fetch(f"{vc.BENCH_DIR}/vnnlib/{inst['prop']}.vnnlib.gz", cache)
        nf = f'vnncomp2026_benchmarks/{vc.BENCH_DIR}/onnx/{vc.NETWORK}.onnx'
        pf = f"vnncomp2026_benchmarks/{vc.BENCH_DIR}/vnnlib/{inst['prop']}.vnnlib"
        ce = os.path.join(root, 'witnesses', inst['witness'], 'witness_v2.txt')
        for tol in (1e-4, 0.0):
            r = cv2.validate_vnnlib2_counterexample(bench, nf, pf, ce, tol, 0.0, ResultType)
            print(f"{vc.NETWORK}/{inst['prop']} abs_tol={tol}: {r}")
            ok &= r[0] == 'correct'
    print('OFFICIAL VALIDATOR: ' + ('both correct' if ok else 'NOT correct'))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
