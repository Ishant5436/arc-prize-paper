# Reproduction and Unsuccessful Configuration Changes in ARC-AGI-3

**Author / team:** Ishant Panchal / rainy-cloudss
**Track:** ARC Prize 2026 Paper Track, ARC-AGI-3
**Status:** Working draft; companion assets require replacement before submission.

## Abstract

We report account-level public leaderboard observations from ARC-AGI-3, including a reproduced solver baseline and unsuccessful subsequent configuration changes. The baseline-associated submission scored 27.85. Three later submissions labelled as baseline reruns scored 26.94, 27.08 and 24.54. Descriptions and the current submission script support that grouping, but archived code and artifact hashes have not established binary identity. Modified submissions in the same account scored between 0.00 and 25.05. These observations motivate an evaluation protocol that separates local diagnostics from competition performance and requires artifact provenance before attributing gains or losses to individual changes. We make no new solver architecture claim.

## Attribution and evidence

The solver depends on upstream work distributed under the Kaggle account **dfranzen**. Local kernel metadata names the source datasets [pennyroyal-v253](https://www.kaggle.com/datasets/dfranzen/pennyroyal-v253) and [taaf-kaggle-source-bundle-copy](https://www.kaggle.com/datasets/dfranzen/taaf-kaggle-source-bundle-copy), together with dfranzen model artifacts. We credit these upstream assets and do not claim their batching, inference implementation or solver design as our invention. A complete version and licence audit remains necessary before release.

The numerical source is the authenticated Kaggle submission-list snapshot preserved at [evidence/2026-10-15-submissions.csv](evidence/2026-10-15-submissions.csv). It records submission identifiers, UTC timestamps, descriptions, statuses and public scores. [The claim audit](evidence/CLAIM_AUDIT.md) documents capture provenance and limitations. A submission description is an operator-supplied label; it does not independently verify executed configuration or code identity.

## Public leaderboard observations

All rows below were marked COMPLETE in the snapshot. No private scores were available. The table summarizes observations, not controlled ablations.

| Submission | UTC date | Account description, abbreviated | Public score |
|---|---|---|---:|
| 56842502 | Oct 5 | Milestone 2 solution; baseline-associated | 27.85 |
| 56898814 | Oct 7 | v1 envelope re-run | 26.94 |
| 57159612 | Oct 14 | v1 envelope re-run | 27.08 |
| 57198437 | Oct 15 | v1 envelope re-run | 24.54 |
| 56870444 | Oct 6 | v3: concurrency 10, 1200s horizon, HUD masking | 6.52 |
| 57011082 | Oct 9 | v4: concurrency 10, 240s envelope | 1.00 |
| 57028832 | Oct 10 | v6: 120 streams, 532m envelope | 25.05 |
| 57059778 | Oct 11 | v7: concurrency 10, HUD masking, 1200s horizon | 7.72 |
| 57088385 | Oct 12 | v13: symbolic-engine integration | 0.00 |
| 57126448 | Oct 13 | v15: sandbox / memory / stream changes | 14.37 |

The four baseline-associated scores span 24.54–27.85. This is descriptive spread in one account, not a confidence interval or an estimate of variance for identical binaries. We cannot separate execution randomness from artifact or evaluation differences without the missing provenance.

None of the listed modified submissions exceeds the initial 27.85 observation. The v3 description includes a local “39.32 benchmark” claim, while its recorded public score is 6.52. The description alone does not validate the local benchmark's task set, metric, seeds or scoring implementation. We exclude it from quantitative comparison. The discrepancy demonstrates a need to audit comparability, not a measured causal effect of masking or batching.

## Interpretation and limits

Our attempted configuration changes did not produce a higher observed public score in this snapshot. Several interventions changed multiple factors together. Differences cannot be assigned to concurrency, time allocation, spatial masking or symbolic integration individually. One failed submission also does not show that its underlying idea is generally ineffective.

We have no verified latency measurements, utilization traces, paired per-game outcomes or independent offline validation set supporting a speedup claim. The earlier manuscript's architectural novelty, attention-mask proof and synthetic ablation table have been withdrawn. Local tests of document structure cannot establish experimental accuracy.

Universality beyond these submissions is untested. Public leaderboard performance may differ from private evaluation, and repeated public evaluation can influence subsequent choices. Historical results reported by public authors have not been independently reproduced here and are excluded from our numerical dataset.

## Engineering failure modes in agentic game solving

Beyond leaderboard metrics, empirical execution of tool-based game-solving agents reveals several silent failure modes that can corrupt experimental evaluation if unmonitored:

1. **Storage prefetch and cold-start timeouts:** When serving large models distributed across multiple tensor checkpoint shards, disk prefetch and tensor deserialization into accelerator memory can take upwards of twenty minutes under containerized cold-storage conditions. If the orchestration harness enforces an aggressive startup timeout before serving endpoints reach full readiness, benchmark requests fail prematurely with connection errors, producing total submission failure unrelated to model reasoning capabilities.

2. **Introspection loops and inaction deadlocks:** When coding agents operate with unconstrained tool turns per step and receive passive prompt feedback assuring them that purely inspecting state without actions is acceptable, agents frequently stall in prolonged inaction cycles. Models generate repetitive state queries, diff evaluations, and exploratory Python scripts across dozens of turns while executing zero real environment actions. Bounding tool iterations and replacing permissive phrasing with explicit action directives is necessary to force game progress.

3. **Admission gate decoupling from batch serving:** In asynchronous architectures where an inference backend handles concurrent request queues, local admission gates in the solver must be harmonized with server batch limits. An upstream gate admitting fewer concurrent streams than the serving engine can decode leaves accelerator memory underutilized, reducing operational token throughput during constrained evaluation envelopes.

## Reproducibility and next experiments

Before another configuration comparison, archive the exact submitted notebook version, source and model versions, environment, generated artifact and SHA-256 hashes. Match each submission identifier to that manifest, including the baseline-labelled reruns. Record per-game outcomes, scoring definitions, seeds, elapsed time and failure logs without exposing restricted competition data.

Use a fixed held-out development set with matching scoring semantics. Change one factor at a time and compare matched games under the same compute envelope; repeat both baseline and candidate to report uncertainty. Register a stop rule before launching runs. Keep local diagnostics and public leaderboard measurements explicitly separate.

The contribution is a transparent account of reproduction and unsuccessful transfer, plus an auditable evidence trail. Its novelty is limited; progress and completeness depend on releasing the provenance bundle and a working companion. Existing PDF, HTML, figures and notebooks still reflect superseded claims and are not submission-ready. No publication or paper submission is asserted by this draft.
