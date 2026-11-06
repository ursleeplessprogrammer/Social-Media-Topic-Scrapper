from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def save_reports(
    posts: pd.DataFrame,
    summaries: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:
    """Save matched posts and summary tables as CSV files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    posts.to_csv(output_dir / "matched_posts.csv", index=False)

    for name, summary in summaries.items():
        summary.to_csv(
            output_dir / f"{name}_summary.csv",
            index=False,
        )


def save_daily_chart(
    daily_summary: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save a chart of matched posts per day."""
    if daily_summary.empty:
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(11, 5))
    plt.plot(
        daily_summary["date"],
        daily_summary["post_count"],
        marker="o",
    )
    plt.title("Keyword-Matched Public Posts by Day")
    plt.xlabel("Date")
    plt.ylabel("Matched post count")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
