from motifwl.families import c5_strictness_pair, cycle
from motifwl.wl import edge_motif_equiv, wl2_equiv
from motifwl.hom import hom_count


def test_c5_c5_vs_c10_strictness():
    G, H = c5_strictness_pair()
    for mode in ["base", "tri", "square1", "square2", "tri_square1", "tri_square2"]:
        assert edge_motif_equiv(G, H, mode, max_iter=64)
    assert not wl2_equiv(G, H, max_iter=64)
    assert hom_count(cycle(5), G) != hom_count(cycle(5), H)
