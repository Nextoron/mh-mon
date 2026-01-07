import os
import hashlib
import requests

URL = "https://www.milehighcomics.com/highgrade/main.html"
WEBHOOK = os.environ["DISCORD_WEBHOOK_URL"]
STATE_FILE = "state.txt"

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="ignore")).hexdigest()

def post(msg: str):
    r = requests.post(WEBHOOK, json={"content": msg}, timeout=20)
    r.raise_for_status()

def main():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()

    current = sha256(r.text)

    old = None
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            old = f.read().strip()
    except FileNotFoundError:
        pass

    # First run: initialize state, no alert
    if not old:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            f.write(current)
        return

    if current != old:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            f.write(current)
        post(f"🟢 Mile High page changed: {URL}")

if __name__ == "__main__":
    main()
