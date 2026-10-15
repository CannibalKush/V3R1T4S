# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. To run the checker alone:

```sh
python3 verify-it-yourself/check_dd.py object/G_14_3_N1117.edges --delta 14 --diameter 3 --expect-n 1117
```

It reads the 0-indexed edge list. It checks that there are no loops, no repeated edges and no unused vertex numbers, and that the maximum degree is at most 14. It then runs a breadth-first search from every one of the 1117 vertices and reports the exact diameter, which must be at most 3, along with the Moore bound. The run script also checks the sha256 against `INDEX.csv`, and checks that a copy with vertex 0's edges deleted is rejected.

## 2. How the object was built

`how-we-built-it/` holds the original run's optimizer (`sa2_opt.c`) and its pre-registration (`PREREG.md`). The commands below are as the original run recorded them. The starting graph is the public Dhar_1116 adjacency list, which is not redistributed here:
https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/adjacencies/adjD3/deg14_diam3_n1116_adjlist.txt

```sh
cc -O3 -o sa2_opt how-we-built-it/sa2_opt.c -lm
./sa2_opt deg14_diam3_n1116_adjlist.txt 14 3 1 G_14_3 300000 10 1
```

The original run reports that restart 1 (seed 1) reached zero vertex pairs at distance more than 3 in 11.5 seconds. We did not re-run it; this claim rests only on the object and the checker above.
