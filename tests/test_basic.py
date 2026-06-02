from motifwl.families import triangle_square_incomparability_pair, square_beats_triangle_pair
from motifwl.wl import edge_motif_equiv


def test_triangle_square_incomparability_pair():
    G, H = triangle_square_incomparability_pair()
    assert not edge_motif_equiv(G, H, "tri")
    assert edge_motif_equiv(G, H, "square1")
    assert edge_motif_equiv(G, H, "square2")
    assert not edge_motif_equiv(G, H, "tri_square1")


def test_square_beats_triangle_pair():
    G, H = square_beats_triangle_pair()
    assert edge_motif_equiv(G, H, "tri")
    assert not edge_motif_equiv(G, H, "square1")
    assert not edge_motif_equiv(G, H, "square2")
    assert not edge_motif_equiv(G, H, "tri_square1")
