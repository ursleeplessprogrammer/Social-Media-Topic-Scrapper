import pandas as pd

from src.config import KEYWORDS, NEGATIVE_TERMS, TOPIC_TERMS


def contains_any(text: str, terms: list[str]) -> bool:
    """Check whether any term appears in the text."""
    lowered_text = text.lower()
    return any(term.lower() in lowered_text for term in terms)


def analyze_posts(
    posts: pd.DataFrame,
    keywords: list[str],
) -> pd.DataFrame:
    """Filter posts by keywords and add basic labels."""
    result = posts.copy()

    result["text_clean"] = (
        result["text"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    result = result[
        result["text_clean"].apply(
            lambda text: contains_any(text, keywords)
        )
    ].copy()

    def find_topics(text: str) -> str:
        topics = [
            topic
            for topic, terms in TOPIC_TERMS.items()
            if contains_any(text, terms)
        ]
        return ", ".join(topics) if topics else "unclassified"

    def classify_signal(text: str) -> str:
        if contains_any(text, NEGATIVE_TERMS):
            return "possible_issue_report"
        return "general_mention"

    result["topics"] = result["text_clean"].apply(find_topics)
    result["signal"] = result["text_clean"].apply(classify_signal)
    result["date"] = result["created_at"].dt.strftime("%Y-%m-%d")
    result["hour_utc"] = result["created_at"].dt.hour

    return result.reset_index(drop=True)


def summarize_posts(posts: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create summaries by date, platform, topic, and signal."""
    if posts.empty:
        return {
            "daily": pd.DataFrame(columns=["date", "post_count"]),
            "platform": pd.DataFrame(columns=["platform", "post_count"]),
            "topic": pd.DataFrame(columns=["topic", "post_count"]),
            "signal": pd.DataFrame(columns=["signal", "post_count"]),
        }

    daily = (
        posts.groupby("date")
        .size()
        .rename("post_count")
        .reset_index()
        .sort_values("date")
    )

    platform = (
        posts.groupby("platform")
        .size()
        .rename("post_count")
        .reset_index()
        .sort_values("post_count", ascending=False)
    )

    topic = (
        posts.assign(topic=posts["topics"].str.split(", "))
        .explode("topic")
        .groupby("topic")
        .size()
        .rename("post_count")
        .reset_index()
        .sort_values("post_count", ascending=False)
    )

    signal = (
        posts.groupby("signal")
        .size()
        .rename("post_count")
        .reset_index()
        .sort_values("post_count", ascending=False)
    )

    return {
        "daily": daily,
        "platform": platform,
        "topic": topic,
        "signal": signal,
    }
