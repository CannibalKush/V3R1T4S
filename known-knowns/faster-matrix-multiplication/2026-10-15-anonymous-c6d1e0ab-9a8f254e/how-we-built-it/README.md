# How we built it

- `REBUILD.md`: the deterministic recipe from the published LITA parent to this scheme (parent URL and sha256, every slice direction and absorption setting, expected output sha256, and the clean-directory test).
- `rebuild.py` with `rebuild.json` and `engine_manifest.json`: the one-command rebuild and the pinned engine files it runs (`engine/`: the exact slice-and-absorb engine, Python plus two small C++ kernels, every file's sha256 in the manifest).
- `rebuild_test_output.txt`: real output of the clean-directory test.
- `PREREG.md`: the pre-registration, with its timing note.

Requirements: Python 3.9 or later with `numpy==2.0.2` and `python-flint==0.6.0`, and a C++17 compiler. Only the rebuild needs them; the checker in `../verify-it-yourself/` uses the standard library. The LITA parent file is downloaded from https://github.com/khoruzhii/lita as `REBUILD.md` states and is not redistributed here.
