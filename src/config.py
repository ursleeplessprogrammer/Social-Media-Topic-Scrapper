from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT_DIR / "data" / "posts.csv"
OUTPUT_DIR = ROOT_DIR / "output"

REQUIRED_COLUMNS = [
    "platform",
    "post_id",
    "created_at",
    "text",
]

KEYWORDS = [
    "bank app",
    "mobile banking",
    "product launch",
    "new feature",
]

TOPIC_TERMS = {
    "login": [
        "login",
        "log in",
        "sign in",
        "password",
    ],
    "payments and transfers": [
        "transfer",
        "payment",
        "transaction",
        "send money",
    ],
    "availability": [
        "down",
        "outage",
        "not working",
        "unavailable",
        "crash",
        "crashing",
    ],
    "feedback": [
        "feature",
        "update",
        "feedback",
        "review",
        "experience",
    ],
}

NEGATIVE_TERMS = [
    "can't",
    "cannot",
    "unable",
    "failed",
    "failing",
    "error",
    "issue",
    "problem",
    "not working",
    "down",
    "outage",
    "crash",
    "crashing",
]
