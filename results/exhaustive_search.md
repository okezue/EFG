# Exhaustive small-graph search for `Δ+□₂ < Δ+□₁` witnesses

Goal: find a graph pair `(G,H)` with equal `tri_square2` signature but distinct
`tri_square1` signature (a witness for the strict separation `Δ+□₂ ≺ Δ+□₁`),
smaller than the known 80-vertex parity construction in
`docs/one_type_vs_two_type_strictness.md`.

## Method
- `geng` (nauty) enumerates all non-isomorphic graphs on `n` vertices, sharded by
  edge count, including disconnected graphs (the known witnesses are disconnected).
- For each graph, `motifwl.wl.canonical_edge_motif_signature` computes a per-graph
  canonical signature using content-hash (blake2b) colors. Refining each graph in
  isolation is exact and comparable across graphs (disconnected components refine
  independently); verified to agree with the union-based `edge_motif_equiv` on
  15,000 structured atlas pairs with 0 disagreements.
- `experiments/sweep.py` buckets graphs by `tri_square2` signature in parallel
  (`multiprocessing`, all cores), then tests `tri_square1` inside each collision
  bucket. O(N) refinement rather than O(N²) pairwise comparison.

## Result
Exhaustive over **all graphs on n ≤ 10 vertices**: **0 witnesses.**

| n | graphs | wall time (190 cores) | peak RAM | witnesses |
|---|---|---|---|---|
| ≤8 | 12,346 | ~40 s | — | 0 |
| 9 | 274,668 | 2 m 20 s | 295 MB | 0 |
| 10 | ~12 M | 1 h 37 m | 12.7 GB | 0 |

Run on `tambe-server-1` (192 cores). Reproduce:

```bash
python experiments/sweep.py --weaker tri_square2 --stronger tri_square1 \
  --nmin 4 --nmax 10 --procs 190 --out results/n10.jsonl
```

## Conclusion
The minimal witness for `Δ+□₂ ≺ Δ+□₁` has **at least 11 vertices**. This is
consistent with the parity-square construction needing a genuinely large gadget;
no small accidental separator exists. (n = 11 is ~10× more graphs and exceeds the
single-node memory used here, so it would need a streaming/sharded driver.)
