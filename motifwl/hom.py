from __future__ import annotations

from itertools import product
import networkx as nx


def hom_count(F: nx.Graph, G: nx.Graph) -> int:
    """Brute-force homomorphism count hom(F,G). Suitable only for small F,G."""
    F = nx.convert_node_labels_to_integers(F)
    G = nx.convert_node_labels_to_integers(G)
    n = G.number_of_nodes()
    adjG = [[False] * n for _ in range(n)]
    for u, v in G.edges():
        adjG[u][v] = adjG[v][u] = True
    edgesF = list(F.edges())
    count = 0
    for phi in product(range(n), repeat=F.number_of_nodes()):
        ok = True
        for u, v in edgesF:
            if not adjG[phi[u]][phi[v]]:
                ok = False
                break
        if ok:
            count += 1
    return count


def rooted_hom_count(F: nx.Graph, root: tuple[int, int], G: nx.Graph, image: tuple[int, int]) -> int:
    """Brute-force rooted hom count. Root and image are ordered edges."""
    F = nx.convert_node_labels_to_integers(F)
    # If caller gives non-integer root, relabel outside. This simple function assumes ints.
    a, b = root
    u, v = image
    if not G.has_edge(u, v):
        return 0
    nodes = list(range(F.number_of_nodes()))
    free = [x for x in nodes if x not in (a, b)]
    Gnodes = list(G.nodes())
    count = 0
    adj = {x: set(G.neighbors(x)) for x in G.nodes()}
    for vals in product(Gnodes, repeat=len(free)):
        phi = {a: u, b: v}
        phi.update(dict(zip(free, vals)))
        ok = True
        for x, y in F.edges():
            if phi[y] not in adj[phi[x]]:
                ok = False
                break
        if ok:
            count += 1
    return count
