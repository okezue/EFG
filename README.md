# Edge-motif WL: completed hierarchy proofs

This repository accompanies the EB-1WL/EF-game manuscript and the 4-cycle edge-message-passing proof work.

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
