# Neural edge-motif GNN experiments

`motifgnn/model.py` is a PyTorch GNN whose message-passing layer mirrors the
discrete edge-motif update `_edge_feature` exactly: edge states `h_{(u,v)}` are
updated by MLPs over the old state, left/right incidence sums, the triangle term
(Δ), and the 4-cycle terms (□₁ one-type triple, □₂ two-type). Readout sums edge
states. Run on `tambe-server-1` (H100, float64). Three experiments.

## 1. Theory ↔ neural bridge (untrained) — `experiments/gnn_bridge.py`
For an **untrained** model, two graphs that are WL-indistinguishable under a mode
have identical edge-feature multisets at every layer, so their summed embeddings
are **exactly equal** regardless of weights; distinguishable graphs differ.

Result: **20/20 (pair, mode) cases match the discrete refinement** (float64).

| pair | indistinguishable modes → rel-diff | distinguishable modes → rel-diff |
|---|---|---|
| C3+C3 / C6 | square1, square2 → **0** | tri, tri_square1/2 → ~5e-2 |
| C4+C4 / C8 | tri → **0** | square1/2, tri_square1/2 → ~9e-2 |
| C5+C5 / C10 | all edge modes → **0** | (only 2-WL separates) |
| parity (80v) | tri, square1, square2, tri_square2 → ~1e-16 | **tri_square1 → 2.4e-9** |

The neural architecture provably realizes the discrete refinement.

## 2. Hierarchy via training (small witnesses) — `experiments/gnn_train.py`
Train each mode to classify each witness pair. A mode reaches accuracy 1.0 iff it
discretely distinguishes the pair; otherwise its two embeddings are bit-identical
and it is **provably stuck at chance (0.5)**.

Result: **10/10 cases — trained learnability matches discrete expressivity.**
- `tri` learns C3+C3/C6 but **cannot** learn C4+C4/C8.
- `square1/2` learn C4+C4/C8 but **cannot** learn C3+C3/C6.
- `tri_square1/2` learn both.

This realizes the `tri ∥ square` incomparability and the mode hierarchy in
actual trained networks.

## 3. Expressivity–trainability gap on the parity pair — `experiments/gnn_train_parity.py`
`tri_square1` *theoretically* separates the 80-vertex parity pair, but the signal
is only ~2.4e-9 (vs ~5e-2 for small witnesses). Consequences:
- In **float32** the signal is below machine-ε (~1e-7): embeddings are numerically
  identical, gradient is zero, no training is possible.
- Even in **float64**, standard Adam from random init does **not** recover the
  separation within 300 steps (loss stays at ln 2).

So the parity separation, though exact in theory, is **numerically near-unrealizable
by gradient training** — a concrete expressivity-vs-trainability gap. `tri_square2`
is provably unable in any precision (embeddings bit-identical).
