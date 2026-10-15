# Workspace checker timeout

`--timeout N` sets the seconds passed to each package checker invocation, both through `--package DIR` and when checking workspace outbox packages (including `--setup` and a selected `--run`). The default remains 900. Each clean and corrupted-copy invocation receives the same configured timeout; this is not a total-workspace deadline. `--no-exec` still prevents package checker execution.

Before this change, direct package checks respected the option but workspace mode silently used 900 even when a different value was explicitly requested. The fix only forwards the value through `main` and `check_workspace`; it does not change subprocess behavior or verifier acceptance rules.

Run the standard-library suite from the repository root:

    python3 -m unittest discover -s kit/tests -p 'test_*.py' -v

Focused tests mock package checker execution and the read-only Git probe. They cover package/workspace/setup/selected-run modes, multiple outbox packages, the unchanged default, and --no-exec. No scientific or third-party submission scripts are needed.

This is standalone on upstream main; no other toolkit-fix PR is required. It adds no stdout byte cap, process-group or descendant-cleanup implementation, security sandbox, or infrastructure-error recovery. Existing per-process timeout and temporary-copy behavior remain unchanged. Runtime tests were performed on Linux/Python 3.12.

Before integration, maintainers must reconcile root `SHA256SUMS` against the complete final tree, including coverage and hashes for the changed checker, new test, and this README. The release manifest is intentionally unchanged in the draft; local tests and independent review are not remote CI or release qualification.
