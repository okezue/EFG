"""Arithmetic constraint graphs: vertices are integer points, edges given by a
Presburger-style constraint (linear inequality, distance bound, or congruence).

These are the objects in the "arithmetic constraint graphs + EF/WL" direction:
run both ef_equiv (FO quantifier rank) and the edge-motif / 2-WL refinements on
them to compare logical and combinatorial indistinguishability.
"""
import networkx as nx
from itertools import product


def interval_graph_1d(N, c):
    """Vertices 0..N-1 (integers), edge i~j iff 0 < |i-j| <= c. A band graph."""
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(i + 1, N):
            if abs(i - j) <= c:
                G.add_edge(i, j)
    return G


def congruence_graph(N, m, r):
    """Vertices 0..N-1, edge i~j (i!=j) iff (i-j) % m == r or (j-i) % m == r."""
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(i + 1, N):
            if (i - j) % m == r or (j - i) % m == r:
                G.add_edge(i, j)
    return G


def linear_grid_graph(N, d, a, c):
    """Vertices = integer points in [0,N)^d, edge p~q iff |a . (p-q)| <= c, p!=q."""
    pts = list(product(range(N), repeat=d))
    idx = {p: i for i, p in enumerate(pts)}
    G = nx.Graph()
    G.add_nodes_from(range(len(pts)))
    for p in pts:
        for q in pts:
            if p < q:
                s = sum(ai * (pi - qi) for ai, pi, qi in zip(a, p, q))
                if abs(s) <= c:
                    G.add_edge(idx[p], idx[q])
    return G
