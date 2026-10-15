# ARC Prize 2026 paper working package

**Not submission-ready.** `PAPER.md` was repaired on 2026-10-15 around verified account submission records. Existing `PAPER.pdf`, `PAPER.html`, every asset under `figures/`, and notebooks under `notebooks/` are **obsolete/unverified**: they may retain withdrawn architecture, theoretical, benchmark or novelty claims. Do not upload or cite those assets as support for the revised draft.

The working manuscript is [PAPER.md](PAPER.md). Numerical observations trace to [the preserved submission snapshot](evidence/2026-10-15-submissions.csv); provenance, withdrawn claims and remaining verification work are in [CLAIM_AUDIT.md](evidence/CLAIM_AUDIT.md).

The paper credits upstream dfranzen solver assets and reports reproduction plus unsuccessful configuration changes. Baseline-labelled submissions are not established as byte-identical. Public scores cannot establish causal ablation effects.

Before publication:

1. Match submission IDs to archived versions and artifact hashes; audit attribution and licences.
2. Replace the companion with a reproducible evidence analysis, then verify public accessibility and execution.
3. Regenerate the PDF, HTML, cover and figures from the corrected manuscript and evidence.
4. Recheck current paper-track rules, eligibility, word counting and required assets, then review the complete package.

Run document/evidence checks with `python3 -m pytest tests/test_paper_invariants.py -q` using an environment containing pytest. These checks verify word limits, evidence linkage and asset-status disclosure. **They do not validate experiments, hardware performance, provenance of submitted binaries or scientific conclusions.**
