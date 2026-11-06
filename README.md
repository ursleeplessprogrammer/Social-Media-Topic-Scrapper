# 🔎 Social Media Topic Scrapper

<p align="center">
      <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
      <img src="https://img.shields.io/badge/IDE-Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" />
      <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />

</p>

> **Search permitted public-post data by topic, explore emerging discussions, and receive summaries in Telegram.**

## 📌 Project Overview

This is a Python project that analyzes social-media posts related to user-selected keywords or topics. It reads posts from a CSV, filters them by search terms, assigns simple topic labels, summarizes results by date and platform, and creates a chart.

Optionally, the project sends a short summary of the results to a Telegram chat.

This project **does not scrape social-media platforms**. Post data must be obtained through an authorized API or permitted export. Results are exploratory and may contain duplicates, irrelevant posts, or incorrect topic labels.

## 🗺️ Contents

- [Project Goals](#-project-goals)
- [How It Works](#-how-it-works)
- [Data Sources and Platform Access](#-data-sources-and-platform-access)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Input Data](#-input-data)
- [Setup](#-setup)
- [Telegram Setup](#-telegram-setup)
- [Run the Project](#-run-the-project)
- [Command-Line Options](#️-command-line-options)
- [Generated Output](#-generated-output)
- [Sample Telegram Message](#-sample-telegram-message)
- [Limitations and Responsible Use](#️-limitations-and-responsible-use)

## 🎯 Project Goals

- Analyze posts about a user-selected topic or keyword.
- Match posts using configurable search phrases.
- Group matching posts into simple topic categories.
- Summarize post counts by date, platform, topic, and signal.
- Create CSV reports and a daily activity chart.
- Optionally send a summary notification through Telegram.

## 🔄 How It Works

```text
Authorized API data or permitted post export
                    ↓
              Load post records
                    ↓
        Match user-selected keywords
                    ↓
   Add simple topic and signal categories
                    ↓
       Save summaries and a daily chart
                    ↓
      Optionally send summary to Telegram
```

1. **Collect or import data:** Obtain post data through an authorized API or permitted export.
2. **Load and validate:** Read the CSV and check that required fields are present.
3. **Match keywords:** Keep posts containing one or more configured phrases.
4. **Analyze matches:** Assign basic topic and signal labels using configured word lists.
5. **Create reports:** Save matching posts, summaries, and a chart.
6. **Notify through Telegram:** If enabled, send a concise summary to a configured chat.

## 🔌 Data Sources and Platform Access

This project reads a CSV file; it does not connect directly to Instagram, Facebook, X, Threads, or other platforms.

Platform access varies. Before collecting or storing posts:

- Review the platform’s current official API documentation and terms.
- Use only endpoints and permissions you are authorized to access.
- Respect rate limits, retention requirements, and privacy rules.
- Do not collect private posts, direct messages, or restricted content.
- Avoid scraping in ways that violate platform terms.

The CSV-based design keeps analysis separate from platform-specific authentication and access requirements.

## 🧰 Technology Stack

- **Python** — application language
- **Pandas** — data loading and analysis
- **Matplotlib** — chart generation
- **Requests** — Telegram Bot API calls
- **Telegram Bot API** — optional notifications

## 📁 Project Structure

```text
social-media-topic-insights/
├── data/
│   └── posts.csv
├── output/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── load_data.py
│   ├── analyze_posts.py
│   ├── report.py
│   ├── telegram_notifier.py
│   └── main.py
├── requirements.txt
└── README.md
```

- `src/config.py` stores paths, keywords, and topic terms.
- `src/load_data.py` loads and validates the input CSV.
- `src/analyze_posts.py` filters posts, assigns labels, and creates summaries.
- `src/report.py` saves CSV reports and the chart.
- `src/telegram_notifier.py` sends a summary through Telegram.
- `src/main.py` coordinates the project.
- `src/__init__.py` marks `src` as a Python package.
- `data/` contains input data.
- `output/` contains generated reports and charts.

## 📥 Input Data

Create `data/posts.csv` with these required columns:

| Column | Purpose |
|---|---|
| `platform` | Source platform name |
| `post_id` | Post identifier used for deduplication |
| `created_at` | Post creation timestamp |
| `text` | Post text |

An optional `url` column can contain a link to a post, if storing it is permitted.

Example:

```csv
platform,post_id,created_at,text,url
X,post-001,2026-04-12T10:30:00Z,"Looking for thoughts on the latest app update",https://example.com/post-001
Threads,post-002,2026-04-12T10:45:00Z,"This new product feature is interesting",https://example.com/post-002
Instagram,post-003,2026-04-12T11:00:00Z,"Anyone else tried the new service?",https://example.com/post-003
```

These example records and URLs are placeholders, not real posts.

## ⚙️ Setup

Use Python 3. Create a virtual environment if desired:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS or Linux**

```bash
source .venv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
pandas
matplotlib
requests
```

## 📲 Telegram Setup

Telegram notifications are optional. The project sends a summary only; it does not send every matching post.

### 1. Create a bot

Create a bot through Telegram’s **@BotFather** and copy its token. Keep the token private.

### 2. Get your chat ID

Start a conversation with your bot and send it a message. Then obtain your chat ID using the Telegram Bot API’s update methods or another trusted method.

### 3. Set environment variables

The application reads the bot token and chat ID from environment variables.

**macOS or Linux:**

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

**Windows PowerShell:**

```powershell
$env:TELEGRAM_BOT_TOKEN="your-bot-token"
$env:TELEGRAM_CHAT_ID="your-chat-id"
```

Do not put your bot token in Python source code, your CSV, or a public GitHub repository. If it is exposed, revoke it through @BotFather and create a new one.

## ▶️ Run the Project

Run the analysis without sending a Telegram message:

```bash
python -m src.main
```

Send a summary to Telegram:

```bash
python -m src.main --telegram
```

## 🏷️ Command-Line Options

### Specify another input file

```bash
python -m src.main --input data/exported_posts.csv
```

### Select an output directory

```bash
python -m src.main --output results
```

### Search custom phrases

```bash
python -m src.main --keywords "product launch" "new feature" "customer feedback"
```

### Combine options and send a Telegram notification

```bash
python -m src.main \
  --input data/exported_posts.csv \
  --output output \
  --keywords "product launch" "new feature" \
  --telegram
```

On Windows Command Prompt, enter the command on one line or use its supported line-continuation syntax.

## 📤 Generated Output

The project writes results to the selected output directory:

```text
output/
├── matched_posts.csv
├── daily_summary.csv
├── platform_summary.csv
├── topic_summary.csv
├── signal_summary.csv
└── daily_post_volume.png
```

- **`matched_posts.csv`** — posts matching configured keywords, with derived analysis fields.
- **`daily_summary.csv`** — matching-post counts by date.
- **`platform_summary.csv`** — counts by source platform.
- **`topic_summary.csv`** — counts by configured topic.
- **`signal_summary.csv`** — counts by basic signal label.
- **`daily_post_volume.png`** — chart of matching-post volume over time.

## 💬 Sample Telegram Message

When run with `--telegram`, the project sends a summary similar to this:

```text
🔎 Social Media Topic Insights

Search terms: product launch, new feature
Matched posts: 42

Top topics:
• feedback: 20
• availability: 12
• login: 7
• unclassified: 3

By platform:
• X: 24
• Threads: 12
• Instagram: 6

These are keyword-based exploratory results, not verified findings.
```

This is an illustrative example; actual results depend on the input CSV and configured terms.

## 📖 Understanding the Results

### Keyword matches

A post is included if its text contains at least one configured phrase. Simple text matching may miss spelling variations, slang, abbreviations, and other languages. It may also match a phrase used in an unrelated context.

### Topic labels

Topic labels are assigned using configured word lists. They are a starting point for exploration, not a reliable interpretation of every post.

### Post volume

A rise in matching posts may be worth investigating, but it does not necessarily mean that public interest has increased. It could also result from duplicate posts, reposts, sampling differences, API limits, or changes in collection.

### Platform comparisons

Platform totals only describe the records collected. They are not directly comparable if platforms have different search coverage, APIs, limits, or collection periods.

## ⚠️ Limitations and Responsible Use

- The project analyzes only records supplied through its input CSV.
- It does not collect posts from platforms.
- Results depend on data sources, search terms, and collection coverage.
- Keyword matching can produce false positives and miss relevant posts.
- Topic and signal labels are rule-based, not verified classifications.
- Public posts do not represent all users or the wider population.
- A post should not be treated as verified fact without corroboration.
- Avoid storing unnecessary personal or sensitive information.
- Follow platform terms, API permissions, privacy requirements, and retention rules.
- Use the results for exploration and human review, not as the sole basis for consequential decisions.

## 🔗 References

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram: Creating a bot](https://core.telegram.org/bots/tutorial)

---
## 📄 License

Please refer to the repository for applicable licensing information.

## 👨‍💻 Author

**ursleeplessprogrammer**

*This project analyzes topic-related post data and can send a summary to Telegram. Its output describes the records collected and the rules applied—not the views of everyone discussing the topic.*
