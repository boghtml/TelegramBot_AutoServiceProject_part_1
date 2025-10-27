# TelegramBot_AutoServiceProject_part_1

## Run locally (Windows PowerShell)

1. Copy `.env.example` to `.env` and fill values for `MONGO_URI` and `TELEGRAM_TOKEN`.

2. Create and use a virtual environment and install dependencies:

```powershell
cd "d:\Qt_designer\TelegramBotAutoService\TelegramBotAutoService"
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
```

3. Run the bot (ensure `TELEGRAM_TOKEN` is set in environment or loaded from your environment manager):

```powershell
# If you set environment variable in the current session:
$env:TELEGRAM_TOKEN = 'your_token_here'
# Then run
.venv\Scripts\python main.py
```

Notes:
- Do NOT commit `.env` or any secrets to the repository. `.gitignore` already excludes `.env` and `.venv`.
- If you don't have MongoDB credentials yet, you can still run a syntax-only check using the venv Python:

```powershell
.venv\Scripts\python -m py_compile main.py
```
