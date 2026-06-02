from motifwl.families import triangle_square_incomparability_pair, square_beats_triangle_pair
from motifwl.wl import edge_motif_equiv, graph6


def report(name, G, H):
    print(f"\n{name}")
    print("G", graph6(G))
    print("H", graph6(H))
    for mode in ["tri", "square1", "square2", "tri_square1", "tri_square2"]:
        print(f"  {mode:12s} equivalent? {edge_motif_equiv(G, H, mode)}")


if __name__ == "__main__":
    report("Triangle-only separates, square-only misses: C3 + C3 vs C6", *triangle_square_incomparability_pair())
    report("Square-only separates, triangle-only misses: C4 + C4 vs C8", *square_beats_triangle_pair())
