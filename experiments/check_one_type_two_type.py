from __future__ import annotations

import argparse
from motifwl.parity import private_triangle_parity_pair
from motifwl.wl import edge_motif_equiv, wl2_equiv, graph6

MODES = ["tri", "square1", "square2", "tri_square2", "tri_square1", "base"]


def main() -> None:
    ap = argparse.ArgumentParser(description="Verify the Delta+square_2 < Delta+square_1 separation.")
    ap.add_argument("--d", type=int, default=1, help="Dimension of the GF(2)^d construction. d=1 is smallest.")
    ap.add_argument("--max-iter", type=int, default=40)
    ap.add_argument("--print-graph6", action="store_true")
    args = ap.parse_args()

    G0, G1 = private_triangle_parity_pair(d=args.d)
    print(f"Parity pair d={args.d}")
    print(f"  G0: n={G0.number_of_nodes()} m={G0.number_of_edges()}")
    print(f"  G1: n={G1.number_of_nodes()} m={G1.number_of_edges()}")
    for mode in MODES:
        eq = edge_motif_equiv(G0, G1, mode, max_iter=args.max_iter)
        print(f"  {mode:12s} equivalent? {eq}")
    print(f"  {'2wl':12s} equivalent? {wl2_equiv(G0, G1, max_iter=args.max_iter)}")
    if args.print_graph6:
        print("G0 graph6:")
        print(graph6(G0))
        print("G1 graph6:")
        print(graph6(G1))


if __name__ == "__main__":
    main()
