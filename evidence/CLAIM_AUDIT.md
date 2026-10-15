# Claim audit — 2026-10-15

## Snapshot provenance

- Source: authenticated Kaggle CLI `kaggle competitions submissions -c arc-prize-2026-arc-agi-3 --csv` (account submission-list export supplied by the portfolio audit).
- Source file: `/Users/ishantpanchal/kaggle-portfolio/audits/2026-10-15/arc-prize-2026-arc-agi-3-submissions.csv`.
- Source filesystem modification time: 2026-10-15 20:32:20 +0530 (15:02:20 UTC). This is the export file timestamp, not an independently authenticated server capture time.
- Copied without modification to `2026-10-15-submissions.csv` at 2026-10-15T15:05:32.696302+00:00.
- SHA-256: `83c24d49d422847a33c00fe8e6fdb6fa951cbec1d1d362028000bb19edc4aaf6`.
- Independent CLI list read during inventory returned matching IDs and scores. The CSV establishes account-level public observations, not executable identity, evaluation invariance or causality.

## Withdrawn claims

| Earlier claim | Evidence issue | Repair |
|---|---|---|
| 27.85 demonstrates calibrated masking/batching improvements | Initial milestone submission scored 27.85; v3 modification labelled masking scored 6.52 | Report original and modified submission scores separately |
| 39.79 offline result; 34.12/18.50/11.40/8.33 ablations and 14.20/2.28 public scores | No adequate experimental provenance in the reviewed evidence | Remove table and claims |
| 7.8x improvement; 182ms to 23ms; over400% search gain | No paired latency/utilization traces | Remove |
| Masking provably improves model attention and reasoning | No implemented attention intervention or evidence of claimed theorem | Remove proof and guarantees |
| New speculative batching architecture | Upstream solver/source dependencies and no demonstrated original architecture | Credit upstream and limit novelty |
| All code public and reproducible; tests verify benchmarks | Local metadata marks kernel private; tests previously asserted strings | Mark assets obsolete/unverified and replace document checks |
| Baseline reruns are identical binaries | Descriptions and current version1 submit script do not prove historical artifact identity | Require manifests and hashes |

Attribution links in the manuscript come from `/Users/ishantpanchal/arc-agi-3/m2-solution/kernel-metadata.json`: `dfranzen/pennyroyal-v253`, `dfranzen/taaf-kaggle-source-bundle-copy`, plus dfranzen model sources. These are source-distribution links, not a verified complete authorship/licence bibliography. Historical public-author run numbers in older planning notes are not independently verified and are excluded.

## Remaining work

Archive per-submission notebook/source/model/environment/artifact manifests and hashes; verify runtime/scoring semantics and upstream licences; replace companion notebook and all old visual/rendered assets; verify public access, paper-track eligibility and current formatting rules. Existing `PAPER.pdf`, `PAPER.html`, `figures/` and `notebooks/` are obsolete/unverified and not submission-ready. No publication, cron mutation, submission or compute launch was performed by this repair.
