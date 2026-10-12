"""Bipartite route-chart lift (controller generators outside an index-2 subgroup), diameter target Db=5, with the
fast rank proxy: even elements need a full-rank (rank s) reduced word of length Db-1, odd elements a rank-s reduced
word of length Db. Chart SA on the proxy; whenever the proxy is small, the exact BFS defect (cap Db, q^s sources)
decides. Usage: bip_proxy_search.py --group G --gens '[a,b,c]' --minutes M --out F
"""
import sys, os, json, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import rcl, rcl2, rankproxy, rcl_bip

ap = argparse.ArgumentParser()
ap.add_argument('--group', required=True); ap.add_argument('--gens', required=True)
ap.add_argument('--q', type=int, default=3); ap.add_argument('--s', type=int, default=4); ap.add_argument('--Db', type=int, default=5)
ap.add_argument('--minutes', type=float, default=30); ap.add_argument('--seed', type=int, default=1)
ap.add_argument('--iters', type=int, default=6000); ap.add_argument('--thresh', type=int, default=0)
ap.add_argument('--out'); ap.add_argument('--spec', default='pair3,pair3,inv3')
a = ap.parse_args()
rng = np.random.default_rng(a.seed)
H = rcl2.parse_group(a.group); n = H['n']; mul = H['mul'].astype(np.int64)
par = rcl_bip.parity_vec(H, a.group)
gens = json.loads(a.gens)
spec = rcl2.parse_spec(a.spec)
q, s, Db = a.q, a.s, a.Db
letters = np.array([gens[0], H['inv'](gens[0]), gens[1], H['inv'](gens[1]), gens[2]], dtype=np.int64)
linv = [1, 0, 3, 2, 4]
wE = rankproxy.reduced_words(Db - 1, linv); eE = rankproxy.endpoints(wE, letters, mul)
wO = rankproxy.reduced_words(Db, linv); eO = rankproxy.endpoints(wO, letters, mul)
hasE = np.zeros(n, bool); hasE[eE] = True
hasO = np.zeros(n, bool); hasO[eO] = True
targetE = (par == 0) & hasE; targetE[0] = False
targetO = (par == 1) & hasO
print(json.dumps(dict(group=a.group, n=n, N=n * q ** s, even_targets=int(targetE.sum()), odd_targets=int(targetO.sum()),
                      even_without_len4=int(((par == 0) & ~hasE).sum()) - 1, odd_without_len5=int(((par == 1) & ~hasO).sum()))), flush=True)
lift = rcl2.Lift(H, spec, gens, q, s, Db - 1, rng)


def exact():
    nbr = lift.build()
    return int(rcl.g_defect(nbr, lift.sources, Db)[0])


def proxy(chart):
    As, bs = rankproxy.expand_chart(chart, spec, q)
    rE = rankproxy.word_ranks(wE, As, bs, q); rO = rankproxy.word_ranks(wO, As, bs, q)
    covE = np.zeros(n, bool); covE[eE[rE == s]] = True
    covO = np.zeros(n, bool); covO[eO[rO == s]] = True
    return int((targetE & ~covE).sum() + (targetO & ~covO).sum())


t_end = time.time() + 60 * a.minutes
best = None
for rs in range(100000):
    if time.time() > t_end:
        break
    lift.chart = [lift.rand_chart(i) for i in range(3)]
    cur = proxy(lift.chart); T = 2.0
    for it in range(a.iters):
        if cur <= a.thresh or time.time() > t_end:
            break
        i = int(rng.integers(3)); old = lift.chart[i]
        lift.tweak(i)
        new = proxy(lift.chart)
        if new <= cur or rng.random() < np.exp(-(new - cur) / T):
            cur = new
        else:
            lift.chart[i] = old
        T = max(T * 0.998, 0.05)
    d = exact()
    print(json.dumps(dict(restart=rs, proxy=cur, exact=d)), flush=True)
    if best is None or d < best[0]:
        best = (d, lift.state())
        if a.out:
            json.dump(dict(best=d, state=best[1]), open(a.out, 'w'))
    if d == 0:
        print(json.dumps(dict(FOUND=True, N=n * q ** s)), flush=True)
        break
print(json.dumps(dict(final=best[0] if best else None)), flush=True)
