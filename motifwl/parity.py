"""Parity-square constructions for separating one-type and two-type C4 aggregation.

The main public function is ``private_triangle_parity_pair``.  It returns two
ordinary unlabelled simple graphs G_even and G_odd.  They have the same
Delta+square_2 edge-motif WL signature, but Delta+square_1 separates them.

Construction summary
--------------------
Core vertices are four copies of GF(2)^d named U,V,W,Y.  Core edges are the
four sides of the cyclic 4-partite pattern U--V--W--Y--U.  Each core edge has a
role R,A,B,C and a bit:

    R(U_i,V_j) = first_bit(i xor j)
    A(U_i,Y_l) = first_bit(i xor l)
    B(V_j,W_k) = first_bit(j xor k)
    C(Y_l,W_k) = first_bit(l xor k) xor parity

Thus every core square U_i V_j W_k Y_l U_i satisfies

    R xor A xor B xor C = parity.

The role+bit label is encoded without labels by attaching a distinct number of
private triangle vertices to each core edge.  If lambda(role,bit)=q, then q new
vertices are adjacent to the two endpoints of that core edge and to no other
vertices.  The resulting graphs are simple and unlabelled.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple
import networkx as nx

Role = str
Bit = int

ROLES: Tuple[Role, ...] = ("R", "A", "B", "C")

# Distinct positive triangle multiplicities for the eight role/bit labels.
DEFAULT_LABEL_MULTIPLICITIES: Dict[Tuple[Role, Bit], int] = {
    (role, bit): 1 + 2 * i + bit
    for i, role in enumerate(ROLES)
    for bit in (0, 1)
}


@dataclass(frozen=True)
class CoreEdgeRecord:
    """Metadata for one core edge before private triangles are attached."""

    u: int
    v: int
    role: Role
    bit: Bit
    left_part: str
    right_part: str
    left_value: int
    right_value: int


def _first_bit(x: int) -> int:
    return x & 1


def parity_core_graph(parity: int = 0, d: int = 1) -> Tuple[nx.Graph, List[CoreEdgeRecord]]:
    """Return the labelled-by-metadata core graph for parity ``0`` or ``1``.

    The returned graph is still an ordinary NetworkX graph; labels are only
    stored in the records returned alongside it.  The core graph has four parts
    U,V,W,Y, each of size 2**d, and complete bipartite graphs on the four cyclic
    side pairs U--V, V--W, W--Y, Y--U.
    """
    if parity not in (0, 1):
        raise ValueError("parity must be 0 or 1")
    if d < 1:
        raise ValueError("d must be at least 1")

    G = nx.Graph()
    values = list(range(2**d))
    idx: Dict[Tuple[str, int], int] = {}
    node = 0
    for part in ("U", "V", "W", "Y"):
        for value in values:
            idx[(part, value)] = node
            G.add_node(node, part=part, value=value, core=True)
            node += 1

    records: List[CoreEdgeRecord] = []

    def add_core_edge(p: str, x: int, q: str, y: int, role: Role, bit: Bit) -> None:
        u, v = idx[(p, x)], idx[(q, y)]
        G.add_edge(u, v, core=True, role=role, bit=bit)
        records.append(CoreEdgeRecord(u, v, role, bit, p, q, x, y))

    for u in values:
        for v in values:
            add_core_edge("U", u, "V", v, "R", _first_bit(u ^ v))
    for u in values:
        for y in values:
            add_core_edge("U", u, "Y", y, "A", _first_bit(u ^ y))
    for v in values:
        for w in values:
            add_core_edge("V", v, "W", w, "B", _first_bit(v ^ w))
    for y in values:
        for w in values:
            add_core_edge("Y", y, "W", w, "C", _first_bit(y ^ w) ^ parity)

    return G, records


def private_triangle_lift(
    core: nx.Graph,
    records: Iterable[CoreEdgeRecord],
    multiplicities: Dict[Tuple[Role, Bit], int] | None = None,
) -> nx.Graph:
    """Replace role/bit labels by private triangle multiplicities.

    For each core edge xy of role/bit tau and q=multiplicities[tau], add q new
    private vertices adjacent exactly to x and y.  The core edge xy remains.
    """
    if multiplicities is None:
        multiplicities = DEFAULT_LABEL_MULTIPLICITIES
    G = nx.Graph()
    G.add_nodes_from(core.nodes(data=True))
    # Copy only core edges; private vertices are added below.
    for u, v, data in core.edges(data=True):
        G.add_edge(u, v, **data)
    next_node = max(G.nodes(), default=-1) + 1
    for rec in records:
        q = multiplicities[(rec.role, rec.bit)]
        for j in range(q):
            z = next_node
            next_node += 1
            G.add_node(
                z,
                core=False,
                private=True,
                role=rec.role,
                bit=rec.bit,
                private_index=j,
                attached_to=(rec.u, rec.v),
            )
            G.add_edge(rec.u, z, private=True, role=rec.role, bit=rec.bit, side="left")
            G.add_edge(z, rec.v, private=True, role=rec.role, bit=rec.bit, side="right")
    return nx.convert_node_labels_to_integers(G)


def private_triangle_parity_graph(parity: int = 0, d: int = 1) -> nx.Graph:
    """Return the unlabelled graph G_parity used in the strictness proof."""
    core, records = parity_core_graph(parity=parity, d=d)
    return private_triangle_lift(core, records)


def private_triangle_parity_pair(d: int = 1) -> Tuple[nx.Graph, nx.Graph]:
    """Return (G_even, G_odd) for the one-type/two-type separation."""
    return private_triangle_parity_graph(0, d=d), private_triangle_parity_graph(1, d=d)
