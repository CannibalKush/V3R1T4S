#!/bin/sh
# Level-1 verification of the shipped Lehmer branch logs (python3 only, about 2 minutes).  Exit 0 iff all pass.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
SECTION=known-knowns/lehmer-past-10-to-the-50
require() {  # input files must be present
  for o in "$@"; do
    [ -f "$HERE/$o" ] || { echo "missing $SECTION/$o"; exit 2; }
  done
}
require branch_logs/lcrt5_1e50_LCRT4_tasks.tar.gz branch_logs/lcrt6_1e50_bigsieve_LCRT6_tasks.tar.gz \
        branch_logs/vlrt2_full50_union.tasks.jsonl.gz
TMP=${TMPDIR:-/tmp}/v3r1t4s-lehmer.$$
mkdir -p "$TMP"; fail=0
echo "== analytic closures (exact rationals)"
python3 "$HERE/verify-it-yourself/closures.py" 50 || fail=1
echo "== unpack branch logs"
tar xzf "$HERE/branch_logs/lcrt5_1e50_LCRT4_tasks.tar.gz" -C "$TMP" || fail=1
tar xzf "$HERE/branch_logs/lcrt6_1e50_bigsieve_LCRT6_tasks.tar.gz" -C "$TMP" || fail=1
tar xzf "$HERE/branch_logs/lbb2_e50_S1000000000_tasks.tar.gz" -C "$TMP" || fail=1
expect() {  # json-line-on-stdin key expected
  python3 -c "import json,sys; d=json.loads(sys.stdin.read()); v=str(d['$1']); ok=(v=='$2'); print('  $1 =',v,'' if ok else '  <-- EXPECTED $2'); sys.exit(0 if ok else 1)"
}
check_summary() {  # run [extra args]
  out=$(python3 "$HERE/verify-it-yourself/recompute_summary.py" "$@") || fail=1
  for kv in nodes_total=2169013803 live_total=130205304 euler_closed_total=102312897 euler_pass_total=0 c2_int_total=0 \
            kfilt_total=25849618340 max_q_seen=43725458932 n_events=0 digest=74e2002af271a197 digest_live=7c1d8e5190f9754f \
            task_lines=65647 duplicate_conflicts=0; do
    echo "$out" | expect "${kv%%=*}" "${kv#*=}" || fail=1
  done
}
echo "== author run, mode LCRT-4"; check_summary "$TMP/lcrt5_1e50"
echo "== author run, mode LCRT-6"; check_summary "$TMP/lcrt6_1e50_bigsieve"
echo "== independent engine vlrt2, all 65647 subtrees"; check_summary "$HERE/branch_logs/vlrt2_full50_union.tasks.jsonl.gz" --top "$HERE/branch_logs/vlrt2_r50c.summary.json"
echo "== subtree-by-subtree diffs"
python3 "$HERE/verify-it-yourself/diff_runs.py" "$TMP/lcrt5_1e50" "$TMP/lcrt6_1e50_bigsieve" --maxq || fail=1
python3 "$HERE/verify-it-yourself/diff_runs.py" "$HERE/branch_logs/vlrt2_full50_union.tasks.jsonl.gz" "$TMP/lcrt5_1e50" || fail=1
python3 "$HERE/verify-it-yourself/diff_runs.py" "$HERE/branch_logs/vlrt2_full50_union.tasks.jsonl.gz" "$TMP/lcrt6_1e50_bigsieve" || fail=1
echo "== independent engine lbb2, completeness"
python3 "$HERE/verify-it-yourself/lbb2_aggregate.py" "$TMP/e50_S1000000000" || fail=1
rm -rf "$TMP"
[ $fail = 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECK FAILED"
exit $fail
