# Package mutation diagnostics

Run from the repository root:

    python3 -m unittest discover -s kit/tests -p 'test_*.py' -v

The focused regression suite mocks subprocess results and uses a tiny synthetic
object. It never executes third-party submission scripts or scientific checkers.
The existing checker suite also uses locally generated synthetic fixtures.

After a successful clean package run, a corrupted copy is reported as rejected
when the checker exits with a positive status and its last nonempty line is
exactly `FAIL`, as specified in `kit/SUBMIT.md`. Timeout, launch failure, missing
shell, negative signal status, empty output and malformed output are inconclusive.
Contradictory zero-exit `FAIL` and nonzero-exit `PASS` are inconclusive too.

Positive statuses are not reserved by the package protocol. Even 126, 127 or 139
with terminal `FAIL` is therefore treated as rejection; an arbitrary checker can
use these as ordinary exit codes. A shell-wrapped crash or missing dependency
that itself leaves terminal `FAIL` is indistinguishable from a protocol rejection.
This probe checks the declared protocol, not the scientific meaning of rejection.

The focused tests cover ordinary and unusual positive rejection codes, CRLF and
trailing blank lines, infrastructure failures (including the real runner's mocked
timeout and launch-error paths), malformed output, corrupted `PASS`, and clean
failure before mutation. Existing word-PASS matching remains unchanged; stricter
PASS matching belongs to the separate confirmation-gate work.

This revision is based on upstream main
`371938deefd77b9e6a95d2a0c3e2d3c6ead7eaac`, preserving its UTF-8/CRLF fixes,
merged null-control validation and source-placeholder handling. The root
`SHA256SUMS` is intentionally left to the maintainer to refresh for the final tree.
