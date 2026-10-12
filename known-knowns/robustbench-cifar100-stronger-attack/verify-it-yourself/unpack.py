#!/usr/bin/env python3
"""
unpack.py -- restore the adversarial tensor from the compressed archive and prove that nothing was lost.

The archive adversarial-examples/x_adv_Addepalli2022Efficient_RN18.npz was written with numpy.savez_compressed
(zip + DEFLATE, which is lossless). Its single member x_adv.npy is the original .npy file, byte for byte.

  python3 unpack.py [OUT.npy]
Checks
  1. sha256 of the .npz archive;
  2. sha256 of the member x_adv.npy, streamed straight out of the zip       == ORIGINAL_NPY_SHA256;
  3. sha256 of the array as numpy loads it, re-serialised with numpy.save  == ORIGINAL_NPY_SHA256,
     and sha256 of its raw float32 bytes                                     == ORIGINAL_RAW_SHA256;
and, if OUT.npy is given, writes the original .npy file there (and re-checks its sha256).
Requirements: python3 + numpy. Exit 0 iff all hashes match.
"""
import hashlib, io, os, sys, zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(os.path.dirname(HERE), 'adversarial-examples', 'x_adv_Addepalli2022Efficient_RN18.npz')
NPZ_SHA256 = 'da17d7c6bbb4c4fffb6dcdb66711f02223ad5c58a1362973d167248107477a07'
ORIGINAL_NPY_SHA256 = '4eea7cd6de71c6fc0646adeab2d1a2f3705ded97004ea93f972a7dceef67decb'   # the file the reviewers checked
ORIGINAL_RAW_SHA256 = 'aabc97bd6bb05d9f3a6d0d6793c600f16611ea1688041f3becd892bbcdb81ee0'   # its 122,880,000 data bytes


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(npz=NPZ):
    """Return the float32 array (10000, 3, 32, 32), after checking it is bit-identical to the original."""
    x = np.load(npz, allow_pickle=False)['x_adv']
    buf = io.BytesIO(); np.save(buf, x)
    assert hashlib.sha256(buf.getvalue()).hexdigest() == ORIGINAL_NPY_SHA256, 'tensor differs from the original'
    return x


def main():
    ok = True
    s = sha_file(NPZ)
    print(f'archive  {os.path.basename(NPZ)}  {os.path.getsize(NPZ)} bytes  sha256 {s}  {"ok" if s == NPZ_SHA256 else "MISMATCH"}')
    ok &= s == NPZ_SHA256
    h = hashlib.sha256()
    with zipfile.ZipFile(NPZ) as z:
        names = z.namelist()
        with z.open('x_adv.npy') as m:
            for b in iter(lambda: m.read(1 << 20), b''):
                h.update(b)
        info = z.getinfo('x_adv.npy')
    print(f'members  {names}; x_adv.npy {info.file_size} bytes stored as {info.compress_size} (DEFLATE)')
    print(f'member x_adv.npy sha256 {h.hexdigest()}  {"== original" if h.hexdigest() == ORIGINAL_NPY_SHA256 else "DIFFERS"}')
    ok &= h.hexdigest() == ORIGINAL_NPY_SHA256
    x = np.load(NPZ, allow_pickle=False)['x_adv']
    buf = io.BytesIO(); np.save(buf, x)
    a, r = hashlib.sha256(buf.getvalue()).hexdigest(), hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()
    print(f'loaded array {x.dtype} {x.shape}; numpy.save sha256 {a}  {"== original" if a == ORIGINAL_NPY_SHA256 else "DIFFERS"}')
    print(f'raw float32 bytes sha256 {r}  {"== original" if r == ORIGINAL_RAW_SHA256 else "DIFFERS"}')
    ok &= a == ORIGINAL_NPY_SHA256 and r == ORIGINAL_RAW_SHA256
    if len(sys.argv) > 1:
        out = sys.argv[1]
        with open(out, 'wb') as f:
            f.write(buf.getvalue())
        o = sha_file(out)
        print(f'wrote {out}  sha256 {o}  {"== original" if o == ORIGINAL_NPY_SHA256 else "DIFFERS"}')
        ok &= o == ORIGINAL_NPY_SHA256
    print('LOSSLESS: ' + ('yes, bit-identical to the original tensor' if ok else 'NO'))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
