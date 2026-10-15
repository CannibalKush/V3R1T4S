# How we built it

- `rebuild.py`: regenerates the generator matrix from its six parameters (standard library) and compares it with the shipped object. This is the reproducible build.
- `qcs.c`: the quasi-cyclic search program (one generator, index p, exact distance by orbit enumeration), at its packaging-time version.
- `killcols.c`: the column-covering search that picks the added columns, at its packaging-time version.
- `PREREG.md`: the pre-registration, with its timing note.

The two C programs are shipped for transparency; compile with any C99 compiler (`cc -O2 -o qcs qcs.c`). The claim does not depend on them.
