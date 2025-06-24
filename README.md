# Pastebin Keyword Crawler

A Python tool to scrape Pastebin's public archive for pastes containing cryptocurrency-related keywords or Telegram links, and save the results in a structured JSONL format.

## Features

- Scrapes the latest 30 pastes from Pastebin's public archive.
- Searches for crypto-related keywords (e.g., "crypto", "bitcoin", "ethereum", "blockchain", "btc", "eth", "nft", "defi", "wallet", "binance", "coinbase") and Telegram links ("t.me").
- Multi-threaded for fast crawling.
- Rate limiting and random delays to avoid being blocked.
- Comprehensive logging to both file and console.
- Outputs results in JSONL format, one JSON object per line.

## Requirements

- Python 3.7+
- Internet connection

### Python Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install requests beautifulsoup4
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the crawler with:

```bash
python pastebinkeywordcrawler/pastein.py
```

By default, results are saved to `pastebinkeywordcrawler/keyword_matches.jsonl`.

### Customization

- To change the keywords or output file, modify the `PastebinCrawler` initialization in `pastein.py`.
- To adjust the number of threads, change the `max_workers` parameter in the `run()` method.

## Output Format

Each matching paste is saved as a JSON object in `keyword_matches.jsonl`:

```json
{
  "source": "pastebin",
  "context": "Found crypto-related content in Pastebin paste ID abc123",
  "paste_id": "abc123",
  "url": "https://pastebin.com/raw/abc123",
  "discovered_at": "2025-05-12T10:00:00Z",
  "keywords_found": ["crypto", "bitcoin"],
  "status": "pending"
}
```

## Logging

- Logs are saved to `pastebinkeywordcrawler/crawler.log` and also printed to the console.
- Each paste is logged as processed, skipped, or matched.

## Best Practices

- Respect Pastebin's Terms of Service.
- Do not use this tool for illegal activities.
- Be mindful of rate limits and avoid excessive requests.

## Legal Notice

This tool is for educational and research purposes only. Do not use it to access private or unauthorized content.
