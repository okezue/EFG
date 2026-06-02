# Final edge-motif WL package

Contents:

- `edge_motif_wl/` — code, proof notes, tests, and experiment scripts.
- `edge_motif_wl/docs/one_type_vs_two_type_strictness.md` — proof that
  `Delta+square2 < Delta+square1` using an explicit 80-vertex unlabelled parity pair.
- `edge_motif_wl/completed_proofs.md` — proof that `Delta+square1 < 2WL` using
  `C5 + C5` vs `C10`, plus addendum with the final strict chain.
- `edge_motif_wl/results/one_type_two_type_witness.txt` — graph6 strings and verification output.
- `eb_ef_chordal_manuscript.pdf` and `.tex` — EB-1WL EF-game/homomorphism manuscript.

To verify all code results:

```bash
cd edge_motif_wl
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$PWD:$PYTHONPATH"
pytest -q
python experiments/check_one_type_two_type.py --d 1
python experiments/check_completed_proofs.py
```
