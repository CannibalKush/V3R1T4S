# How we built it

- `sa.py`: slice and absorb. It loads a scheme, ranks slice directions by the terms they remove, slices, then absorbs exact dependencies across the three factor pairings until none removes a term.
- `sweep.py`: runs `sa.py` along every axis of a parent and compares each child with the bars.
- `PREREG.md`: the pre-registration, with its timing note.

Requirements: Python 3.9 or later with `numpy==2.0.2` and `python-flint==0.6.0`. Only the search needs them; the checker in `../verify-it-yourself/` uses the standard library. The parent is Perminov's `schemes/results/Q/12x13x16_m1509_Q.json` (sha256 f4343e3746fd8f64a7ec7db07eefe65b470feb00d593e4897d24d755c000eef4), downloaded from https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/Q/12x13x16_m1509_Q.json and not redistributed here. See `../RUN_IT_YOURSELF.md` for the commands.
