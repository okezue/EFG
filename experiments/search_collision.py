from __future__ import annotations
import argparse, json, sys
from collections import defaultdict
from pathlib import Path
import networkx as nx
from motifwl.wl import edge_motif_signatures, wl2_signatures, graph6


def signatures(graphs, mode):
    if mode == "2wl":
        return wl2_signatures(graphs)
    return edge_motif_signatures(graphs, mode)


def read_g6(path):
    with open(path, "rb") as f:
        return [nx.convert_node_labels_to_integers(G) for G in nx.read_graph6(f)]


def main():
    ap = argparse.ArgumentParser(description="Collision search: weaker-mode signature buckets, then test stronger-mode split inside each bucket. O(N) not O(N^2).")
    ap.add_argument("--graph6-file", required=True)
    ap.add_argument("--weaker", required=True)
    ap.add_argument("--stronger", required=True)
    ap.add_argument("--out", default="results/collision.jsonl")
    args = ap.parse_args()
    gs = read_g6(args.graph6_file)
    if len(gs) < 2:
        return
    wsig = signatures(gs, args.weaker)
    buckets = defaultdict(list)
    for i, s in enumerate(wsig):
        buckets[s].append(i)
    out_path = Path(args.out); out_path.parent.mkdir(parents=True, exist_ok=True)
    found = checked = 0
    with out_path.open("w") as out:
        for s, idx in buckets.items():
            if len(idx) < 2:
                continue
            sub = [gs[i] for i in idx]
            ssig = signatures(sub, args.stronger)
            by = defaultdict(list)
            for k, ss in enumerate(ssig):
                by[ss].append(idx[k])
            if len(by) < 2:
                continue
            reps = [v[0] for v in by.values()]
            for a in range(len(reps)):
                for b in range(a + 1, len(reps)):
                    checked += 1
                    G, H = gs[reps[a]], gs[reps[b]]
                    rec = {"n": G.number_of_nodes(), "m": G.number_of_edges(),
                           "weaker": args.weaker, "stronger": args.stronger,
                           "G_graph6": graph6(G), "H_graph6": graph6(H),
                           "connected": nx.is_connected(G) and nx.is_connected(H)}
                    out.write(json.dumps(rec) + "\n"); out.flush()
                    print(json.dumps(rec)); found += 1
    print(f"graphs={len(gs)} witness_pairs={found}", file=sys.stderr)


if __name__ == "__main__":
    main()
