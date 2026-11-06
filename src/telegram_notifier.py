import os

import requests


TELEGRAM_API = "https://api.telegram.org"


def send_telegram_message(message: str) -> None:
    """Send a plain-text message to the configured Telegram chat."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise RuntimeError(
            "Telegram is enabled, but TELEGRAM_BOT_TOKEN or "
            "TELEGRAM_CHAT_ID is missing."
        )

    response = requests.post(
        f"{TELEGRAM_API}/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": True,
        },
        timeout=20,
    )
    response.raise_for_status()

    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API returned an error: {result}")
