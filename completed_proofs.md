# Completed proof extension: triangle+4-cycle edge WL is strictly below 2-WL

This note completes the main proof direction suggested by the edge-motif scaffold.  The key observation is that adding simple 4-cycle aggregation to EB-1WL still does not let an edge-local refinement see odd cycles of length at least five.  This gives a small, explicit, fully proved separation from full 2-WL:

\[
C_5\sqcup C_5 \equiv_{\Delta+\square_1} C_{10},
\qquad
C_5\sqcup C_5 \equiv_{\Delta+\square_2} C_{10},
\]

but

\[
C_5\sqcup C_5 \not\equiv_{2\mathrm{WL}} C_{10}.
\]

Thus the major equality candidate

\[
\Delta+\square_1\text{-EB-WL}\stackrel{?}{=}2\mathrm{WL}
\]

is false.  The formal conclusion is

\[
\boxed{\Delta+\square_2\preceq \Delta+\square_1 \prec 2\mathrm{WL}.}
\]

The strictness of the right containment is witnessed by \(C_5\sqcup C_5\) and \(C_{10}\).  The strictness of the left containment is now proved in `docs/one_type_vs_two_type_strictness.md`: an explicit 80-vertex parity-square pair satisfies \(G_0\equiv_{\Delta+\square_2}G_1\) and \(G_0
ot\equiv_{\Delta+\square_1}G_1\).

---

## 1. Definitions

All graphs are finite, simple, undirected, and loopless.  For a graph \(G\), write

\[
\vec E(G)=\{(u,v):uv\in E(G)\}
\]

for its ordered edges.

An edge-motif refinement colors ordered edges.  At round \(t\), the color of \((u,v)\in\vec E(G)\) is denoted

\[
\chi_t^G(u,v).
\]

Initially all ordered edges have one color:

\[
\chi_0^G(u,v)=0.
\]

Every mode considered here includes:

1. the old color \(\chi_t^G(u,v)\);
2. the left-incidence multiset
   \[
   L_t^G(u,v)=\multiset{\chi_t^G(u,x):x\in N_G(u)};
   \]
3. the right-incidence multiset
   \[
   R_t^G(u,v)=\multiset{\chi_t^G(v,z):z\in N_G(v)}.
   \]

The triangle mode \(\Delta\) also includes

\[
T_t^G(u,v)=
\multiset{(\chi_t^G(u,y),\chi_t^G(v,y)):y\in N_G(u)\cap N_G(v)}.
\]

A simple oriented 4-cycle witness for an ordered edge \((u,v)\) is a pair \((y,w)\) such that:

\[
u,y,w,v\quad\text{are pairwise distinct,}
\]

and

\[
uy,yw,wv,vu\in E(G).
\]

The 4-cycle is not required to be induced; chords \(uw\) and \(vy\) may exist.

The one-type 4-cycle mode \(\square_1\) includes the multiset

\[
Q_{1,t}^G(u,v)=
\multiset{(\chi_t^G(u,y),\chi_t^G(v,w),\chi_t^G(y,w)):(y,w)\in\operatorname{Sq}_G(u,v)},
\]

where \(\operatorname{Sq}_G(u,v)\) denotes the set of simple oriented 4-cycle witnesses for \((u,v)\).

The two-type 4-cycle mode \(\square_2\) includes the two marginals

\[
Q_{2,t}^{G,\mathrm{near}}(u,v)=
\multiset{(\chi_t^G(u,y),\chi_t^G(v,w)):(y,w)\in\operatorname{Sq}_G(u,v)},
\]

and

\[
Q_{2,t}^{G,\mathrm{opp}}(u,v)=
\multiset{\chi_t^G(y,w):(y,w)\in\operatorname{Sq}_G(u,v)}.
\]

We write:

\[
\Delta+\square_1
\]

for old color + left/right incidence + triangle + one-type 4-cycle aggregation, and

\[
\Delta+\square_2
\]

for old color + left/right incidence + triangle + two-type 4-cycle aggregation.

The graph-level signature is

\[
\operatorname{Sig}_M(G)=
\left(|V(G)|,
\multiset{\multiset{\chi_\infty^G(u,v),\chi_\infty^G(v,u)}:uv\in E(G)}
\right).
\]

Two graphs are equivalent for a mode \(M\), written \(G\equiv_M H\), when the refinement run on the disjoint union \(G\sqcup H\) gives equal graph-level signatures.

---

## 2. A local invisibility lemma

The separation rests on a strong local invariance statement for cycle graphs of girth at least five.

### Lemma 2.1

Let \(G\) be a disjoint union of cycles, each of length at least five.  Under any of the modes

\[
\mathrm{inc},\quad
\Delta,\quad
\square_1,\quad
\square_2,\quad
\Delta+\square_1,\quad
\Delta+\square_2,
\]

all ordered edges of \(G\) have the same color at every round.

### Proof

We prove the statement by induction on the refinement round \(t\).

At round \(t=0\), all ordered edges have the same initial color by definition.

Assume that at round \(t\), every ordered edge of \(G\) has the same color.  Call this color \(c_t\).  Let \((u,v)\in\vec E(G)\) be arbitrary.  We compute every component of the round-\((t+1)\) update and show that it is independent of \((u,v)\).

First, the old-color component is

\[
\chi_t^G(u,v)=c_t,
\]

independent of \((u,v)\).

Second, since every component of \(G\) is a cycle, every vertex has degree two.  Hence \(N_G(u)\) has exactly two vertices.  For both neighbors \(x\in N_G(u)\), the ordered edge \((u,x)\) has color \(c_t\).  Therefore the left-incidence multiset is

\[
L_t^G(u,v)=\multiset{c_t,c_t}.
\]

The same argument at \(v\) gives

\[
R_t^G(u,v)=\multiset{c_t,c_t}.
\]

Third, the triangle term is empty.  Indeed, if \(y\in N_G(u)\cap N_G(v)\), then \(u,v,y\) span a triangle.  A cycle of length at least five contains no triangle, and distinct connected components have no edges between them.  Thus

\[
N_G(u)\cap N_G(v)=\varnothing,
\]

and

\[
T_t^G(u,v)=\varnothing.
\]

Fourth, the simple 4-cycle witness set is empty.  Write the cycle component containing \(uv\) as

\[
\cdots - p - u - v - q - \cdots.
\]

A simple 4-cycle witness \((y,w)\) for \((u,v)\) must satisfy:

\[
y\in N_G(u),\qquad w\in N_G(v),\qquad yw\in E(G),
\]

with \(y,w\notin\{u,v\}\) and \(y\neq w\).  Since \(y\neq v\), the only possible value of \(y\) is \(p\).  Since \(w\neq u\), the only possible value of \(w\) is \(q\).  Thus a simple 4-cycle witness exists precisely when \(p q\in E(G)\).  But in a cycle of length at least five, the predecessor \(p\) of \(u\) and the successor \(q\) of \(v\) are not adjacent.  Therefore

\[
\operatorname{Sq}_G(u,v)=\varnothing.
\]

Consequently

\[
Q_{1,t}^G(u,v)=\varnothing,
\]

and

\[
Q_{2,t}^{G,\mathrm{near}}(u,v)=\varnothing,
\qquad
Q_{2,t}^{G,\mathrm{opp}}(u,v)=\varnothing.
\]

Every possible update component is therefore one of the fixed objects

\[
c_t,
\qquad
\multiset{c_t,c_t},
\qquad
\varnothing.
\]

Thus every ordered edge receives the same next color \(c_{t+1}\).  This completes the induction.  \(\square\)

---

## 3. The strictness pair

### Lemma 3.1

Let

\[
G=C_5\sqcup C_5,
\qquad
H=C_{10}.
\]

Then

\[
G\equiv_{\Delta+\square_1} H
\qquad\text{and}\qquad
G\equiv_{\Delta+\square_2} H.
\]

The same holds for the weaker modes \(\mathrm{inc}\), \(\Delta\), \(\square_1\), and \(\square_2\).

### Proof

Both \(G\) and \(H\) are disjoint unions of cycles of length at least five.  By Lemma 2.1, in the disjoint union \(G\sqcup H\), every ordered edge of \(G\sqcup H\) has the same color at every round for each of the listed modes.

At stabilization, let the single stable ordered-edge color be \(c\).  Then every undirected edge in both graphs has unordered orientation-color pair

\[
\multiset{c,c}.
\]

The graph-level signature records the number of vertices and the multiset of such edge-pairs.  We have

\[
|V(G)|=10=|V(H)|,
\]

and

\[
|E(G)|=10=|E(H)|.
\]

Therefore both graph-level signatures are

\[
\left(10,\multiset{\underbrace{\multiset{c,c},\ldots,\multiset{c,c}}_{10\text{ times}}}\right).
\]

Hence \(G\equiv_M H\) for every listed mode \(M\), in particular for \(\Delta+\square_1\) and \(\Delta+\square_2\).  \(\square\)

---

## 4. Full 2-WL separates the pair

The next step uses the standard homomorphism-count characterization of 2-WL: two graphs are indistinguishable by 2-WL if and only if they have equal homomorphism counts from every graph of treewidth at most two.  Since every cycle has treewidth two, the graph \(C_5\) is an admissible 2-WL homomorphism-count test.

For completeness, we spell out the relevant homomorphism-count difference.

### Lemma 4.1

\[
\hom(C_5,C_5\sqcup C_5)>0,
\qquad
\hom(C_5,C_{10})=0.
\]

### Proof

A homomorphism from \(C_5\) to a graph \(X\) is equivalently a closed walk of length five in \(X\).  Indeed, write

\[
V(C_5)=\{0,1,2,3,4\}
\]

with edges \(i(i+1)\), indices modulo five.  A homomorphism \(\varphi:C_5\to X\) chooses vertices

\[
x_i=\varphi(i)
\]

such that

\[
x_0x_1,x_1x_2,x_2x_3,x_3x_4,x_4x_0\in E(X),
\]

which is exactly a closed walk of length five.

First consider \(C_5\sqcup C_5\).  Each copy of \(C_5\) receives at least ten homomorphisms from \(C_5\): choose one of five images for vertex \(0\), and choose one of the two cyclic orientations.  Thus

\[
\hom(C_5,C_5\sqcup C_5)\ge 20>0.
\]

The exact value is not needed.

Now consider \(C_{10}\).  The graph \(C_{10}\) is bipartite.  Every closed walk in a bipartite graph has even length, because each step switches sides of the bipartition and returning to the starting side requires an even number of steps.  Therefore \(C_{10}\) has no closed walk of length five.  Hence

\[
\hom(C_5,C_{10})=0.
\]

This proves the lemma.  \(\square\)

### Theorem 4.2

\[
C_5\sqcup C_5\not\equiv_{2\mathrm{WL}} C_{10}.
\]

### Proof

The graph \(C_5\) has treewidth two.  By Lemma 4.1,

\[
\hom(C_5,C_5\sqcup C_5)\neq \hom(C_5,C_{10}).
\]

The homomorphism-count characterization of 2-WL implies that any such difference from a treewidth-two pattern is detected by 2-WL.  Therefore

\[
C_5\sqcup C_5\not\equiv_{2\mathrm{WL}} C_{10}.
\]

\(\square\)

---

## 5. Main strictness theorem

### Theorem 5.1

The combined triangle-plus-4-cycle edge refinements are strictly weaker than full 2-WL:

\[
\Delta+\square_1\prec 2\mathrm{WL},
\qquad
\Delta+\square_2\prec 2\mathrm{WL}.
\]

### Proof

First, both \(\Delta+\square_1\)-EB-WL and \(\Delta+\square_2\)-EB-WL are no stronger than 2-WL.  This can be seen in either of two equivalent ways.

1. At the color-refinement level, the edge-motif states are ordered edges, i.e. a subset of ordered vertex pairs, and every update aggregates color information from configurations of at most two free vertices around the current ordered edge.  These updates are definable from the information available to 2-WL on ordered pairs.

2. At the homomorphism-count level, every rooted pattern generated by incidence, triangle, and simple 4-cycle constructors has treewidth at most two.  Incidence constructors add an edge along a root endpoint; triangle constructors glue along a triangle; square constructors glue a 4-cycle gadget of treewidth two along rooted edges.  Gluing along vertices or edges and contracting equality-pattern degeneracies do not increase treewidth.  Thus every unrooted homomorphism witness produced by these refinements has treewidth at most two.  Since 2-WL determines all treewidth-two homomorphism counts, it determines every edge-motif signature.

Now strictness follows from the explicit pair

\[
G=C_5\sqcup C_5,
\qquad
H=C_{10}.
\]

By Lemma 3.1,

\[
G\equiv_{\Delta+\square_1}H
\qquad\text{and}\qquad
G\equiv_{\Delta+\square_2}H.
\]

By Theorem 4.2,

\[
G\not\equiv_{2\mathrm{WL}}H.
\]

Therefore each combined edge-motif refinement is strictly weaker than 2-WL.  \(\square\)

---

## 6. Infinite family

The same proof gives an infinite family.

### Theorem 6.1

For every odd \(\ell\ge 5\), let

\[
G_\ell=C_\ell\sqcup C_\ell,
\qquad
H_\ell=C_{2\ell}.
\]

Then

\[
G_\ell\equiv_{\Delta+\square_1}H_\ell
\qquad\text{and}\qquad
G_\ell\equiv_{\Delta+\square_2}H_\ell,
\]

but

\[
G_\ell\not\equiv_{2\mathrm{WL}}H_\ell.
\]

### Proof

Both \(G_\ell\) and \(H_\ell\) are disjoint unions of cycles of length at least five, and both have \(2\ell\) vertices and \(2\ell\) edges.  Lemma 2.1 implies that all ordered edges have the same stable color in \(G_\ell\sqcup H_\ell\) under \(\Delta+\square_1\) and \(\Delta+\square_2\).  The graph-level signatures agree because both graphs have the same vertex and edge counts.

To separate them by 2-WL, use the treewidth-two pattern \(C_\ell\).  The graph \(G_\ell\) has homomorphisms from \(C_\ell\): map \(C_\ell\) isomorphically, in either orientation, to either copy of \(C_\ell\).  Hence

\[
\hom(C_\ell,G_\ell)>0.
\]

The graph \(H_\ell=C_{2\ell}\) is an even cycle and is therefore bipartite.  Since \(\ell\) is odd, a homomorphism \(C_\ell\to H_\ell\) would be an odd closed walk in a bipartite graph, impossible.  Thus

\[
\hom(C_\ell,H_\ell)=0.
\]

Since \(\tw(C_\ell)=2\), the 2-WL homomorphism theorem gives

\[
G_\ell\not\equiv_{2\mathrm{WL}}H_\ell.
\]

\(\square\)

---

## 7. Relation to triangle-only EB-1WL and square-only refinements

The earlier small separations remain valid.

### Proposition 7.1: triangle-only and square-only are incomparable

Triangle-only refinement distinguishes

\[
C_3\sqcup C_3
\quad\text{from}\quad
C_6,
\]

because every edge of \(C_3\sqcup C_3\) lies in a triangle and no edge of \(C_6\) does.  Square-only refinement does not distinguish this pair, because both graphs are 2-regular and have no simple 4-cycle witnesses around any edge.

Square-only refinement distinguishes

\[
C_4\sqcup C_4
\quad\text{from}\quad
C_8,
\]

because every edge of \(C_4\sqcup C_4\) has a simple 4-cycle witness and no edge of \(C_8\) has one.  Triangle-only refinement does not distinguish this pair, because both graphs are 2-regular and triangle-free.

Therefore

\[
\Delta\parallel\square_1
\qquad\text{and}\qquad
\Delta\parallel\square_2.
\]

### Proposition 7.2: adding 4-cycles strictly strengthens triangle-only EB-1WL

For \(i\in\{1,2\}\),

\[
\Delta\prec \Delta+\square_i.
\]

### Proof

Containment is immediate because \(\Delta+\square_i\) contains every update component of \(\Delta\).

Strictness is witnessed by

\[
C_4\sqcup C_4
\quad\text{and}\quad
C_8.
\]

Triangle-only refinement does not distinguish this pair, by Proposition 7.1.  The combined refinement \(\Delta+\square_i\) does distinguish it, because its square component distinguishes it after one round.  \(\square\)

### Proposition 7.3: one-type dominates two-type

\[
\square_2\preceq\square_1,
\qquad
\Delta+\square_2\preceq\Delta+\square_1.
\]

### Proof

The one-type 4-cycle update sees the full multiset of triples

\[
\multiset{(a,b,c)}.
\]

From this triple multiset one can recover the near-edge marginal

\[
\multiset{(a,b)}
\]

by applying the projection \((a,b,c)\mapsto(a,b)\) to each triple, preserving multiplicity.  One can also recover the opposite-edge marginal

\[
\multiset{c}
\]

by applying the projection \((a,b,c)\mapsto c\).  Thus every square component used by \(\square_2\) is determined by the corresponding square component used by \(\square_1\).  The old-color, left-incidence, right-incidence, and triangle components are identical when present.

By induction on refinement rounds, equality of \(\square_1\)-colors implies equality of \(\square_2\)-colors, and equality of \((\Delta+\square_1)\)-colors implies equality of \((\Delta+\square_2)\)-colors.  Therefore the signature of the one-type mode determines the signature of the two-type mode.  \(\square\)

The converse of Proposition 7.3 remains the main unresolved comparison in this small hierarchy.

---

## 8. Corrected homomorphism-proof scaffold for simple squares

This section records the correction needed for simple 4-cycle semantics.  The quotient-closure phrase in the earlier proof note was too coarse.  The correct proof handles degeneracies explicitly.

### 8.1 Walk-square constructor

For rooted patterns \(P,Q,R\), define \(W(P,Q,R)\) by creating a root edge \((r,s)\), two new vertices \(y,w\), and edges

\[
rs,\quad ry,\quad yw,\quad ws.
\]

Glue \(P\) to \((r,y)\), \(Q\) to \((s,w)\), and \(R\) to \((y,w)\).  The unrestricted rooted homomorphism count is

\[
h_{W(P,Q,R)}^G(u,v)=
\sum_{\substack{y\in N(u),\;w\in N(v)\\ yw\in E(G)}}
h_P^G(u,y)h_Q^G(v,w)h_R^G(y,w).
\]

This sum allows the degeneracies \(y=v\) and \(w=u\).  The other equalities either force loops or are already impossible in a loopless host.

### 8.2 Simple-square count

The simple-square count used by the refinement is

\[
S(P,Q,R)^G(u,v)=
\sum_{(y,w)\in\operatorname{Sq}_G(u,v)}
h_P^G(u,y)h_Q^G(v,w)h_R^G(y,w),
\]

where \(y\neq v\) and \(w\neq u\), in addition to the edge constraints.  Since \((u,v)\) is a host edge, the only nonzero degeneracies of the unrestricted walk-square sum are:

1. \(y=v\);
2. \(w=u\);
3. both \(y=v\) and \(w=u\).

Therefore

\[
S(P,Q,R)=W(P,Q,R)-D_{y=v}(P,Q,R)-D_{w=u}(P,Q,R)+D_{y=v,w=u}(P,Q,R).
\]

Each degeneracy term is generated by the older incidence/root-product/reversal operations.

For example, when \(y=v\), the summand becomes

\[
h_P(u,v)h_Q(v,w)h_R(v,w),
\]

summed over \(w\in N(v)\).  This is

\[
h_P(u,v)\cdot h_{R(Q\odot R)}(u,v),
\]

where \(R(\cdot)\) is the right-incidence constructor and \(Q\odot R\) is the root product of \(Q\) and \(R\) rooted at \((v,w)\).  Multiplying by \(h_P(u,v)\) is root product at the outer root.

The case \(w=u\) is analogous, using left incidence and, if necessary, root reversal.  The case \(y=v,w=u\) is a root-edge product of \(P\), a reversed-root copy of \(Q\), and a reversed-root copy of \(R\), all evaluated on the root edge.

Thus the simple-square coordinate is in the algebra generated by the walk-square constructor plus the already-present incidence, root-product, and reversal operations.  Conversely, the unrestricted walk-square count is the simple-square coordinate plus these three degeneracy terms, so it is also determined by the refinement color once the lower-depth rooted counts are determined.

### 8.3 Consequence

The exact EF/span theorem can be stated using walk-square rooted patterns, with the simple-square implementation handled by the degeneracy identity above.  This avoids an uncontrolled arbitrary quotient-closure operation and keeps the generated homomorphism witnesses inside treewidth two.

---

## 9. Experimental verification

The repo contains `experiments/check_completed_proofs.py`, which verifies the finite witness and the odd-cycle family computationally.  The key expected output is:

```text
Main strictness pair: C5 + C5 vs C10
  base         equivalent? True
  tri          equivalent? True
  square1      equivalent? True
  square2      equivalent? True
  tri_square1  equivalent? True
  tri_square2  equivalent? True
  2wl          equivalent? False
  hom(C5,G)>0
  hom(C5,H)=0
```

The computation is not needed for the proof, but it is a useful guard against implementation mistakes and a starting point for searching the remaining one-type/two-type question.


---

## Addendum: one-type/two-type question closed

The remaining comparison mentioned in the first version of this note is closed in
`docs/one_type_vs_two_type_strictness.md`.  The result is

\[
\Delta+\square_2 \prec \Delta+\square_1.
\]

Together with the odd-cycle separation from 2-WL proved above, this gives the
strict chain

\[
\boxed{\Delta+\square_2 \prec \Delta+\square_1 \prec 2\mathrm{WL}.}
\]

The new strictness witness is an unlabelled graph pair on 80 vertices and 160
edges.  It is a private-triangle lift of the even/odd parity distribution on
core 4-cycles.  The two-type square aggregator sees only pairwise and one-way
marginals of this distribution; the one-type aggregator sees the full triple.
