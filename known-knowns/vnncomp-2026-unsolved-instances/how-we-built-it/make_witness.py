"""Turn a CP-SAT checkpoint (d vector, NHWC order) into witness files and replay with onnxruntime.
  x = v + off + m*d  with (v, off, m) = bnn.pixel_map(lo, hi, pw)   (float32-exact; strictly inside the box)
Writes: <out>/witness_plain.txt (one value per line, X[0,h,w,c] row-major) and <out>/witness_v2.txt (VNN-LIB 2.0
textual assignment with X and Y blocks, Y = onnxruntime replay).
Usage: python -I make_witness.py --ckpt ckpt.json --vnnlib P.vnnlib.gz --onnx NET.onnx.gz --out DIR [--shape 30,30,3] [--pw 9]
(pw defaults to the value stored in the checkpoint, else 9. The idx_1703 checkpoint in checkpoints/ has no pw field;
it was searched with pw = 10, so pass --pw 10 for it.)
"""
import argparse, gzip, json, os, sys
import numpy as np
import onnxruntime as ort
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bnn import parse_box, pixel_map

ap = argparse.ArgumentParser()
ap.add_argument('--ckpt', required=True); ap.add_argument('--vnnlib', required=True); ap.add_argument('--onnx', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--shape', default='30,30,3'); ap.add_argument('--pw', type=int, default=None)
a = ap.parse_args()
shape = tuple(int(s) for s in a.shape.split(','))
ck = json.load(open(a.ckpt))
pw = a.pw if a.pw is not None else int(ck.get('pw', 9))
lo, hi, tgt = parse_box(a.vnnlib, shape)
v, off, m, dmin, dmax = pixel_map(lo, hi, pw)
d = np.array(ck['d'], dtype=np.int64).reshape(shape)
assert np.all(d >= dmin) and np.all(d <= dmax), 'd outside its domain'
x64 = v.astype(np.float64) + off + m * d
x = x64.astype(np.float32)
assert np.all(x.astype(np.float64) == x64), 'not float32-exact'
assert (lo < x).all() and (x < hi).all(), 'not strictly inside'
os.makedirs(a.out, exist_ok=True)
flat = x.reshape(-1)
with open(os.path.join(a.out, 'witness_plain.txt'), 'w') as f:
    for val in flat: f.write(repr(float(val)) + '\n')
so = ort.SessionOptions(); so.intra_op_num_threads = 1; so.inter_op_num_threads = 1
sess = ort.InferenceSession(gzip.open(a.onnx).read(), so, providers=['CPUExecutionProvider'])
y = sess.run(None, {sess.get_inputs()[0].name: x.reshape((1,) + shape)})[0].reshape(-1)
with open(os.path.join(a.out, 'witness_v2.txt'), 'w') as f:
    f.write('sat\n')
    f.write('X float32 [1, %s]\n' % ', '.join(str(s) for s in shape))
    for val in flat: f.write(repr(float(val)) + '\n')
    f.write('Y float32 [1, %d]\n' % y.size)
    for val in y: f.write(repr(float(val)) + '\n')
print('pw', pw, 'target', tgt, 'argmax', int(y.argmax()), 'y[target]', float(y[tgt]), 'y[argmax]', float(y.max()), 'margin', float(y.max() - y[tgt]),
      'n changed coords', int((d != 0).sum()), 'min dist to bound', float(min((x - lo).min(), (hi - x).min())))
