#!/bin/zsh
# Public-chain rebuild of the 2105 candidate: codex's pinned rebuild (LITA 17 npz -> step 4 = 15x16x16 r2176,
# SHA c67b34f2...) followed by my deterministic last step, compared term by term with the candidate scheme.
cd [the opus_step folder]
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=python3
D=work/r2/pubchain_run
mkdir -p $D
nice -n 19 perl -e 'alarm shift; exec @ARGV' 1900 $PY ../rebuild.py --work-dir $PWD/$D/codex_chain > $D/codex_chain.log 2>&1
P=$(ls $D/codex_chain/step_04_*_r2176.json)
nice -n 19 perl -e 'alarm shift; exec @ARGV' 900 $PY rebuild_step.py $P --parent-sha c67b34f2d0c763379b993754f0a2f304df65bbb1eb6b22235ce8a6c2351ff659 --axis 2 --f '[[1,1]]' --e '[[1,1],[10,1]]' --seed 2 --out $PWD/$D/rebuilt_2105.json --compare candidates/15x15x16_r2105/scheme.json > $D/step5_2105.log 2>&1
nice -n 19 perl -e 'alarm shift; exec @ARGV' 900 $PY rebuild_step.py $P --parent-sha c67b34f2d0c763379b993754f0a2f304df65bbb1eb6b22235ce8a6c2351ff659 --axis 2 --f '[[1,1]]' --e '[[1,1]]' --seed 0 --out $PWD/$D/rebuilt_2106.json --compare candidates/15x15x16_r2106/scheme.json > $D/step5_2106.log 2>&1
echo PUBCHAIN DONE
