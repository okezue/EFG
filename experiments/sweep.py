from __future__ import annotations
import argparse, json, subprocess, sys, time
from collections import defaultdict
from functools import partial
from multiprocessing import Pool
import networkx as nx
from motifwl.wl import canonical_edge_motif_signature as csig, graph6


def _sig(g6: str, mode: str):
    return csig(nx.from_graph6_bytes(g6.encode()), mode)


def geng_graphs(n: int, e: int, connected: bool):
    cmd = ["geng", "-q"] + (["-c"] if connected else []) + [str(n), f"{e}:{e}"]
    out = subprocess.run(cmd, capture_output=True).stdout.decode().split()
    return out  # list of graph6 strings


def main():
    ap = argparse.ArgumentParser(description="Parallel exhaustive collision sweep over geng output.")
    ap.add_argument("--weaker", required=True)
    ap.add_argument("--stronger", required=True)
    ap.add_argument("--nmin", type=int, required=True)
    ap.add_argument("--nmax", type=int, required=True)
    ap.add_argument("--procs", type=int, default=0)
    ap.add_argument("--connected", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    pool = Pool(args.procs or None)
    total_found = 0
    with open(args.out, "w") as outf:
        for n in range(args.nmin, args.nmax + 1):
            emax = n * (n - 1) // 2
            t0 = time.time()
            n_found = 0
            for e in range(emax + 1):
                g6s = geng_graphs(n, e, args.connected)
                if len(g6s) < 2:
                    continue
                wsigs = pool.map(partial(_sig, mode=args.weaker), g6s, chunksize=64)
                buckets = defaultdict(list)
                for i, s in enumerate(wsigs):
                    buckets[s].append(i)
                coll = [idx for idx in buckets.values() if len(idx) > 1]
                for idx in coll:
                    by = defaultdict(list)
                    for i in idx:
                        by[_sig(g6s[i], args.stronger)].append(i)
                    if len(by) < 2:
                        continue
                    reps = [v[0] for v in by.values()]
                    for a in range(len(reps)):
                        for b in range(a + 1, len(reps)):
                            G, H = g6s[reps[a]], g6s[reps[b]]
                            rec = {"n": n, "m": e, "weaker": args.weaker, "stronger": args.stronger,
                                   "G_graph6": G, "H_graph6": H}
                            outf.write(json.dumps(rec) + "\n"); outf.flush()
                            print(json.dumps(rec)); n_found += 1; total_found += 1
            print(f"n={n} done in {time.time()-t0:.1f}s witnesses={n_found}", file=sys.stderr); sys.stderr.flush()
    pool.close(); pool.join()
    print(f"SWEEP COMPLETE {args.weaker} vs {args.stronger}: total_witnesses={total_found}", file=sys.stderr)


if __name__ == "__main__":
    main()
