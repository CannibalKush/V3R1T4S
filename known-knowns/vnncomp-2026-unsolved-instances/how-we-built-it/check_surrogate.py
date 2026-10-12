"""Check the exact integer model (bnn.BNN30) against onnxruntime on the real ONNX model: the pre-softmax MatMul output
of onnxruntime (CPU, float32) must equal the integer logits exactly, at each box centre, at 20 random integer points
and at 20 random real points strictly inside each box (numpy seed 0). Also prints the centre statistics used to size
the search (true class, best other class, logit gap, number of first-layer neurons with |preactivation| <= 26).

Run from the family directory after `python3 verify-it-yourself/vnncheck.py --cache downloads`:
  python3 -I how-we-built-it/check_surrogate.py
Expected last line: max |ort MatMul - surrogate logits| over all tests: 0.0
"""
import argparse, os, sys
import numpy as np
import onnx, onnxruntime as ort
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bnn import BNN30, parse_box, load_onnx

BENCH = 'downloads/benchmarks/traffic_signs_recognition_2023/2.0'
ap = argparse.ArgumentParser()
ap.add_argument('--onnx', default=f'{BENCH}/onnx/3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.onnx.gz')
ap.add_argument('--vnnlib', nargs='+', default=[f'{BENCH}/vnnlib/model_30_idx_1703_eps_1.00000.vnnlib.gz',
                                                f'{BENCH}/vnnlib/model_30_idx_178_eps_1.00000.vnnlib.gz'])
args = ap.parse_args()

net = BNN30(args.onnx)
# real model with the pre-softmax MatMul exposed as an extra output (used only for this comparison)
m = load_onnx(args.onnx)
mm_name = [n.output[0] for n in m.graph.node if n.op_type == 'MatMul'][0]
m.graph.output.extend([onnx.helper.make_tensor_value_info(mm_name, onnx.TensorProto.FLOAT, None)])
so = ort.SessionOptions(); so.intra_op_num_threads = 1; so.inter_op_num_threads = 1
sess_dbg = ort.InferenceSession(m.SerializeToString(), so, providers=['CPUExecutionProvider'])
in_name = sess_dbg.get_inputs()[0].name


def ort_logits(x_hwc):
    y, L = sess_dbg.run(None, {in_name: np.asarray(x_hwc, dtype=np.float32).reshape(1, 30, 30, 3)})
    return y.reshape(-1), L.reshape(-1)


rng = np.random.default_rng(0)
max_dev = 0.0
for path in args.vnnlib:
    key = os.path.basename(path).split('.vnnlib')[0]
    lo, hi, tgt = parse_box(path)
    v = ((lo + hi) / 2).astype(np.int64)
    a1, h1, a2, h2, L = net.forward_int(v)
    y, Lo = ort_logits(v)
    dev = float(np.abs(Lo - L).max()); max_dev = max(max_dev, dev)
    unst1 = int((np.abs(a1) <= 26).sum())
    others = np.delete(L, tgt)
    print(f'{key}: target {tgt}, centre L_t={L[tgt]}, best other class {np.delete(np.arange(43), tgt)[others.argmax()]} at {others.max()}, gap {L[tgt]-others.max()}, '
          f'layer1 |a|<=26: {unst1}, layer1 |a|<=27: {int((np.abs(a1) <= 27).sum())}, a2 in [{a2.min()},{a2.max()}], ort-vs-int max dev {dev:.2e}, ort y_t={y[tgt]:.6f}')
    # random integer points in the box
    for _ in range(20):
        x = v + rng.integers(-1, 2, size=v.shape)
        _, _, _, _, L2 = net.forward_int(x)
        _, Lo2 = ort_logits(x)
        max_dev = max(max_dev, float(np.abs(Lo2 - L2).max()))
    # random real points strictly inside
    for _ in range(20):
        x = (v + rng.uniform(-0.99, 0.99, size=v.shape)).astype(np.float32)
        _, _, _, _, L2 = net.forward_int(x.astype(np.float64))
        _, Lo2 = ort_logits(x)
        max_dev = max(max_dev, float(np.abs(Lo2 - L2).max()))
print('max |ort MatMul - surrogate logits| over all tests:', max_dev)
