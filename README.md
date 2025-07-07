# Finance → Notion Sync (Free & Universal)

Automate ingestion of credit-card and bank transactions into Notion, enrich them with optional AI analytics, and get bill-due reminders via Telegram—**100% free**, runs unattended on GitHub Actions, supports any OFX-compliant institution worldwide.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Quickstart Onboarding (Fully Automatic)](#quickstart-onboarding-fully-automatic)
4. [Manual Setup (Alternative)](#manual-setup-alternative)
5. [Configuration & Secrets](#configuration--secrets)
6. [Connectors Overview](#connectors-overview)
7. [Running Locally](#running-locally)
8. [GitHub Actions Workflow](#github-actions-workflow)
9. [Extending & Customization](#extending--customization)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## Features

* **Global Coverage** via OFX: connect to any bank that supports OFX (URL, org, FID, credentials).
* **EU Banks** via Nordigen (open-banking, free).
* **Capital One** Credit Card API connector.
* **CSV Import** for manual or legacy exports.
* **Notion** upsert: date, vendor, amount, category, card-last4.
* **AI Analytics** (optional) via OpenAI: smart categorization, monthly summary & tips.
* **Bill-Due Reminders** via Telegram Bot.
* **No Paid Cloud**: runs on GitHub’s free Actions tier, state managed in repo.
* **Plugin-Ready**: add your own connectors by implementing the `Connector` interface.

---

## Prerequisites

* **GitHub** account & repository.
* **GitHub PAT** (`GITHUB_TOKEN`) with **repo** + **secrets** scopes.
* **Notion** integration token & database ID:

  1. In Notion → **Settings & Members** → **Integrations** → **+ New integration**
  2. Copy its **Internal Integration Token**.
  3. Share your target database with that integration.
* **Telegram** bot & chat ID:

  1. Chat with [@BotFather](https://t.me/BotFather) → **/newbot** → get **Bot Token**
  2. Send a message to your bot, then request
     `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
     to retrieve your numeric **chat\_id**.
* *(Optional)* **Capital One** API key.
* *(Optional)* **Nordigen** credentials & account IDs.
* *(Optional)* **OFX** details for your bank: URL, ORG, FID, user/pass, account ID/type.
* *(Optional)* **CSV** of historical transactions (`data/transactions.csv`).
* *(Optional)* **OpenAI** API key for analytics.

---

## Quickstart Onboarding (Fully Automatic)

This one-shot script collects your credentials, configures GitHub Secrets, bootstraps state, and commits—all without touching the GitHub UI.

1. **Clone repository**

   ```bash
   git clone https://github.com/<your-org>/finance-notion-sync-free.git
   cd finance-notion-sync-free
   ```

2. **Set environment variables**

   ```bash
   export GITHUB_REPOSITORY="<your-org>/finance-notion-sync-free"
   export GITHUB_TOKEN="<your-PAT-with-repo+secrets-scope>"
   ```

3. **Install dependencies**

   ```bash
   pip install requests cryptography
   ```

4. **Run onboarding script**

   ```bash
   python onboard.py
   ```

   * You’ll be prompted for each secret (Notion, Telegram, OFX, Nordigen, Capital One, CSV path, OpenAI, reminder days).
   * The script encrypts & uploads them to GitHub Actions secrets.
   * It creates `state.json` (30 days ago baseline), commits, and pushes it to `main`.

5. **Done!**
   GitHub Actions will now run your sync nightly—no further manual input required.

---

## Manual Setup (Alternative)

If you prefer to configure everything by hand, skip the onboarding script:

1. **Clone & initialize state**

   ```bash
   git clone https://github.com/<your-org>/finance-notion-sync-free.git
   cd finance-notion-sync-free
   echo '{ "last_timestamp": "2025-07-05T00:00:00Z" }' > state.json
   git add state.json && git commit -m "Init state" && git push
   ```

2. **Add GitHub Secrets**
   In **Settings → Secrets and variables → Actions**, add the secrets listed below.

3. **(Optional) Add CSV file**

   ```bash
   mkdir -p data
   # Create data/transactions.csv with header: id,date,name,amount,category,card_last4
   git add data/transactions.csv && git commit -m "Add CSV sample" && git push
   ```

---

## Configuration & Secrets

| Secret Name              | Description                                            |
| ------------------------ | ------------------------------------------------------ |
| `NOTION_TOKEN`           | Notion Integration Token                               |
| `NOTION_DB_ID`           | Target Notion Database ID                              |
| `TELEGRAM_TOKEN`         | Telegram Bot Token                                     |
| `TELEGRAM_CHAT_ID`       | Telegram Chat ID                                       |
| `OPENAI_API_KEY` (opt.)  | OpenAI API Key (for AI analytics)                      |
| `DUE_REMINDER_DAYS`      | Days before due date to send reminder (default `3`)    |
| `CSV_PATH` (opt.)        | Path to CSV file (default `data/transactions.csv`)     |
| `CAPI_KEY` (opt.)        | Capital One API Key                                    |
| `NORDIGEN_ID` (opt.)     | Nordigen Secret ID                                     |
| `NORDIGEN_SECRET` (opt.) | Nordigen Secret Key                                    |
| `NORDIGEN_ACCOUNT_IDS`   | Comma-separated account IDs for Nordigen connector     |
| `OFX_URL` (opt.)         | OFX server URL (e.g. `https://ofx.bank.com`)           |
| `OFX_ORG`                | OFX organization code                                  |
| `OFX_FID`                | OFX financial institution ID                           |
| `OFX_USER`               | OFX username                                           |
| `OFX_PASS`               | OFX password                                           |
| `OFX_ACCT_ID`            | OFX account ID                                         |
| `OFX_ACCT_TYPE`          | OFX account type (`CHECKING`, `SAVINGS`, `CREDITCARD`) |

> **Tip**: Skip any secrets you don’t need—connectors without config will simply be disabled.

---

## Connectors Overview

* **OFXConnector** (`src/connectors/ofx_connector.py`): any OFX-compliant bank worldwide
* **NordigenConnector** (`src/connectors/nordigen.py`): EU banks via Nordigen open-banking
* **CapitalOneConnector** (`src/connectors/capitalone.py`): Capital One Credit Card API
* **CSVConnector** (`src/connectors/csv_connector.py`): manual CSV import

Each implements:

```python
fetch_transactions(self, since_timestamp: str) -> list[dict]
```

Returns a list of `{ id, date, vendor, amount, category, card_last4 }` objects.

---

## Running Locally

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Export your secrets**

   ```bash
   export NOTION_TOKEN=… NOTION_DB_ID=… \
          TELEGRAM_TOKEN=… TELEGRAM_CHAT_ID=… \
          OFX_URL=… OFX_ORG=… OFX_FID=… OFX_USER=… OFX_PASS=… OFX_ACCT_ID=… OFX_ACCT_TYPE=… \
          CAPI_KEY=… NORDIGEN_ID=… NORDIGEN_SECRET=… NORDIGEN_ACCOUNT_IDS=… \
          OPENAI_API_KEY=… DUE_REMINDER_DAYS=3 CSV_PATH=data/transactions.csv
   ```

3. **Execute sync**

   ```bash
   python src/handlers/cli.py
   ```

4. **Verify**

   * **Console logs** show connector successes/failures and upsert counts
   * **Notion**: new pages in your database
   * **Telegram**: bill-due reminder message

---

## GitHub Actions Workflow

File: `.github/workflows/sync.yml`

```yaml
name: Finance Sync (Free)

on:
  schedule:
    - cron: '0 20 * * *'  # daily at 2 AM IST

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python src/handlers/cli.py
      - name: Commit updated state
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          if [[ -n "$(git status --porcelain)" ]]; then
            git add state.json
            git commit -m "Update last_timestamp"
            git push
          fi
```

---

## Extending & Customization

* **New Connectors**: add a subclass in `src/connectors/` implementing `fetch_transactions()`.
* **Schedule**: modify the `cron` expression in `.github/workflows/sync.yml`.
* **Analytics**: enhance `src/analytics/engine.py` or swap models.
* **Notifications**: replace `TelegramNotifier` with any webhook, email, or Slack integration in `src/notifications/`.
* **State Logic**: adjust retention or timezone handling in `src/utils/state.py`.

---

## Troubleshooting

* **Missing secret**: Action logs or local run will raise `ValueError`. Ensure your GitHub Secret is correctly named & populated.
* **Connector failures**: logs will show `ConnectorName failed: <error>`. Inspect error message & double-check credentials/URLs.
* **No new transactions**: check `state.json` timestamp; consider resetting it further back.
* **Notion errors**: verify integration token and database sharing.
* **Telegram errors**: ensure bot token, chat\_id, and that you’ve messaged your bot at least once.

---

## License

This project is released under the [MIT License](LICENSE).

---

Enjoy a completely free, globally compatible, zero-touch finance sync into Notion! 🚀

