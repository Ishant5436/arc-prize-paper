"""
TDD Invariant & Rubric Validation Suite for ARC Prize 2026 Paper Track.
Ensures adherence to Kaggle's official submission requirements and
Holzmann's Power of 10 Deterministic Safety Invariants.
"""

import os
import re
import ast
import pytest
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent.parent
PAPER_FILE = PAPER_DIR / "PAPER.md"

def count_words(text: str) -> int:
    """Deterministic word counter that strips markdown formatting."""
    assert isinstance(text, str), "Input text must be a string"
    # Remove code blocks and comments
    text_clean = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text_clean = re.sub(r'<!--.*?-->', '', text_clean, flags=re.DOTALL)
    text_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text_clean)  # keep link text
    text_clean = re.sub(r'[#*_`|>-]', ' ', text_clean)
    words = text_clean.split()
    assert len(words) >= 0, "Word count cannot be negative"
    return len(words)

def test_paper_file_exists():
    """Verify that PAPER.md exists and is readable."""
    assert PAPER_FILE.exists(), f"Target file {PAPER_FILE} does not exist"
    assert PAPER_FILE.is_file(), f"{PAPER_FILE} must be a regular file"

def test_word_count_within_kaggle_bounds():
    """Kaggle mandate: Writeup must not exceed 1,500 words."""
    assert PAPER_FILE.exists(), "PAPER.md must exist before checking word count"
    content = PAPER_FILE.read_text(encoding="utf-8")
    words = count_words(content)
    assert 1100 <= words <= 1500, (
        f"Paper word count ({words}) out of bounds! Must be between 1,100 and 1,500 words."
    )

def test_all_six_rubric_categories_explicitly_covered():
    """Verify coverage of all 6 official ARC Paper Track evaluation criteria."""
    assert PAPER_FILE.exists(), "PAPER.md must exist before checking rubric"
    content = PAPER_FILE.read_text(encoding="utf-8").lower()
    required_criteria = [
        "accuracy",
        "universality",
        "progress",
        "theory",
        "completeness",
        "novelty"
    ]
    for criterion in required_criteria:
        assert criterion in content, f"Missing required rubric criterion: {criterion}"

def test_empirical_benchmarks_and_hardware_evidence_cited():
    """Verify concrete empirical benchmark numbers and hardware targets are cited."""
    assert PAPER_FILE.exists(), "PAPER.md must exist before checking citations"
    content = PAPER_FILE.read_text(encoding="utf-8")
    # Live submission ID or score
    assert "27.85" in content, "Must cite live leaderboard score (27.85)"
    assert "39.79" in content, "Must cite offline benchmark score (39.79)"
    assert "56842502" in content or "submission" in content.lower(), "Must cite submission reference"
    # SGLang and Hardware
    assert "SGLang" in content, "Must cite SGLang continuous batching engine"
    assert "RTX Pro 6000" in content or "RTX" in content, "Must cite target GPU accelerator"

def test_power_of_ten_function_lengths():
    """Holzmann Rule 4: No function may exceed 60 lines."""
    test_file = Path(__file__).resolve()
    with open(test_file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1
            assert length <= 60, f"Function {node.name} length {length} > 60 lines"
