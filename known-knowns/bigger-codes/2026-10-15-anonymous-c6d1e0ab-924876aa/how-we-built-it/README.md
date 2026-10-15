# How we built it

- `rebuild.py`: regenerates the generator matrix from its polynomial description (standard library) and compares it with the shipped object. This is the reproducible build.
- `qcs.c`: the quasi-cyclic search program (one generator, index p, exact distance by orbit enumeration), at its packaging-time version; the exhaustive scan mode that found this code is a later extension of it.
- `PREREG.md`: the pre-registration, with its timing note.

The C program is shipped for transparency; compile with any C99 compiler (`cc -O2 -o qcs qcs.c`). The claim does not depend on it.
