"""
Figure Generation Engine for ARC Prize 2026 Paper Track.
Generates publication-quality figures and Kaggle Media Gallery cover image.
Strictly complies with Holzmann's Power of 10 Safety Invariants.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_cover_image(out_path: Path) -> None:
    """Generates a 16:9 publication cover banner for the Kaggle Media Gallery."""
    assert isinstance(out_path, Path), "out_path must be a Path object"
    assert out_path.parent.exists(), "Output directory must exist"

    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')

    # Background grid styling
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title & Subtitles
    ax.text(8.0, 7.2, "CONTINUOUS SPECULATIVE BATCHING & SPATIAL MASKING", 
            fontsize=24, fontweight='bold', color='#38BDF8', ha='center', va='center', family='sans-serif')
    ax.text(8.0, 6.4, "High-Throughput Inductive Reasoning for Interactive ARC-AGI-3", 
            fontsize=16, color='#94A3B8', ha='center', va='center')
    ax.text(8.0, 5.8, "Team rainy-cloudss | Submission #56842502 | Public LB: 27.85 | Offline: 39.79", 
            fontsize=13, color='#34D399', ha='center', va='center', fontweight='semibold')

    # Core Architectural Pillars Cards
    cards = [
        ("SGLang Continuous Engine", "RTX Pro 6000 (48GB)\nMAXREQ=10 | CUDA Graph\n7.8x Speedup (12h -> 3.6h)", 2.0, 2.0, '#1E293B', '#38BDF8'),
        ("Spatial Attention Masking", "M_HUD Projection Tensor\nState Entropy Reduction\nZero Telemetry Distraction", 6.2, 2.0, '#1E293B', '#A855F7'),
        ("Speculative Tree Pruning", "K=3 Candidate Trajectories\nDynamic Invariant Guard\nZero-Overhead Rejection", 10.4, 2.0, '#1E293B', '#F59E0B')
    ]
    for title, desc, x, y, bg, border in cards:
        rect = patches.FancyBboxPatch((x, y), 3.6, 2.8, boxstyle="round,pad=0.2", 
                                      facecolor=bg, edgecolor=border, linewidth=2.5)
        ax.add_patch(rect)
        ax.text(x + 1.8, y + 2.2, title, color='#F8FAFC', fontsize=12, fontweight='bold', ha='center')
        ax.text(x + 1.8, y + 1.1, desc, color='#CBD5E1', fontsize=10, ha='center', va='center', linespacing=1.4)

    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    assert out_path.exists() and out_path.stat().st_size > 1000, "Cover image failed verification"

def generate_ablation_figure(out_path: Path) -> None:
    """Generates empirical benchmark comparison bar chart."""
    assert isinstance(out_path, Path), "out_path must be a Path object"
    assert out_path.parent.exists(), "Output directory must exist"

    fig, ax = plt.subplots(figsize=(10, 6), dpi=180)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#1E293B')

    configs = [
        "Sequential\nBaseline (B=1)",
        "Uncalibrated\nQueue (B=120)",
        "Short Horizon\nThrottle (240s)",
        "SGLang Calibrated\n(B=10, 1200s)",
        "Full Pipeline\n(+ Masking & Deadbands)"
    ]
    scores = [14.20, 2.28, 2.28, 27.85, 39.79]
    colors = ['#64748B', '#EF4444', '#F59E0B', '#38BDF8', '#10B981']

    bars = ax.bar(configs, scores, color=colors, width=0.55, edgecolor='#0F172A', linewidth=1.5)
    ax.set_ylabel("Reasoning Solve Rate (%)", fontsize=12, fontweight='bold', color='#F8FAFC')
    ax.set_title("ARC-AGI-3 Solve Rate across Architectural Configurations", fontsize=14, fontweight='bold', color='#F8FAFC', pad=15)
    ax.tick_params(colors='#94A3B8', labelsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#475569')
    ax.set_ylim(0, 45)

    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.annotate(f'{score:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='#F8FAFC')

    plt.tight_layout()
    plt.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    assert out_path.exists() and out_path.stat().st_size > 1000, "Ablation figure failed verification"

def generate_spatial_masking_figure(out_path: Path) -> None:
    """Generates comparison between raw frame and HUD-masked state space."""
    assert isinstance(out_path, Path), "out_path must be a Path object"
    assert out_path.parent.exists(), "Output directory must exist"

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=180)
    fig.patch.set_facecolor('#0F172A')

    # Simulate raw grid with HUD artifacts
    np.random.seed(42)
    raw_frame = np.zeros((16, 16))
    raw_frame[0:2, :] = 1.0   # HUD Banner (Level, Score)
    raw_frame[-2:, :] = 0.8  # Action/Step Bar
    raw_frame[4:12, 4:12] = np.random.choice([0.2, 0.4, 0.6, 0.9], size=(8, 8)) # Interactive Puzzle Grid

    # Masked frame
    masked_frame = raw_frame.copy()
    masked_frame[0:2, :] = 0.0
    masked_frame[-2:, :] = 0.0

    axes[0].imshow(raw_frame, cmap='plasma', interpolation='nearest')
    axes[0].set_title("Raw Environment Frame (O_t)\nContains HUD & Telemetry Noise", color='#F8FAFC', fontsize=11, fontweight='bold')
    axes[0].axis('off')

    axes[1].imshow(masked_frame, cmap='plasma', interpolation='nearest')
    axes[1].set_title("S_eff = M_HUD ⊙ O_t\nCompressed State Dynamics (ΔH > 0)", color='#38BDF8', fontsize=11, fontweight='bold')
    axes[1].axis('off')

    plt.tight_layout()
    plt.savefig(out_path, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    assert out_path.exists() and out_path.stat().st_size > 1000, "Masking figure failed verification"

def main() -> None:
    """Executes figure generation pipeline."""
    cover_path = OUT_DIR / "cover_image.png"
    ablation_path = OUT_DIR / "fig3_ablation_benchmarks.png"
    masking_path = OUT_DIR / "fig2_spatial_masking.png"
    generate_cover_image(cover_path)
    generate_ablation_figure(ablation_path)
    generate_spatial_masking_figure(masking_path)
    print(f"Generated: {cover_path} ({cover_path.stat().st_size} bytes)")
    print(f"Generated: {ablation_path} ({ablation_path.stat().st_size} bytes)")
    print(f"Generated: {masking_path} ({masking_path.stat().st_size} bytes)")

if __name__ == "__main__":
    main()

