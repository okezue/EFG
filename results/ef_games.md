# EF-games and arithmetic constraint graphs (exploratory scaffold)

This is the "arithmetic constraint graphs + EF/WL" direction (combined problem #6
from the brainstorm). It is a research scaffold, not a solved problem: the open
Presburger EF lower-bound question is theory-heavy and computation only generates
small examples.

## What's here
- `efgames/ef.py` — exact r-round Ehrenfeucht-Fraisse game on finite graphs.
  `ef_equiv(G,H,r)` (Duplicator wins r rounds = agree on all FO sentences of
  quantifier rank ≤ r) and `spoiler_rank(G,H)` (least FO rank that separates).
  Sanity-checked: P2 vs P3 → rank 2; K3 vs K4 → rank 4; K3 vs K3 → equal.
- `efgames/arith_graphs.py` — Presburger-style constraint graphs: integer
  vertices with edges from distance bounds (`|i-j|≤c`), congruences
  (`(i-j)≡r mod m`), or linear inequalities on `[0,N)^d`.
- `experiments/ef_explore.py` — runs **both** the EF game and the edge-motif /
  2-WL refinements on each pair, tabulating FO quantifier rank against WL
  distinguishability.

## A clean EF-vs-WL contrast
`C6` vs `C3+C3` (both 2-regular):

| measure | separates? |
|---|---|
| degree / base (1-WL) | **no** (both 2-regular) |
| `tri`, `tri_square1`, 2-WL | yes |
| FO quantifier rank (EF) | yes, at **rank 3** (a triangle) |

So plain degree-refinement is blind, while both the triangle edge-motif and an
FO-rank-3 sentence see the difference — a concrete meeting point of the EF-game
and WL/edge-motif machinery on the same objects.

## Honest status
The engine and graph family are real and runnable; the *research* contribution
(an EF-game lower bound, or a separation between FO-rank and edge-motif/k-WL on a
structured arithmetic family) is open and would be theory-first. This scaffold
makes it cheap to search for candidate separating families.
