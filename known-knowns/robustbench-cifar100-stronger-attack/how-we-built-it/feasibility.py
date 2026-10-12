"""
feasibility.py -- exact_feasible(): repairs float32 rounding so that max|x_adv - x| <= 8/255 holds EXACTLY in float64
(against the float32 ToTensor images) and 0 <= x_adv <= 1.  Used by multistart.py and assemble.py (stage 6).
(In the original run this function lived in the stage-6 author's own checker script; it is copied here unchanged.)
"""
import numpy as np

EPS = 8.0 / 255.0


def exact_feasible(xa, x):
    """xa, x float32 arrays of equal shape. Returns a float32 copy with |xa - x| <= 8/255 exactly in float64, [0,1]."""
    xa = xa.astype(np.float32, copy=True)
    x64 = x.astype(np.float64)
    for it in range(8):
        d = xa.astype(np.float64) - x64
        over = np.abs(d) > EPS
        if not over.any():
            break
        if it == 0:   # re-cast the exact float64 bound to float32 (nearest), then walk toward x one ulp at a time
            target = (x64 + np.sign(d) * EPS).astype(np.float32)
            xa[over] = target[over]
        else:
            xa[over] = np.nextafter(xa[over], x[over]).astype(np.float32)
    np.clip(xa, 0.0, 1.0, out=xa)
    d = np.abs(xa.astype(np.float64) - x64)
    assert not (d > EPS).any(), 'exact_feasible failed'
    return xa
