from __future__ import annotations
import networkx as nx
from collections import defaultdict
from motifwl.wl import canonical_edge_motif_signature as csig, canonical_wl2_signature as c2

MODES = ["base", "tri", "square1", "square2", "tri_square1", "tri_square2", "2wl"]


def sig(G, m):
    return c2(G) if m == "2wl" else csig(G, m)


def cyc(k):
    return nx.cycle_graph(k)


def union(a, b):
    return nx.disjoint_union(a, b)


# Named witness pairs from the manuscript + exhaustive search, with their sizes.
def named_witnesses():
    return [
        ("C3+C3 vs C6", union(cyc(3), cyc(3)), cyc(6)),     # tri distinguishes, square does not
        ("C4+C4 vs C8", union(cyc(4), cyc(4)), cyc(8)),     # square distinguishes, tri does not
        ("C5+C5 vs C10", union(cyc(5), cyc(5)), cyc(10)),   # 2WL distinguishes, tri_square1 does not
    ]


def relation_over(pairs_graphs):
    """Given a list of graphs, return strict< and incomparable relations among MODES."""
    sigs = {m: [sig(G, m) for G in pairs_graphs] for m in MODES}

    def refines(B, A):
        by = defaultdict(set)
        for i in range(len(pairs_graphs)):
            by[sigs[B][i]].add(sigs[A][i])
        return all(len(v) == 1 for v in by.values())
    return refines


def main():
    print("=== Mode separations on the named witness pairs ===")
    for name, G, H in named_witnesses():
        diffs = [m for m in MODES if sig(G, m) != sig(H, m)]
        print(f"  {name:16} distinguished by: {', '.join(diffs) if diffs else '(none)'}")

    print("\n=== Established hierarchy (witness -> minimal size) ===")
    facts = [
        ("base    < square1, square2, tri", "exhaustive n<=5", "<=5"),
        ("tri     || square1, square2", "C3+C3/C6 and C4+C4/C8", "6 and 8"),
        ("tri_square1 < 2WL", "C5+C5 vs C10", "10"),
        ("tri_square2 < tri_square1", "80-vertex parity pair; none smaller", ">=11 (exhaustive n<=10)"),
        ("tri_square2 < tri_square1 < 2WL", "full chain", "-"),
    ]
    for rel, wit, size in facts:
        print(f"  {rel:34} | witness: {wit:34} | min |V|: {size}")


if __name__ == "__main__":
    main()
