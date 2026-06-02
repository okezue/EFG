"""Classic r-round Ehrenfeucht-Fraisse game on finite graphs (FO, quantifier rank).

ef_equiv(G,H,r) is True iff Duplicator wins the r-round game, i.e. G and H agree
on all first-order sentences of quantifier rank <= r. spoiler_rank(G,H) returns
the least r at which Spoiler wins (the FO quantifier rank needed to separate),
or None if equal up to maxr.
"""
from functools import lru_cache
import networkx as nx


def _adj(G):
    n = G.number_of_nodes()
    A = [[False] * n for _ in range(n)]
    for u, v in G.edges():
        A[u][v] = A[v][u] = True
    return A


def _partial_iso(a, b, AG, AH):
    for i in range(len(a)):
        for j in range(len(a)):
            if (a[i] == a[j]) != (b[i] == b[j]):
                return False
            if AG[a[i]][a[j]] != AH[b[i]][b[j]]:
                return False
    return True


def ef_equiv(G, H, r):
    G = nx.convert_node_labels_to_integers(G)
    H = nx.convert_node_labels_to_integers(H)
    AG, AH = _adj(G), _adj(H)
    VG, VH = range(G.number_of_nodes()), range(H.number_of_nodes())

    @lru_cache(maxsize=None)
    def dup(a, b, k):
        if not _partial_iso(a, b, AG, AH):
            return False
        if k == 0:
            return True
        for c in VG:
            if not any(dup(a + (c,), b + (d,), k - 1) for d in VH):
                return False
        for d in VH:
            if not any(dup(a + (c,), b + (d,), k - 1) for c in VG):
                return False
        return True

    return dup((), (), r)


def spoiler_rank(G, H, maxr=6):
    for r in range(1, maxr + 1):
        if not ef_equiv(G, H, r):
            return r
    return None
