from pathlib import Path

import pandas as pd

from src.config import REQUIRED_COLUMNS


def load_posts(path: Path) -> pd.DataFrame:
    """Load and validate a CSV of social posts."""
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}\n"
            "Place the post data in data/posts.csv or provide another path."
        )

    posts = pd.read_csv(path)

    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in posts.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. "
            f"Found columns: {posts.columns.tolist()}"
        )

    if posts.empty:
        raise ValueError("The CSV contains no posts.")

    posts = posts.copy()
    posts["created_at"] = pd.to_datetime(
        posts["created_at"],
        errors="coerce",
        utc=True,
    )
    posts["text"] = posts["text"].fillna("").astype(str)
    posts["platform"] = posts["platform"].fillna("Unknown").astype(str)
    posts["post_id"] = posts["post_id"].fillna("").astype(str)

    posts = posts.dropna(subset=["created_at"])
    posts = posts.drop_duplicates(
        subset=["platform", "post_id"],
        keep="first",
    )

    return posts.reset_index(drop=True)
