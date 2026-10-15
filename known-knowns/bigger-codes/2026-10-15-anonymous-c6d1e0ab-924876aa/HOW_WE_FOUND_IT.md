# How we found it (contributor text, unverified)

The claim rests only on `object/code_q2_n213_k26_d77.json` and the checker in `verify-it-yourself/`.

1. **Where to look.** In the codetables.de binary table the k = 26 row is flat at lower bound 76 for lengths 210 to 213. A length-210 code with distance 76 whose codimension-3 subcode has distance 77 leaves exactly three columns for a Construction X lift to 77.
2. **Exhaustive scan.** For circulant size m = 105 and every degree-26 divisor h of x^105 - 1, an exhaustive scan over all multiplier classes f (up to block shift) of one-generator index-2 quasi-cyclic codes evaluated, for each code reaching distance 76, whether a submodule subcode avoiding all weight-76 words exists. The pair (h = 0x73921a7, f = 0x2d547) is one of twelve multipliers for that h where the subcode {a : (x^3+x^2+1) | a} has distance 77.
3. **Construction X.** Appending the three columns a mod (x^3+x^2+1) gives [213, 26, 77]. The code was then rebuilt independently in pure Python from the polynomial description and its distance computed by three full enumerations.

The scan programs are in `how-we-built-it/` for transparency (the versions at packaging time). The deterministic `rebuild.py` there, not the scan, regenerates the object.
