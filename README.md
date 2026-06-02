# Edge-motif WL: completed hierarchy proofs

This repository accompanies the EB-1WL/EF-game manuscript and the 4-cycle edge-message-passing proof work.

## Computational extensions (`results/`)
Layered on the proofs, three computational directions (all reproducible):
- **Exhaustive search** (`results/exhaustive_search.md`): all graphs on ≤10
  vertices contain **no** `Δ+□₂ < Δ+□₁` witness → minimal separator is ≥11
  vertices. Run on a 192-core server via `experiments/sweep.py` with an exact
  O(N) canonical-signature collision search.
- **Full mode lattice** (`experiments/lattice.py`): `base < {tri, square1,
  square2}`, `tri ∥ square1, square2`, `tri_square1 < 2WL`, with witness sizes.
- **Neural GNN** (`results/gnn_experiments.md`, `motifgnn/`): a PyTorch
  edge-motif GNN. Untrained models exactly realize the discrete refinement
  (20/20); trained models' learnability matches discrete expressivity (10/10);
  the parity pair exposes an expressivity-vs-trainability gap (signal ~2e-9).
- **EF-games** (`results/ef_games.md`, `efgames/`): exact Ehrenfeucht-Fraisse
  game engine + arithmetic constraint graphs, comparing FO quantifier rank with
  WL/edge-motif distinguishability.

The completed hierarchy result is:

\[
\boxed{\Delta+\square_2 \prec \Delta+\square_1 \prec 2\mathrm{WL}.}
\]

- `\Delta` is the triangle/common-neighbor term from EB-1WL.
- `\square_1` is one-type simple 4-cycle aggregation: it records triples
  `(left-near color, right-near color, opposite color)` for each 4-cycle witness.
- `\square_2` is two-type simple 4-cycle aggregation: it records the near pair
  multiset and opposite-edge-color multiset separately.

The strict separation

\[
\Delta+\square_2 \prec \Delta+\square_1
\]

is witnessed by an explicit 80-vertex unlabelled parity-square pair generated in
`motifwl/parity.py`.  The strict separation

\[
\Delta+\square_1 \prec 2\mathrm{WL}
\]

is witnessed by

\[
C_5\sqcup C_5 \quad\text{vs.}\quad C_{10}.
\]

## Files

- `docs/one_type_vs_two_type_strictness.md` — full proof that `tri_square2 < tri_square1`.
- `completed_proofs.md` — proof of the odd-cycle separation from full 2-WL.
- `proof_note.md` — earlier general scaffold and homomorphism-count discussion.
- `motifwl/wl.py` — exact discrete color-refinement code for edge-motif WL and 2-WL.
- `motifwl/parity.py` — explicit parity-square graph construction closing the one-type/two-type question.
- `motifwl/families.py` — graph-family helpers.
- `motifwl/hom.py` — brute-force homomorphism counts for small patterns.
- `experiments/check_one_type_two_type.py` — verifies the 80-vertex parity-square witness.
- `experiments/check_completed_proofs.py` — verifies the odd-cycle strictness pair and family.
- `experiments/check_theorem_pairs.py` — verifies the earlier triangle/square incomparability examples.
- `experiments/search_pairs.py` — brute-force search utility for additional comparisons.
- `tests/` — pytest tests for the proved witnesses.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$PWD:$PYTHONPATH"
pytest -q
```

## Verify the new strictness result

```bash
python experiments/check_one_type_two_type.py --d 1 --print-graph6
```

Expected headline:

```text
Parity pair d=1
  G0: n=80 m=160
  G1: n=80 m=160
  tri          equivalent? True
  square1      equivalent? True
  square2      equivalent? True
  tri_square2  equivalent? True
  tri_square1  equivalent? False
```

## Verify the 2-WL strictness result

```bash
python experiments/check_completed_proofs.py
```

Expected headline:

```text
Main strictness pair: C5 + C5 vs C10
  base         equivalent? True
  tri          equivalent? True
  square1      equivalent? True
  square2      equivalent? True
  tri_square1  equivalent? True
  tri_square2  equivalent? True
  2wl          equivalent? False
  hom(C5,G)=20
  hom(C5,H)=0
```

## Search for additional witnesses

```bash
python experiments/search_pairs.py --source atlas --max-n 7 \
  --weaker tri_square2 --stronger tri_square1 \
  --out results/two_type_vs_one_type.jsonl
```

The explicit parity construction is much smaller conceptually than an exhaustive
search witness: it realizes the standard even/odd parity gap between pairwise
marginals and full triples directly inside edge-based 4-cycle aggregation.
