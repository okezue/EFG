from __future__ import annotations

import argparse, json, random, sys
from collections import defaultdict
from pathlib import Path
import networkx as nx

from motifwl.wl import edge_motif_equiv, wl2_equiv, graph6


def graph_atlas(max_n: int, connected: bool):
    for G in nx.graph_atlas_g():
        if G.number_of_nodes() == 0 or G.number_of_nodes() > max_n:
            continue
        if connected and not nx.is_connected(G):
            continue
        yield nx.convert_node_labels_to_integers(G)


def read_graph6_file(path: str):
    with open(path, "rb") as f:
        for G in nx.read_graph6(f):
            yield nx.convert_node_labels_to_integers(G)


def group_graphs(graphs):
    groups = defaultdict(list)
    for G in graphs:
        groups[(G.number_of_nodes(), G.number_of_edges())].append(G)
    return groups


def relation_holds(G, H, weaker: str, stronger: str, simple_squares: bool):
    # Returns True if weaker identifies the pair and stronger separates it.
    if weaker == "2wl":
        weak_eq = wl2_equiv(G, H)
    else:
        weak_eq = edge_motif_equiv(G, H, weaker, simple_squares=simple_squares)
    if stronger == "2wl":
        strong_eq = wl2_equiv(G, H)
    else:
        strong_eq = edge_motif_equiv(G, H, stronger, simple_squares=simple_squares)
    return weak_eq and not strong_eq


def main():
    ap = argparse.ArgumentParser(description="Search graph pairs separated by one WL mode but not another.")
    ap.add_argument("--source", choices=["atlas", "graph6"], default="atlas")
    ap.add_argument("--graph6-file", type=str, default=None)
    ap.add_argument("--max-n", type=int, default=7)
    ap.add_argument("--connected", action="store_true")
    ap.add_argument("--weaker", required=True, help="Mode expected to identify the pair, e.g. tri, square2, tri_square1")
    ap.add_argument("--stronger", required=True, help="Mode expected to separate the pair, or 2wl")
    ap.add_argument("--limit-pairs", type=int, default=0, help="0 means no limit")
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--walk-squares", action="store_true", help="Allow degenerate length-3 walks instead of simple 4-cycles")
    ap.add_argument("--out", type=str, default="results/search_results.jsonl")
    args = ap.parse_args()

    if args.source == "atlas":
        graphs = list(graph_atlas(args.max_n, args.connected))
    else:
        if not args.graph6_file:
            ap.error("--graph6-file is required for --source graph6")
        graphs = list(read_graph6_file(args.graph6_file))

    groups = group_graphs(graphs)
    rng = random.Random(args.seed)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    checked = 0
    found = 0
    with out_path.open("w") as out:
        for key, gs in sorted(groups.items()):
            pairs = [(i, j) for i in range(len(gs)) for j in range(i + 1, len(gs))]
            if args.shuffle:
                rng.shuffle(pairs)
            for i, j in pairs:
                checked += 1
                G, H = gs[i], gs[j]
                if relation_holds(G, H, args.weaker, args.stronger, simple_squares=not args.walk_squares):
                    rec = {
                        "n": key[0], "m": key[1],
                        "weaker": args.weaker, "stronger": args.stronger,
                        "G_graph6": graph6(G), "H_graph6": graph6(H),
                        "connected": nx.is_connected(G) and nx.is_connected(H),
                    }
                    out.write(json.dumps(rec) + "\n")
                    out.flush()
                    print(json.dumps(rec))
                    found += 1
                    # Keep going; multiple witnesses are useful.
                if args.limit_pairs and checked >= args.limit_pairs:
                    print(f"checked={checked} found={found} out={out_path}", file=sys.stderr)
                    return
    print(f"checked={checked} found={found} out={out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
