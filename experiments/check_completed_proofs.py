from motifwl.families import c5_strictness_pair, odd_cycle_double_pair, cycle
from motifwl.wl import edge_motif_equiv, wl2_equiv, available_modes
from motifwl.hom import hom_count


def report_pair(name, G, H):
    print(f"\n{name}")
    print(f"  |V|,|E|: G=({G.number_of_nodes()},{G.number_of_edges()}), H=({H.number_of_nodes()},{H.number_of_edges()})")
    for mode in available_modes():
        print(f"  {mode:12s} equivalent? {edge_motif_equiv(G, H, mode, max_iter=64)}")
    print(f"  {'2wl':12s} equivalent? {wl2_equiv(G, H, max_iter=64)}")
    C5 = cycle(5)
    print(f"  hom(C5,G)={hom_count(C5, G)}")
    print(f"  hom(C5,H)={hom_count(C5, H)}")


def main():
    G, H = c5_strictness_pair()
    report_pair("Main strictness pair: C5 + C5 vs C10", G, H)
    for k in [5, 7, 9]:
        Gk, Hk = odd_cycle_double_pair(k)
        print(f"\nOdd-cycle family check: C{k}+C{k} vs C{2*k}")
        print(f"  tri_square1 equivalent? {edge_motif_equiv(Gk, Hk, 'tri_square1', max_iter=64)}")
        print(f"  tri_square2 equivalent? {edge_motif_equiv(Gk, Hk, 'tri_square2', max_iter=64)}")
        print(f"  2wl equivalent?         {wl2_equiv(Gk, Hk, max_iter=64)}")


if __name__ == "__main__":
    main()
