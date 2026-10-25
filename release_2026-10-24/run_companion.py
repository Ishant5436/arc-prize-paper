from pathlib import Path
import hashlib
import io
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

SNAPSHOT = 'ref,fileName,date,description,status,publicScore,privateScore\n57575277,submission.parquet,2026-10-24 00:01:04.460000,D-prime fork v3 retry after system error,SubmissionStatus.ERROR,,\n57541607,submission.parquet,2026-10-23 00:01:05.220000,milestone-2-solution v19 (fallback after D-prime v3 scored ERROR),SubmissionStatus.COMPLETE,14.40,\n57501028,submission.parquet,2026-10-22 00:01:06.247000,D-prime fork v3: early benchmark release + gateway keepalive,SubmissionStatus.ERROR,,\n57456808,submission.parquet,2026-10-21 00:01:05.950000,"fork dennis6886/arc3-d-prime-public-base, unmodified",SubmissionStatus.COMPLETE,0.00,\n57413236,submission.parquet,2026-10-20 00:01:05.047000,v1 envelope re-run (27.08% / 27.85% certified baseline),SubmissionStatus.COMPLETE,0.00,\n57372927,submission.parquet,2026-10-19 00:01:06.167000,Kernel v23: 1200s Runtime Budget Restored + Duck REPL Multi-Level (SGLang 32),SubmissionStatus.COMPLETE,3.79,\n57329829,submission.parquet,2026-10-18 00:01:05.637000,"Kernel v19: Authentic Parquet Serializer + Leap 68 Harmonized Serving (41.78% Benchmark, 100% sb26, 71% tr87)",SubmissionStatus.COMPLETE,23.43,\n57287079,submission.parquet,2026-10-17 00:01:03.930000,Kernel v18: Leap 68 Harmonized 32-Batch SGLang + 32 Concurrency + 180s Timeout Floor,SubmissionStatus.COMPLETE,0.00,\n57247270,submission.parquet,2026-10-16 00:01:03.517000,"Kernel v16: 0.96 VRAM Allocator + 14-Stream Calibrated Concurrency (35.41 Benchmark, 2 Games 100%)",SubmissionStatus.COMPLETE,14.49,\n57198437,submission.parquet,2026-10-15 00:01:05.990000,v1 envelope re-run,SubmissionStatus.COMPLETE,24.54,\n57159612,submission.parquet,2026-10-14 00:01:05.857000,v1 envelope re-run,SubmissionStatus.COMPLETE,27.08,\n57126448,submission.parquet,2026-10-13 01:41:39.607000,Kernel v15: Clean Native Sandbox + 0.90 VRAM OOM Shield + 120 Streams,SubmissionStatus.COMPLETE,14.37,\n57088385,submission.parquet,2026-10-12 00:01:31.747000,Kernel v13: Clean Symbolic Engine V2 Sandbox Integration,SubmissionStatus.COMPLETE,0.00,\n57059778,submission.parquet,2026-10-11 02:35:08.897000,"ARC-AGI-3 v7: SGLang concurrency=10, spatial HUD masking, 1200s calibrated horizon",SubmissionStatus.COMPLETE,7.72,\n57028832,submission.parquet,2026-10-10 02:51:02.627000,"ARC-AGI-3 v6: SGLang 120 continuous batching streams, 532m envelope on RTX Pro 6000",SubmissionStatus.COMPLETE,25.05,\n57011082,submission.parquet,2026-10-09 13:55:07.853000,"ARC-AGI-3 v4: SGLang concurrency=10, calibrated 240s envelope",SubmissionStatus.COMPLETE,1.00,\n56898814,submission.parquet,2026-10-07 03:22:56.883000,v1 envelope re-run,SubmissionStatus.COMPLETE,26.94,\n56870444,submission.parquet,2026-10-06 04:42:17.620000,"ARC-AGI-3 v3: SGLang concurrency=10, 1200s horizon, HUD spatial masking (39.32 benchmark)",SubmissionStatus.COMPLETE,6.52,\n56842502,submission.parquet,2026-10-05 04:41:04.577000,Milestone 2 solution,SubmissionStatus.COMPLETE,27.85,\n'
EXPECTED_SHA256 = 'fc2c92f155f7903d3f74ed8ce5cbf829d09900fab986d3cde103197c6e2bc7fd'
assert hashlib.sha256(SNAPSHOT.encode()).hexdigest() == EXPECTED_SHA256
observations = pd.read_csv(io.StringIO(SNAPSHOT), dtype={"ref": str})
assert observations.ref.is_unique
observations["date"] = pd.to_datetime(observations["date"], utc=True)
observations["publicScore"] = pd.to_numeric(observations["publicScore"], errors="coerce")
observations["status"] = observations["status"].str.removeprefix("SubmissionStatus.")
completed = observations[observations.status.eq("COMPLETE")].sort_values("date").copy()
errors = observations[observations.status.eq("ERROR")].copy()
assert completed.publicScore.notna().all()
assert completed.publicScore.between(0, 100).all()
assert errors.publicScore.isna().all(), "Do not silently treat failed scoring as zero"
print(observations[["ref", "date", "status", "publicScore", "description"]].to_string(index=False))


figure, axes = plt.subplots(figsize=(11, 6), constrained_layout=True)
positions = list(range(len(completed)))
bars = axes.bar(positions, completed.publicScore, color="#266e9c")
axes.set_xticks(positions, completed.ref, rotation=65, ha="right", fontsize=8)
axes.set_ylabel("Recorded public score")
axes.set_xlabel("Submission reference, chronological order")
axes.set_title("ARC-AGI-3 account observations through 24 October 2026")
axes.set_ylim(0, max(35, completed.publicScore.max() + 5))
axes.bar_label(bars, fmt="%.2f", fontsize=8, padding=3)
axes.spines[["top", "right"]].set_visible(False)
figure.savefig("recorded_scores.png", dpi=180)
plt.close(figure)
print(f"{len(errors)} ERROR submissions excluded from score chart, not assigned score zero.")


best = completed.loc[completed.publicScore.idxmax()]
summary = dict(snapshot_sha256=EXPECTED_SHA256, recorded_submissions=len(observations),
               scored_submissions=len(completed), scoring_errors=len(errors),
               best_public_score=float(best.publicScore), best_submission=str(best.ref),
               error_references=errors.ref.tolist(),
               controlled_ablation=False, binary_identity_verified=False,
               new_solver_evaluation=False)
Path("evidence_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
observations.to_csv("observed_submissions.csv", index=False)
print(json.dumps(summary, indent=2))
