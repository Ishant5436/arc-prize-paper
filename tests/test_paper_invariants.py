"""Document/evidence consistency checks, not scientific result validation."""

import csv
import hashlib
import re
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent.parent
PAPER_FILE = PAPER_DIR / "PAPER.md"
SNAPSHOT = PAPER_DIR / "evidence/2026-10-15-submissions.csv"


def count_words(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return len(text.split())


def test_word_limit():
    assert 0 < count_words(PAPER_FILE.read_text()) <= 1500


def test_all_table_observations_match_snapshot():
    with SNAPSHOT.open(newline="") as stream:
        rows = {row["ref"]: row for row in csv.DictReader(stream)}
    table = re.findall(r"^\| (\d{8}) \|.*?\| ([\d.]+) \|$", PAPER_FILE.read_text(), re.M)
    assert {ref for ref, _ in table} == set(rows)
    for ref, score in table:
        assert float(score) == float(rows[ref]["publicScore"])
        assert rows[ref]["status"] == "SubmissionStatus.COMPLETE"


def test_snapshot_integrity_and_local_evidence_links():
    audit = (PAPER_DIR / "evidence/CLAIM_AUDIT.md").read_text()
    assert hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest() in audit
    for path in re.findall(r"\]\((evidence/[^)]+)\)", PAPER_FILE.read_text()):
        assert (PAPER_DIR / path).is_file()
    assert "evidence/2026-10-15-submissions.csv" in PAPER_FILE.read_text()
    assert "evidence/CLAIM_AUDIT.md" in PAPER_FILE.read_text()


def test_missing_provenance_and_asset_status_disclosed():
    paper = PAPER_FILE.read_text().lower()
    readme = (PAPER_DIR / "README.md").read_text().lower()
    assert "hashes have not established binary identity" in paper
    assert "not controlled ablations" in paper
    assert "not submission-ready" in paper
    for asset in ("paper.pdf", "paper.html", "figures/", "notebooks/"):
        assert asset in readme
    assert "obsolete/unverified" in readme
    assert "do not validate experiments" in readme


def test_withdrawn_numbers_do_not_return_as_paper_results():
    paper = PAPER_FILE.read_text()
    for unsupported in ("39.79", "34.12", "18.50", "11.40", "8.33", "14.20", "2.28", "7.8", "182 ms", "23 ms"):
        assert not re.search(r"(?<![0-9])" + re.escape(unsupported) + r"(?![0-9])", paper)
    assert "dfranzen" in paper
    assert "https://www.kaggle.com/datasets/dfranzen/" in paper
