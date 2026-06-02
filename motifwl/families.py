from __future__ import annotations

import networkx as nx


def cycle(n: int) -> nx.Graph:
    return nx.cycle_graph(n)


def disjoint_cycles(*lengths: int) -> nx.Graph:
    G = nx.Graph()
    offset = 0
    for L in lengths:
        C = nx.cycle_graph(L)
        G.add_nodes_from(range(offset, offset + L))
        G.add_edges_from((offset + u, offset + v) for u, v in C.edges())
        offset += L
    return G


def triangle_square_incomparability_pair():
    """Pair square-only misses but triangle-only catches: C3 + C3 vs C6."""
    return disjoint_cycles(3, 3), cycle(6)


def square_beats_triangle_pair():
    """Pair triangle-only misses but square-only catches: C4 + C4 vs C8."""
    return disjoint_cycles(4, 4), cycle(8)


def c5_strictness_pair():
    """Main strictness pair: C5 + C5 vs C10.

    Triangle+4-cycle edge refinements see no triangles and no simple 4-cycles
    around any edge in either graph; full 2-WL separates via hom(C5, -).
    """
    return disjoint_cycles(5, 5), cycle(10)


def odd_cycle_double_pair(k: int):
    """Return C_k + C_k vs C_{2k}; k should be odd and at least 5."""
    if k < 5 or k % 2 == 0:
        raise ValueError("k must be odd and at least 5")
    return disjoint_cycles(k, k), cycle(2 * k)
