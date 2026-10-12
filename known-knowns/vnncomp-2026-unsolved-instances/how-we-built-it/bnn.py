"""Exact integer model of the VNN-COMP traffic_signs_recognition_2023 binarized network
3_30_30_QConv_16_3_QConv_32_2_Dense_43_ep_30.

The ONNX graph is: NHWC input -> Transpose -> Conv(+-1 weights) -> Transpose -> [Sign -> Add 0.1 -> Sign]
-> ... -> Reshape -> [Sign, Add, Sign] -> MatMul(+-1) -> Softmax.
Sign(a) then +0.1 then Sign means h = +1 if a >= 0 else -1.

Everything here is integer arithmetic (numpy int64) so it is exact. The float32 replay of the real ONNX model is
exact too for the inputs built by pixel_map(): every input is a multiple of 2^-(pw+1) with |x| <= 255, so each
first-layer partial sum (27 terms of +-x) is a multiple of 2^-(pw+1) below 2^13 in magnitude and is representable in
float32; later layers are sums of +-1 (|.| <= 23328 < 2^24). check_surrogate.py compares this model with onnxruntime.
"""
from __future__ import annotations
import gzip, io, re
import numpy as np
import onnx
from onnx import numpy_helper


def load_onnx(path):
    data = gzip.open(path).read() if path.endswith('.gz') else open(path, 'rb').read()
    return onnx.load(io.BytesIO(data))


def conv_valid(x, w):
    """x: (C,H,W) int64 ; w: (O,C,kh,kw) int64 ; stride 1, no padding."""
    O, C, kh, kw = w.shape
    H, Wd = x.shape[1:]
    out = np.zeros((O, H - kh + 1, Wd - kw + 1), dtype=np.result_type(x.dtype, w.dtype))
    for i in range(kh):
        for j in range(kw):
            out += np.tensordot(w[:, :, i, j], x[:, i:i + H - kh + 1, j:j + Wd - kw + 1], axes=([1], [0]))
    return out


class BNN30:
    """The 3_30_30 net: conv1 16x3x3x3 -> sign -> conv2 32x16x2x2 -> sign -> flatten(NHWC) -> dense 23328x43 -> softmax."""

    def __init__(self, onnx_path):
        m = load_onnx(onnx_path)
        W = {t.name: numpy_helper.to_array(t) for t in m.graph.initializer}
        self.w1 = [v for v in W.values() if v.shape == (16, 3, 3, 3)][0].astype(np.int64)
        self.w2 = [v for v in W.values() if v.shape == (32, 16, 2, 2)][0].astype(np.int64)
        self.w3 = [v for v in W.values() if v.shape == (23328, 43)][0].astype(np.int64)
        assert set(np.unique(self.w1)) <= {-1, 1} and set(np.unique(self.w2)) <= {-1, 1} and set(np.unique(self.w3)) <= {-1, 1}
        self.model = m

    def forward_int(self, x_hwc):
        """x_hwc: (30,30,3) integer array (or float array; conv is then done in float64)."""
        if np.issubdtype(np.asarray(x_hwc).dtype, np.integer):
            x = np.asarray(x_hwc).transpose(2, 0, 1).astype(np.int64)
            a1 = conv_valid(x, self.w1)
        else:
            x = np.asarray(x_hwc, dtype=np.float64).transpose(2, 0, 1)
            a1 = conv_valid(x, self.w1.astype(np.float64))
        h1 = np.where(a1 >= 0, 1, -1).astype(np.int64)
        a2 = conv_valid(h1, self.w2)                      # (32,27,27)
        h2 = np.where(a2 >= 0, 1, -1).transpose(1, 2, 0).reshape(-1)  # NHWC flatten
        logits = h2 @ self.w3
        return a1, h1, a2, h2, logits


def parse_box(vnnlib_path, shape=(30, 30, 3)):
    txt = gzip.open(vnnlib_path).read().decode() if vnnlib_path.endswith('.gz') else open(vnnlib_path).read()
    lo = np.full(shape, np.nan); hi = np.full(shape, np.nan)
    for mm in re.finditer(r'\(assert \((<=|>=) X\[0,(\d+),(\d+),(\d+)\] ([-0-9.eE]+)\)\)', txt):
        a = (int(mm.group(2)), int(mm.group(3)), int(mm.group(4)))
        (hi if mm.group(1) == '<=' else lo)[a] = float(mm.group(5))
    assert not np.isnan(lo).any() and not np.isnan(hi).any()
    tgt = int(re.search(r'\(>= Y\[0,\d+\] Y\[0,(\d+)\]\)', txt).group(1))
    return lo, hi, tgt


def softmax64(L):
    L = np.asarray(L, dtype=np.float64)
    e = np.exp(L - L.max())
    return e / e.sum()


def pixel_map(lo, hi, pw=9):
    """Per-pixel affine map x = v + off + m*d keeping x strictly inside [lo, hi] for every integer d in [dmin, dmax].
    v = floor((lo+hi)/2) (integer in [lo,hi]); m = 1 - 2^-pw; off = +2^-(pw+1) if v == lo, -2^-(pw+1) if v == hi, else 0.
    Boundary check: d = dmin = lo - v gives x - lo = 2^-pw*(v-lo) + off > 0; d = dmax gives hi - x = 2^-pw*(hi-v) - off > 0.
    All x are multiples of 2^-(pw+1) with |x| <= 255 -> exactly representable in float32 (pw+1+8 <= 23 bits)."""
    lo = np.asarray(lo, dtype=np.float64); hi = np.asarray(hi, dtype=np.float64)
    assert np.all(lo == np.round(lo)) and np.all(hi == np.round(hi)) and np.all(hi > lo)
    v = np.floor((lo + hi) / 2)
    m = 1.0 - 2.0 ** -pw
    off = np.where(v == lo, 2.0 ** -(pw + 1), np.where(v == hi, -2.0 ** -(pw + 1), 0.0))
    dmin = (lo - v).astype(np.int64); dmax = (hi - v).astype(np.int64)
    # verify strictness at both extremes
    xlo = v + off + m * dmin; xhi = v + off + m * dmax
    assert np.all(xlo > lo) and np.all(xhi < hi)
    return v.astype(np.int64), off, m, dmin, dmax
