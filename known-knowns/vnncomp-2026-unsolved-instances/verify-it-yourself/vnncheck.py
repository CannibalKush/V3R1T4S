#!/usr/bin/env python3
"""
vnncheck.py -- standalone checker for the two VNN-COMP 2026 counterexamples in ../witnesses/.

For each instance it
  1. downloads the ONNX model and the VNN-LIB property from the official benchmark repository
     github.com/VNN-COMP/vnncomp2026_benchmarks at a pinned commit (one GET per file, cached in --cache),
     and checks their sha256 against the values pinned below;
  2. parses every (assert ...) of the property with a small s-expression reader written for this release;
  3. reads the witness (2700 decimal numbers, X[0,h,w,c] in row-major order) and checks, in exact rational
     arithmetic, that every input constraint holds STRICTLY (no tolerance; a value equal to a bound fails)
     and that every value is exactly representable in float32 (so the network sees exactly the witness);
  4. runs the network with onnxruntime (CPUExecutionProvider, float32) and evaluates the output assertion at
     zero tolerance; if the `onnx` package is installed it repeats the evaluation with onnx.reference;
  5. checks that the X block of witness_v2.txt (VNN-LIB 2.0 assignment) equals witness_plain.txt exactly.

Requirements: python3 (3.9+), numpy, onnxruntime; optional: onnx (second runtime).

  python3 vnncheck.py                       # both instances, downloads into a temporary directory
  python3 vnncheck.py --cache DIR           # keep the downloads (reused on the next run, sha256 re-checked)
  python3 vnncheck.py --witness FILE --instance 1703   # check another witness file (used by run_checks.sh)

Exit code 0 iff every check passes. Last line per instance: VNNCHECK PASS ... or VNNCHECK FAIL ...
"""
import argparse, gzip, hashlib, os, re, sys, tempfile, urllib.request
from fractions import Fraction

import numpy as np

BENCH_REPO = 'VNN-COMP/vnncomp2026_benchmarks'
BENCH_COMMIT = '303f2327a8e8411efc4457da03d2016ce42733cf'   # main on 2026-10-12T03:36Z (pushed 2026-07-07)
BENCH_DIR = 'benchmarks/traffic_signs_recognition_2023/2.0'
NETWORK = '3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30'
ONNX_GZ_SHA256 = 'baeca5c8bcf58a9b8bf8a22cf59fffd2fc5e2baac0fd1e5be467dbb716f78a83'
ONNX_SHA256 = '9fb711d9b0019889d648df23ce477a083f0f6d6ef13f732de284a607f0abdce6'
INSTANCES = {
    '1703': dict(prop='model_30_idx_1703_eps_1.00000',
                 vnnlib_gz_sha256='5e4318e8e9320325f0d03f110439f1febe8b34a407bafd4e737359cb958f590a',
                 vnnlib_sha256='cdd6b802863e0f0d7f958e2474743cb7a8706ce75478e8d721462b1a212551d5',
                 witness='model_30_idx_1703_eps_1'),
    '178': dict(prop='model_30_idx_178_eps_1.00000',
                vnnlib_gz_sha256='3b690c291a9f43f4a47ad1987d92abc301c9075fa7567418a1599fe142c3b20e',
                vnnlib_sha256='746adabaff524f20fd49e6dd246a3346cbf1a9f32d55c80346d6b76ecf094571',
                witness='model_30_idx_178_eps_1'),
}
UA = 'V3R1T4S-verify-it-yourself (one GET per file; github.com/elder-plinius/V3R1T4S)'
HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def fetch(rel, cache):
    """One GET of BENCH_REPO@BENCH_COMMIT/<rel>, cached under cache/<rel>."""
    path = os.path.join(cache, rel)
    if not os.path.isfile(path):
        url = f'https://raw.githubusercontent.com/{BENCH_REPO}/{BENCH_COMMIT}/{rel}'
        print(f'  GET {url}')
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data)
    with open(path, 'rb') as f:
        return f.read()


# ---------- a minimal s-expression reader and evaluator for the VNN-LIB assertions used here ----------

def tokenize(text):
    text = re.sub(r';[^\n]*', '', text)                       # comments
    return re.findall(r'\(|\)|[^\s()]+', text)


def parse_forms(tokens):
    stack, out = [[]], None
    for t in tokens:
        if t == '(':
            stack.append([])
        elif t == ')':
            top = stack.pop()
            stack[-1].append(top)
        else:
            stack[-1].append(t)
    assert len(stack) == 1, 'unbalanced parentheses'
    return stack[0]


VAR = re.compile(r'^([XY])\[([0-9,]+)\]$')


def term(tok, env):
    m = VAR.match(tok)
    if m:
        return env[m.group(1)][tuple(int(i) for i in m.group(2).split(','))]
    return Fraction(tok)                                      # numeric literal, exact


def variables(e, acc):
    if isinstance(e, list):
        for s in e:
            variables(s, acc)
    else:
        m = VAR.match(e)
        if m:
            acc.add(m.group(1))
    return acc


def margin(e, env, strict):
    """Return m such that the formula holds iff m > 0 (strict) or m >= 0 (non-strict)."""
    op = e[0]
    if op == 'and':
        return min(margin(s, env, strict) for s in e[1:])
    if op == 'or':
        return max(margin(s, env, strict) for s in e[1:])
    if op in ('<=', '>=', '<', '>') and len(e) == 3:
        a, b = term(e[1], env), term(e[2], env)
        return (b - a) if op in ('<=', '<') else (a - b)
    raise ValueError(f'unsupported operator {op!r} (this checker handles and/or/<=/>=/</> only)')


def holds(m, strict):
    return m > 0 if strict else m >= 0


# ---------- checks ----------

def read_plain(path):
    with open(path) as f:
        toks = [l.strip() for l in f if l.strip()]
    return toks


def read_v2_x(path):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    assert lines[0] == 'sat', 'witness_v2: first line must be "sat"'
    assert lines[1].replace(' ', '') == 'Xfloat32[1,30,30,3]', 'witness_v2: unexpected X header ' + lines[1]
    return lines[2:2 + 2700]


def check_instance(key, cache, witness_path, onnx_bytes, do_v2):
    inst = INSTANCES[key]
    ok = True
    print(f"== instance {NETWORK} + {inst['prop']}")
    gz = fetch(f"{BENCH_DIR}/vnnlib/{inst['prop']}.vnnlib.gz", cache)
    g1, raw = sha256(gz), gzip.decompress(gz)
    g2 = sha256(raw)
    print(f'  vnnlib.gz sha256 {g1} {"(pinned)" if g1 == inst["vnnlib_gz_sha256"] else "MISMATCH"}')
    print(f'  vnnlib    sha256 {g2} {"(pinned)" if g2 == inst["vnnlib_sha256"] else "MISMATCH"}')
    ok &= g1 == inst['vnnlib_gz_sha256'] and g2 == inst['vnnlib_sha256']

    forms = parse_forms(tokenize(raw.decode()))
    asserts = [f[1] for f in forms if isinstance(f, list) and f and f[0] == 'assert']
    in_asserts = [a for a in asserts if variables(a, set()) == {'X'}]
    out_asserts = [a for a in asserts if 'Y' in variables(a, set())]
    assert len(in_asserts) + len(out_asserts) == len(asserts)
    # every input coordinate must have one lower and one upper bound
    seen = {}
    for a in in_asserts:
        if a[0] in ('<=', '>=') and VAR.match(a[1]) and not VAR.match(a[2]):
            seen.setdefault(a[1], set()).add(a[0])
    full = len(seen) == 2700 and all(v == {'<=', '>='} for v in seen.values())
    print(f'  property: {len(in_asserts)} input assertions, {len(out_asserts)} output assertion(s); '
          f'all 2700 coordinates bounded above and below: {full}')
    ok &= full

    toks = read_plain(witness_path)
    if len(toks) != 2700:
        print(f'  witness has {len(toks)} values, expected 2700'); return False
    xq = [Fraction(t) for t in toks]                            # exact decimal values as written
    x32 = np.array([float(t) for t in toks], dtype=np.float32)
    f32_exact = all(Fraction(float(v)) == q for v, q in zip(x32.tolist(), xq))
    print(f'  witness sha256 {sha256(open(witness_path, "rb").read())}; every value exactly representable in float32: {f32_exact}')
    ok &= f32_exact
    X = {}
    for n, q in enumerate(xq):
        h, r = divmod(n, 90); w, c = divmod(r, 3)
        X[(0, h, w, c)] = q
    in_m = min(margin(a, {'X': X}, True) for a in in_asserts)
    strict_in = holds(in_m, True)
    print(f'  input box, exact rationals, strict: {strict_in}; smallest distance to a bound = {in_m} = {float(in_m)}')
    ok &= strict_in

    def run(label, y):
        Y = {(0, j): Fraction(float(v)) for j, v in enumerate(y.reshape(-1).tolist())}
        ms = [margin(a, {'Y': Y}, False) for a in out_asserts]
        h = all(holds(m, False) for m in ms)
        print(f'  {label}: output assertion holds at zero tolerance: {h}; margin {float(min(ms)):.8f}; '
              f'argmax {int(np.argmax(y))}')
        return h, float(min(ms))

    import onnxruntime as ort
    sess = ort.InferenceSession(onnx_bytes, providers=['CPUExecutionProvider'])
    y_ort = sess.run(None, {sess.get_inputs()[0].name: x32.reshape(1, 30, 30, 3)})[0]
    h, m = run(f'onnxruntime {ort.__version__} CPU float32', y_ort)
    ok &= h
    try:
        import onnx
        from onnx.reference import ReferenceEvaluator
        ref = ReferenceEvaluator(onnx.load_from_string(onnx_bytes))
        y_ref = ref.run(None, {sess.get_inputs()[0].name: x32.reshape(1, 30, 30, 3)})[0]
        h2, _ = run(f'onnx.reference {onnx.__version__}', y_ref)
        print(f'  max |onnxruntime - onnx.reference| = {float(np.abs(y_ort - y_ref).max())}')
        ok &= h2
    except ImportError:
        print('  (onnx not installed: second runtime skipped)')

    if do_v2:
        v2 = os.path.join(os.path.dirname(witness_path), 'witness_v2.txt')
        same = [Fraction(t) for t in read_v2_x(v2)] == xq
        print(f'  witness_v2.txt X block equals witness_plain.txt exactly: {same}')
        ok &= same
    print(f"VNNCHECK {'PASS' if ok else 'FAIL'} instance={NETWORK}/{inst['prop']} "
          f"margin={m:.8f} min_input_slack={float(in_m)} witness={os.path.relpath(witness_path, os.path.dirname(HERE))}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cache', default=None, help='download directory (default: a fresh temporary directory)')
    ap.add_argument('--instance', choices=sorted(INSTANCES), default=None)
    ap.add_argument('--witness', default=None, help='witness_plain-format file (default: the shipped witness)')
    a = ap.parse_args()
    cache = a.cache or tempfile.mkdtemp(prefix='vnncheck-')
    print(f'benchmark repository {BENCH_REPO} at commit {BENCH_COMMIT}')
    gz = fetch(f'{BENCH_DIR}/onnx/{NETWORK}.onnx.gz', cache)
    onnx_bytes = gzip.decompress(gz)
    ok = sha256(gz) == ONNX_GZ_SHA256 and sha256(onnx_bytes) == ONNX_SHA256
    print(f'  onnx.gz sha256 {sha256(gz)} {"(pinned)" if sha256(gz) == ONNX_GZ_SHA256 else "MISMATCH"}')
    print(f'  onnx    sha256 {sha256(onnx_bytes)} {"(pinned)" if sha256(onnx_bytes) == ONNX_SHA256 else "MISMATCH"}')
    keys = [a.instance] if a.instance else ['1703', '178']
    for k in keys:
        if a.witness and not a.instance:
            sys.exit('--witness needs --instance')
        w = a.witness or os.path.join(os.path.dirname(HERE), 'witnesses', INSTANCES[k]['witness'], 'witness_plain.txt')
        ok &= check_instance(k, cache, w, onnx_bytes, do_v2=a.witness is None)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
