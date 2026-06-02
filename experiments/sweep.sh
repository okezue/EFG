#!/usr/bin/env bash
# Sharded exhaustive sweep: for each n in [NMIN..NMAX], generate all graphs with
# geng, shard by edge count, and run search_pairs on every (n,e) bucket in
# parallel. A bucket = one (n,m) group, so all candidate pairs live inside it.
# Usage: sweep.sh WEAKER STRONGER NMIN NMAX [PROCS] [GENG_FLAGS]
set -euo pipefail
W=${1:?weaker mode}; S=${2:?stronger mode}; NMIN=${3:?nmin}; NMAX=${4:?nmax}
P=${5:-$(nproc)}; GFLAGS=${6:-}
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; export PYTHONPATH="$ROOT"
SHARD="$ROOT/results/shards/${W}__${S}"; OUT="$ROOT/results/${W}__${S}"
mkdir -p "$SHARD" "$OUT"
gen() {
  local n=$1 e=$2 f="$SHARD/n${n}_e${e}.g6"
  geng -q $GFLAGS "$n" "${e}:${e}" > "$f" 2>/dev/null || true
  [ -s "$f" ] || { rm -f "$f"; return; }
  python "$ROOT/experiments/search_collision.py" --graph6-file "$f" \
    --weaker "$W" --stronger "$S" --out "$OUT/n${n}_e${e}.jsonl" 2>>"$OUT/log.txt"
  rm -f "$f"
}
export -f gen; export SHARD OUT ROOT W S GFLAGS PYTHONPATH
for n in $(seq "$NMIN" "$NMAX"); do
  emax=$(( n*(n-1)/2 ))
  seq 0 "$emax" | xargs -P "$P" -I{} bash -c 'gen "$0" "{}"' "$n"
  echo "n=$n done: $(cat "$OUT"/n${n}_e*.jsonl 2>/dev/null | wc -l) witnesses so far"
done
echo "SWEEP COMPLETE $W vs $S"
cat "$OUT"/*.jsonl 2>/dev/null | sort -t, -k1 | head
