from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, List, Sequence, Tuple, Optional, Set
from collections import Counter, defaultdict
import networkx as nx

Color = Hashable
DirectedEdge = Tuple[int, int]
Signature = Tuple[int, Tuple[Tuple[int, int], ...]]
WL2Signature = Tuple[int, Tuple[int, ...]]


@dataclass(frozen=True)
class Mode:
    """Discrete edge-refinement mode.

    Every mode includes the old ordered-edge color and the left/right incidence
    multisets. Optional motif terms:

    * tri: triangle/common-neighbor multiset of pairs
      ((u,y),(v,y)).
    * square1: one-type 4-cycle multiset of triples
      ((u,y),(v,w),(y,w)).
    * square2: two-type 4-cycle aggregation: separate multisets of
      ((u,y),(v,w)) and (y,w).

    The default square convention is simple, non-induced 4-cycles: u,v,y,w must
    be pairwise distinct and edges u-y, y-w, w-v, v-u must exist. Chords u-w
    and v-y are allowed; this matches the usual non-induced cycle convention.
    """

    tri: bool = False
    square1: bool = False
    square2: bool = False
    simple_squares: bool = True

    @classmethod
    def parse(cls, mode: str, *, simple_squares: bool = True) -> "Mode":
        aliases = {
            "base": cls(False, False, False, simple_squares),
            "inc": cls(False, False, False, simple_squares),
            "tri": cls(True, False, False, simple_squares),
            "eb": cls(True, False, False, simple_squares),
            "triangle": cls(True, False, False, simple_squares),
            "square1": cls(False, True, False, simple_squares),
            "c4_1": cls(False, True, False, simple_squares),
            "1square": cls(False, True, False, simple_squares),
            "square2": cls(False, False, True, simple_squares),
            "c4_2": cls(False, False, True, simple_squares),
            "2square": cls(False, False, True, simple_squares),
            "tri_square1": cls(True, True, False, simple_squares),
            "both1": cls(True, True, False, simple_squares),
            "tri+c4_1": cls(True, True, False, simple_squares),
            "tri_square2": cls(True, False, True, simple_squares),
            "both2": cls(True, False, True, simple_squares),
            "tri+c4_2": cls(True, False, True, simple_squares),
        }
        try:
            return aliases[mode]
        except KeyError as exc:
            raise ValueError(f"Unknown mode {mode!r}. Available: {sorted(aliases)}") from exc


def available_modes() -> List[str]:
    return ["base", "tri", "square1", "square2", "tri_square1", "tri_square2"]


def graph6(G: nx.Graph) -> str:
    return nx.to_graph6_bytes(nx.convert_node_labels_to_integers(G), header=False).decode().strip()


def _canonicalize_graph(G: nx.Graph) -> nx.Graph:
    H = nx.Graph()
    H.add_nodes_from(range(G.number_of_nodes()))
    mapping = {v: i for i, v in enumerate(G.nodes())}
    H.add_edges_from((mapping[u], mapping[v]) for u, v in G.edges())
    return H


def _disjoint_union_with_ranges(graphs: Sequence[nx.Graph]) -> Tuple[nx.Graph, List[Tuple[int, int]]]:
    U = nx.Graph()
    ranges: List[Tuple[int, int]] = []
    offset = 0
    for G in graphs:
        H = _canonicalize_graph(G)
        n = H.number_of_nodes()
        U.add_nodes_from(range(offset, offset + n))
        U.add_edges_from((offset + u, offset + v) for u, v in H.edges())
        ranges.append((offset, offset + n))
        offset += n
    return U, ranges


def _directed_edges(G: nx.Graph) -> List[DirectedEdge]:
    out: List[DirectedEdge] = []
    for u, v in G.edges():
        out.append((u, v))
        out.append((v, u))
    return out


def _adjacency_sets(G: nx.Graph) -> List[Set[int]]:
    n = G.number_of_nodes()
    return [set(G.neighbors(i)) for i in range(n)]


def _square_witnesses(adj: Sequence[Set[int]], u: int, v: int, *, simple: bool = True) -> Iterable[Tuple[int, int]]:
    """Yield oriented 4-cycle witnesses (y,w) for target ordered edge (u,v).

    A witness means u-y-w-v-u is a non-induced 4-cycle. If simple=True, the four
    vertices are pairwise distinct. If simple=False, all length-3 walks from u to
    v whose middle edge is y-w are allowed; this walk-square convention has the
    cleanest ordinary-homomorphism semantics.
    """
    for y in adj[u]:
        for w in adj[v]:
            if w not in adj[y]:
                continue
            if simple and (y == v or w == u or y == w or y == u or w == v):
                continue
            yield (y, w)


def _edge_feature(
    colors: Dict[DirectedEdge, int],
    adj: Sequence[Set[int]],
    e: DirectedEdge,
    mode: Mode,
) -> Tuple[Hashable, ...]:
    u, v = e
    # old, left incidence, right incidence
    feat: List[Hashable] = [
        colors[(u, v)],
        tuple(sorted(colors[(u, x)] for x in adj[u])),
        tuple(sorted(colors[(v, z)] for z in adj[v])),
    ]
    if mode.tri:
        feat.append(tuple(sorted((colors[(u, y)], colors[(v, y)]) for y in (adj[u] & adj[v]))))
    if mode.square1:
        sq = []
        for y, w in _square_witnesses(adj, u, v, simple=mode.simple_squares):
            sq.append((colors[(u, y)], colors[(v, w)], colors[(y, w)]))
        feat.append(tuple(sorted(sq)))
    if mode.square2:
        near = []
        opp = []
        for y, w in _square_witnesses(adj, u, v, simple=mode.simple_squares):
            near.append((colors[(u, y)], colors[(v, w)]))
            opp.append(colors[(y, w)])
        feat.append(tuple(sorted(near)))
        feat.append(tuple(sorted(opp)))
    return tuple(feat)


def _h(x) -> bytes:
    import hashlib
    return hashlib.blake2b(repr(x).encode(), digest_size=16).digest()


def canonical_edge_motif_signature(G: nx.Graph, mode: str | Mode = "tri", *, max_iter: int = 64, simple_squares: bool = True) -> Signature:
    """Per-graph canonical edge-motif signature using content-hash colors.

    Refines G in isolation; colors are structure-only hashes, so signatures are
    comparable across independent calls without a shared disjoint union. Equality
    of canonical signatures is equivalent to edge_motif_equiv.
    """
    mode_obj = Mode.parse(mode, simple_squares=simple_squares) if isinstance(mode, str) else mode
    G = nx.convert_node_labels_to_integers(G)
    adj = _adjacency_sets(G); dedges = _directed_edges(G)
    colors: Dict[DirectedEdge, bytes] = {e: b"\x00" for e in dedges}
    for _ in range(max_iter):
        new = {e: _h(_edge_feature(colors, adj, e, mode_obj)) for e in dedges}
        if new == colors:
            break
        colors = new
    order = {d: i for i, d in enumerate(sorted(set(colors.values())))}
    pairs = []
    for u, v in G.edges():
        a, b = order[colors[(u, v)]], order[colors[(v, u)]]
        pairs.append((a, b) if a <= b else (b, a))
    return (G.number_of_nodes(), G.number_of_edges(), tuple(sorted(pairs)))


def _pair_signature_from_colors(G: nx.Graph, colors: Dict[DirectedEdge, int], lo: int, hi: int) -> Signature:
    pairs: List[Tuple[int, int]] = []
    for u, v in G.edges():
        if lo <= u < hi and lo <= v < hi:
            a, b = colors[(u, v)], colors[(v, u)]
            pairs.append((a, b) if a <= b else (b, a))
    return (hi - lo, tuple(sorted(pairs)))


def edge_motif_signatures(
    graphs: Sequence[nx.Graph],
    mode: str | Mode = "tri",
    *,
    max_iter: int = 32,
    simple_squares: bool = True,
) -> List[Signature]:
    """Run an edge-motif WL mode on a disjoint union and return graph signatures.

    Running on the disjoint union makes color identifiers comparable across all
    graphs in the input list. For pairwise comparisons use edge_motif_equiv.
    """
    if isinstance(mode, str):
        mode_obj = Mode.parse(mode, simple_squares=simple_squares)
    else:
        mode_obj = mode
    U, ranges = _disjoint_union_with_ranges(graphs)
    adj = _adjacency_sets(U)
    dedges = _directed_edges(U)
    colors: Dict[DirectedEdge, int] = {e: 0 for e in dedges}
    sigs: List[Signature] = [_pair_signature_from_colors(U, colors, lo, hi) for (lo, hi) in ranges]

    for _ in range(max_iter):
        features = [_edge_feature(colors, adj, e, mode_obj) for e in dedges]
        color_map: Dict[Hashable, int] = {}
        new_colors: Dict[DirectedEdge, int] = {}
        for e, feat in zip(dedges, features):
            if feat not in color_map:
                color_map[feat] = len(color_map)
            new_colors[e] = color_map[feat]
        new_sigs = [_pair_signature_from_colors(U, new_colors, lo, hi) for (lo, hi) in ranges]
        if new_colors == colors:
            colors = new_colors
            sigs = new_sigs
            break
        colors = new_colors
        sigs = new_sigs
    return sigs


def edge_motif_signature_pair(
    G: nx.Graph,
    H: nx.Graph,
    mode: str | Mode = "tri",
    *,
    max_iter: int = 32,
    simple_squares: bool = True,
) -> Tuple[Signature, Signature]:
    sigs = edge_motif_signatures([G, H], mode, max_iter=max_iter, simple_squares=simple_squares)
    return sigs[0], sigs[1]


def edge_motif_equiv(
    G: nx.Graph,
    H: nx.Graph,
    mode: str | Mode = "tri",
    *,
    max_iter: int = 32,
    simple_squares: bool = True,
) -> bool:
    a, b = edge_motif_signature_pair(G, H, mode, max_iter=max_iter, simple_squares=simple_squares)
    return a == b


def _wl2_signature_from_colors(colors: Dict[Tuple[int, int], int], lo: int, hi: int) -> WL2Signature:
    return (hi - lo, tuple(sorted(colors[(i, j)] for i in range(lo, hi) for j in range(lo, hi))))


def wl2_signatures(graphs: Sequence[nx.Graph], *, max_iter: int = 32) -> List[WL2Signature]:
    """Run standard 2-WL on ordered vertex pairs over a disjoint union."""
    U, ranges = _disjoint_union_with_ranges(graphs)
    n = U.number_of_nodes()
    adj_bool = [[False] * n for _ in range(n)]
    for u, v in U.edges():
        adj_bool[u][v] = adj_bool[v][u] = True
    pairs = [(i, j) for i in range(n) for j in range(n)]
    colors: Dict[Tuple[int, int], Hashable] = {(i, j): (i == j, adj_bool[i][j]) for i, j in pairs}
    # compress initial colors globally
    init_map: Dict[Hashable, int] = {}
    colors_i: Dict[Tuple[int, int], int] = {}
    for p in pairs:
        c = colors[p]
        if c not in init_map:
            init_map[c] = len(init_map)
        colors_i[p] = init_map[c]
    colors = colors_i
    sigs: List[WL2Signature] = [_wl2_signature_from_colors(colors, lo, hi) for (lo, hi) in ranges]
    for _ in range(max_iter):
        feats = []
        for i, j in pairs:
            feats.append((colors[(i, j)], tuple(sorted((colors[(i, k)], colors[(k, j)]) for k in range(n)))))
        cmap: Dict[Hashable, int] = {}
        new: Dict[Tuple[int, int], int] = {}
        for p, feat in zip(pairs, feats):
            if feat not in cmap:
                cmap[feat] = len(cmap)
            new[p] = cmap[feat]
        new_sigs = [_wl2_signature_from_colors(new, lo, hi) for (lo, hi) in ranges]
        if new == colors:
            colors = new
            sigs = new_sigs
            break
        colors = new
        sigs = new_sigs
    return sigs


def wl2_signature_pair(G: nx.Graph, H: nx.Graph, *, max_iter: int = 32) -> Tuple[WL2Signature, WL2Signature]:
    sigs = wl2_signatures([G, H], max_iter=max_iter)
    return sigs[0], sigs[1]


def wl2_equiv(G: nx.Graph, H: nx.Graph, *, max_iter: int = 32) -> bool:
    a, b = wl2_signature_pair(G, H, max_iter=max_iter)
    return a == b
