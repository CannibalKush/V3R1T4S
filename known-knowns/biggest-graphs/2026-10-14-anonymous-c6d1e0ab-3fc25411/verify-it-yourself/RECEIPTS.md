# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0):

```text
sha256 matches INDEX.csv (3fc25411941fa666946464317bc9672386a4923bcb01a24e2c42ec7239b8c3a4)
== check_dd.py on object/G_14_3_N1117.edges
N=1117 edges=7785 degree histogram=[(13, 68), (14, 1049)] max degree=14 exact diameter=3 (BFS from all 1117 vertices) Moore bound=2563
PASS (Delta,D)=(14,3) N=1117 max_degree=14 diameter=3
== negative control: a corrupted copy must FAIL
negative control rejected as expected (FAIL an isolated vertex (or a gap in the vertex numbering))
ALL CHECKS PASS
```
