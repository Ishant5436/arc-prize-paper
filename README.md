# ARC Prize 2026 - Paper Track ($450,000 Prize Pool) Submission Package

[![TDD Invariants](https://img.shields.io/badge/TDD_Invariants-5%2F5_Passing-brightgreen.svg)]()
[![Word Count](https://img.shields.io/badge/Word_Count-1%2C433_%2F_1%2C500-blue.svg)]()
[![Track](https://img.shields.io/badge/Track-ARC--AGI--3-purple.svg)]()
[![Hardware](https://img.shields.io/badge/Target_GPU-NVIDIA_RTX_Pro_6000-orange.svg)]()

## 1. Overview & Competition Metadata
- **Competition:** [ARC Prize 2026 - Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track)
- **Prize Pool:** **$450,000 USD** (Includes $375,000 Bonus Pool divided among all submissions scoring $\ge 4.5/5.0$)
- **Competitor Field:** 227 teams worldwide
- **Deadline:** November 9, 2026
- **Tie-Breaker Precedence:** *"In the event of a tie, the Paper that was entered first to the Competition will be the winner."*
- **Primary Submission Reference:** ARC-AGI-3 Submission `#56842502`
- **Leaderboard Score:** **27.85** (Global Rank 404 / 3,796, Top 10.4%)
- **Offline Benchmark Score:** **39.79**

---

## 2. Submission Package Assets

| Asset Type | File Path | Kaggle Requirement |
| :--- | :--- | :--- |
| **Writeup Body** | [`PAPER.md`](file:///Users/ishantpanchal/arc-prize-paper/PAPER.md) | Formatted project report ($\le 1,500$ words). Current: **1,433 words**. |
| **Media Gallery Cover** | [`figures/cover_image.png`](file:///Users/ishantpanchal/arc-prize-paper/figures/cover_image.png) | 16:9 high-resolution banner (Required for submission). |
| **Pipeline Diagram** | [`figures/fig1_pipeline_architecture.png`](file:///Users/ishantpanchal/arc-prize-paper/figures/cover_image.png) | Architecture flowchart. |
| **Masking Visual** | [`figures/fig2_spatial_masking.png`](file:///Users/ishantpanchal/arc-prize-paper/figures/fig2_spatial_masking.png) | State-space entropy reduction visualization. |
| **Ablation Chart** | [`figures/fig3_ablation_benchmarks.png`](file:///Users/ishantpanchal/arc-prize-paper/figures/fig3_ablation_benchmarks.png) | Empirical benchmark comparison. |
| **Companion Notebook** | [`notebooks/arc_prize_paper_companion.ipynb`](file:///Users/ishantpanchal/arc-prize-paper/notebooks/arc_prize_paper_companion.ipynb) | Public reproducible code notebook. |

---

## 3. How to Submit on Kaggle Portal

1. **Accept Rules / Join:** Navigate to [ARC Prize 2026 - Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) and click **"Join Competition"**.
2. **Open Writeup Studio:** Click **"New Writeup"** at `https://www.kaggle.com/competitions/arc-prize-2026-paper-track/projects`.
3. **Fill Submission Fields:**
   - **Title:** `Continuous Speculative Batching & Spatial Attention Masking for Interactive ARC-AGI-3`
   - **Subtitle:** `High-Throughput Inductive Reasoning Engine with SGLang on NVIDIA RTX Pro 6000`
   - **Track Selection:** `ARC-AGI-3`
   - **Submission ID:** `56842502`
   - **Cover Image:** Upload [`figures/cover_image.png`](file:///Users/ishantpanchal/arc-prize-paper/figures/cover_image.png)
   - **Writeup Content:** Copy-paste the full text from [`PAPER.md`](file:///Users/ishantpanchal/arc-prize-paper/PAPER.md)
   - **Project Links:** Link to public notebook `rainycloudss/arc-agi-3-milestone-2-solution`.
4. **Submit:** Click **"Submit"** in the top right to lock in the early timestamp.

---

## 4. Verification & Testing Evidence
Run the automated test suite locally:
```bash
pytest tests/test_paper_invariants.py -v
```
All 5/5 tests pass, confirming:
- Word count is strictly bounded between 1,100 and 1,500 words.
- All 6 evaluation rubric criteria (Accuracy, Universality, Progress, Theory, Completeness, Novelty) are addressed.
- Empirical benchmark numbers (27.85 live, 39.79 offline) and hardware specifications are verified.
- Power of 10 invariants (functions $\le 60$ lines) are strictly enforced.
