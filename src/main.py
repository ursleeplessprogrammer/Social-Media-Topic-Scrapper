import argparse
from pathlib import Path

from src.analyze_posts import analyze_posts, summarize_posts
from src.config import INPUT_PATH, KEYWORDS, OUTPUT_DIR
from src.load_data import load_posts
from src.report import save_daily_chart, save_reports
from src.telegram_notifier import send_telegram_message


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze topic-related social posts and optionally notify Telegram."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=INPUT_PATH,
        help="Path to the posts CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory for generated reports.",
    )
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=KEYWORDS,
        help="Phrases to match in post text.",
    )
    parser.add_argument(
        "--telegram",
        action="store_true",
        help="Send a summary to Telegram.",
    )
    return parser.parse_args()


def build_telegram_message(
    matched_posts,
    summaries,
    keywords: list[str],
) -> str:
    """Build a short Telegram notification."""
    top_topics = summaries["topic"].head(5)

    if top_topics.empty:
        topic_lines = ["• No topics were detected."]
    else:
        topic_lines = [
            f"• {row.topic}: {row.post_count}"
            for row in top_topics.itertuples(index=False)
        ]

    platforms = summaries["platform"]
    platform_lines = [
        f"• {row.platform}: {row.post_count}"
        for row in platforms.itertuples(index=False)
    ]

    if not platform_lines:
        platform_lines = ["• No platform counts available."]

    return (
        "🔎 Social Media Topic Insights\n\n"
        f"Search terms: {', '.join(keywords)}\n"
        f"Matched posts: {len(matched_posts)}\n\n"
        "Top topics:\n"
        + "\n".join(topic_lines)
        + "\n\nBy platform:\n"
        + "\n".join(platform_lines)
        + "\n\nThese are keyword-based exploratory results, "
          "not verified findings."
    )


def main():
    args = parse_args()

    posts = load_posts(args.input)
    matched_posts = analyze_posts(posts, args.keywords)
    summaries = summarize_posts(matched_posts)

    save_reports(matched_posts, summaries, args.output)
    save_daily_chart(
        summaries["daily"],
        args.output / "daily_post_volume.png",
    )

    print(f"Input posts loaded: {len(posts):,}")
    print(f"Keyword-matched posts: {len(matched_posts):,}")
    print(f"Reports saved to: {args.output.resolve()}")

    if not matched_posts.empty:
        print("\nPosts by platform:")
        print(summaries["platform"].to_string(index=False))

        print("\nPosts by topic:")
        print(summaries["topic"].to_string(index=False))
    else:
        print("No posts matched the configured keywords.")

    if args.telegram:
        message = build_telegram_message(
            matched_posts=matched_posts,
            summaries=summaries,
            keywords=args.keywords,
        )

        try:
            send_telegram_message(message)
            print("Telegram notification sent.")
        except Exception as error:
            print(f"Telegram notification failed: {error}")


if __name__ == "__main__":
    main()
