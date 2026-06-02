from motifwl.parity import private_triangle_parity_pair
from motifwl.wl import edge_motif_equiv


def test_private_triangle_parity_pair_closes_question():
    G0, G1 = private_triangle_parity_pair(d=1)
    assert G0.number_of_nodes() == G1.number_of_nodes() == 80
    assert G0.number_of_edges() == G1.number_of_edges() == 160
    assert edge_motif_equiv(G0, G1, "tri_square2")
    assert not edge_motif_equiv(G0, G1, "tri_square1")


def test_lower_modes_on_parity_pair():
    G0, G1 = private_triangle_parity_pair(d=1)
    assert edge_motif_equiv(G0, G1, "tri")
    assert edge_motif_equiv(G0, G1, "square2")
    # With private-triangle labels, square1 alone does not see the labels early enough;
    # the theorem concerns the combined Delta+square modes.
    assert edge_motif_equiv(G0, G1, "square1")
