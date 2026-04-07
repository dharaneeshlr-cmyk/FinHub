# BudgetCraft — Local Mac App

A personal budget planner that runs entirely on your Mac.
Data is stored in a local SQLite database (`budget.db`).

## Quick Start

```bash
# 1. Open Terminal and go to this folder
cd path/to/budgetcraft-local

# 2. Make the run script executable (first time only)
chmod +x run.sh

# 3. Run the app — it opens your browser automatically
bash run.sh
```

Then visit **http://127.0.0.1:5000** and log in:

| Field    | Value    |
|----------|----------|
| Username | `admin`  |
| Password | `admindr`|

Press **Ctrl+C** in the terminal to stop the server.

---

## Manual Setup (without run.sh)

```bash
cd budgetcraft-local

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the app
python app.py
```

---

## Project Structure

```
budgetcraft-local/
├── app.py              ← Flask server (all routes + SQLite logic)
├── budget.db           ← Created automatically on first run
├── requirements.txt    ← flask + openpyxl
├── run.sh              ← One-click launcher
└── templates/
    ├── login.html      ← Admin login page
    └── index.html      ← Main budget dashboard
```

---

## Features

- 📋 **Budget page** — Income, Insurance, Investments, Expenses, Discretionary
- 📊 **Analysis page** — Monthly / Quarterly / Yearly charts and tables
- ✏️ **Edit entries** — Inline editing for any entry
- ⬇️ **Export** — Download monthly or full-year Excel reports
- 🔒 **Admin login** — Simple single-user login (no signup needed)
- 💾 **SQLite storage** — All data lives in `budget.db` next to `app.py`

---

## Backup your data

Just copy `budget.db` to any safe location. To restore, put it back next to `app.py`.
