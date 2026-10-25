"""Package public account observations as a standalone CPU notebook."""

import argparse
import ast
import csv
import hashlib
import io
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path('/Users/ishantpanchal/kaggle-portfolio/audits/2026-10-24/arc-prize-2026-arc-agi-3-submissions.csv')
OUTPUT = PROJECT / 'release_2026-10-24'
SLUG = 'arc3-submission-evidence-oct24'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_cell(source):
    ast.parse(source)
    return dict(cell_type='code', execution_count=None, metadata={}, outputs=[], source=source.splitlines(keepends=True))


def markdown_cell(source):
    return dict(cell_type='markdown', metadata={}, source=source.splitlines(keepends=True))


def build(snapshot, output):
    snapshot_text = snapshot.read_text()
    records = list(csv.DictReader(io.StringIO(snapshot_text)))
    if not records or len({record['ref'] for record in records}) != len(records):
        raise ValueError('Snapshot must contain unique submission references')
    for record in records:
        if record['status'] == 'SubmissionStatus.COMPLETE' and not record['publicScore']:
            raise ValueError('A completed submission lacks its public score')
    snapshot_hash = digest(snapshot)
    title = '# ARC-AGI-3: recorded submissions and evaluation limits\n\n'
    title += ('Account observations captured on 24 October 2026 using the authenticated Kaggle CLI. '
              'This notebook reproduces tables and figures from the account export. It evaluates no new solver. '
              'Descriptions are operator labels, not proof of binary identity or controlled ablations.\n\n'
              'Upstream solver assets credited in the paper include '
              '[dfranzen](https://www.kaggle.com/dfranzen). No solver-architecture or speedup claim is made.\n')
    setup = (
        'from pathlib import Path\nimport hashlib\nimport io\nimport json\n'
        'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport pandas as pd\n\n'
        f'SNAPSHOT = {snapshot_text!r}\nEXPECTED_SHA256 = {snapshot_hash!r}\n'
        'assert hashlib.sha256(SNAPSHOT.encode()).hexdigest() == EXPECTED_SHA256\n'
        'observations = pd.read_csv(io.StringIO(SNAPSHOT), dtype={"ref": str})\n'
        'assert observations.ref.is_unique\n'
        'observations["date"] = pd.to_datetime(observations["date"], utc=True)\n'
        'observations["publicScore"] = pd.to_numeric(observations["publicScore"], errors="coerce")\n'
        'observations["status"] = observations["status"].str.removeprefix("SubmissionStatus.")\n'
        'completed = observations[observations.status.eq("COMPLETE")].sort_values("date").copy()\n'
        'errors = observations[observations.status.eq("ERROR")].copy()\n'
        'assert completed.publicScore.notna().all()\n'
        'assert completed.publicScore.between(0, 100).all()\n'
        'assert errors.publicScore.isna().all(), "Do not silently treat failed scoring as zero"\n'
        'print(observations[["ref", "date", "status", "publicScore", "description"]].to_string(index=False))\n'
    )
    plot = (
        'figure, axes = plt.subplots(figsize=(11, 6), constrained_layout=True)\n'
        'positions = list(range(len(completed)))\n'
        'bars = axes.bar(positions, completed.publicScore, color="#266e9c")\n'
        'axes.set_xticks(positions, completed.ref, rotation=65, ha="right", fontsize=8)\n'
        'axes.set_ylabel("Recorded public score")\n'
        'axes.set_xlabel("Submission reference, chronological order")\n'
        'axes.set_title("ARC-AGI-3 account observations through 24 October 2026")\n'
        'axes.set_ylim(0, max(35, completed.publicScore.max() + 5))\n'
        'axes.bar_label(bars, fmt="%.2f", fontsize=8, padding=3)\n'
        'axes.spines[["top", "right"]].set_visible(False)\n'
        'figure.savefig("recorded_scores.png", dpi=180)\n'
        'plt.close(figure)\n'
        'print(f"{len(errors)} ERROR submissions excluded from score chart, not assigned score zero.")\n'
    )
    report = (
        'best = completed.loc[completed.publicScore.idxmax()]\n'
        'summary = dict(snapshot_sha256=EXPECTED_SHA256, recorded_submissions=len(observations),\n'
        '               scored_submissions=len(completed), scoring_errors=len(errors),\n'
        '               best_public_score=float(best.publicScore), best_submission=str(best.ref),\n'
        '               error_references=errors.ref.tolist(),\n'
        '               controlled_ablation=False, binary_identity_verified=False,\n'
        '               new_solver_evaluation=False)\n'
        'Path("evidence_summary.json").write_text(json.dumps(summary, indent=2) + "\\n")\n'
        'observations.to_csv("observed_submissions.csv", index=False)\n'
        'print(json.dumps(summary, indent=2))\n'
    )
    caveats = (
        '## Interpretation\n\n'
        'The chart contains scored account submissions. It cannot identify the cause of differences. '
        'An ERROR means scoring failed and supplies no measured performance value. '
        'Notebook save-run output and a competition scoring rerun are different executions.\n\n'
        'A controlled comparison needs pinned notebook/model/environment versions, matched games, '
        'equal budgets and repeated runs. This export contains no latency traces, per-game outcomes, '
        'private scores or archive hashes establishing executable identity. '
        'No significance, architectural novelty or generalization claim follows from this chart.\n\n'
        'The paper manuscript and upstream licence/provenance review still require final review. '
        'This package is private preparation; it is not a submitted paper.\n'
    )
    notebook = dict(cells=[markdown_cell(title), code_cell(setup), code_cell(plot),
                          code_cell(report), markdown_cell(caveats)],
                    metadata=dict(kernelspec=dict(display_name='Python 3', language='python', name='python3')),
                    nbformat=4, nbformat_minor=4)
    metadata = dict(id=f'rainycloudss/{SLUG}', title='ARC3 Submission Evidence Oct24',
                    code_file=f'{SLUG}.ipynb', language='python', kernel_type='notebook',
                    is_private=True, enable_gpu=False, enable_tpu=False, enable_internet=False,
                    dataset_sources=[], competition_sources=[], kernel_sources=[])
    output.mkdir(parents=True, exist_ok=True)
    notebook_path = output / metadata['code_file']
    notebook_path.write_text(json.dumps(notebook, indent=2) + '\n')
    (output / 'kernel-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (output / 'submissions_snapshot.csv').write_text(snapshot_text)
    (output / 'run_companion.py').write_text('\n\n'.join([setup, plot, report]))
    manifest = dict(source_snapshot=str(snapshot), snapshot_sha256=snapshot_hash,
                    builder_sha256=digest(Path(__file__)),
                    notebook_sha256=digest(notebook_path),
                    metadata_sha256=digest(output / 'kernel-metadata.json'),
                    scientific_scope='Account observations only; no solver evaluation or causal ablation')
    (output / 'build_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Built {notebook_path}; private CPU execution, no external inputs')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, default=SNAPSHOT)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    build(arguments.snapshot, arguments.output)
