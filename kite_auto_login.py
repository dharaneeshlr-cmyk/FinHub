#!/usr/bin/env python3
"""
BudgetCraft — Kite Auto-Login Script
Run once each morning before syncing holdings.
Usage : python kite_auto_login.py
Needs : pip install requests pyotp
"""
import sqlite3, hashlib, pyotp, requests, sys, os

# ── CONFIGURATION ──────────────────────────────────────────────────────────
API_KEY      = "hi30f0cztcpm37av"
API_SECRET   = "00mxqst9dpzknjunr551gkwqwqdw8jfi"
ZERODHA_ID   = "JQG304"
ZERODHA_PASS = "anju@143"
TOTP_SECRET  = "ZN76WVHEUMV6HBK4ZNTO34QNSAJAEYEX"   # 32-char base32 key from Zerodha 2FA setup page
DB_PATH      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget.db")
# ──────────────────────────────────────────────────────────────────────────

def get_access_token():
    sess = requests.Session()
    sess.headers.update({"X-Kite-Version": "3", "User-Agent": "Mozilla/5.0"})

    # Step 1 — Password login
    r = sess.post("https://kite.zerodha.com/api/login",
                  data={"user_id": ZERODHA_ID, "password": ZERODHA_PASS})
    r.raise_for_status()
    d = r.json()
    if d.get("status") != "success":
        raise Exception(f"Login failed: {d.get('message')}")
    req_id = d["data"]["request_id"]
    print(f"  Step 1 ✓  Password accepted")

    # Step 2 — TOTP 2FA
    totp_val = pyotp.TOTP(TOTP_SECRET).now()
    r = sess.post("https://kite.zerodha.com/api/twofa",
                  data={"user_id": ZERODHA_ID, "request_id": req_id,
                        "twofa_value": totp_val, "skip_session": ""})
    r.raise_for_status()
    d = r.json()
    if d.get("status") != "success":
        raise Exception(f"2FA failed: {d.get('message')}")
    print(f"  Step 2 ✓  TOTP accepted")

    # Step 3 — Grab request_token from redirect Location header
    r = sess.get(
        f"https://kite.zerodha.com/connect/login?api_key={API_KEY}&v=3",
        allow_redirects=False
    )
    location = r.headers.get("Location", "")
    req_token = None
    for part in location.split("&"):
        if "request_token=" in part:
            req_token = part.split("request_token=")[-1].split("&")[0]
            break
    if not req_token:
        # Fallback: follow redirect and parse final URL
        from urllib.parse import urlparse, parse_qs
        r2 = sess.get(f"https://kite.zerodha.com/connect/login?api_key={API_KEY}&v=3")
        params = parse_qs(urlparse(r2.url).query)
        req_token = (params.get("request_token") or [""])[0]
    if not req_token:
        raise Exception("Could not find request_token in redirect URL")
    print(f"  Step 3 ✓  request_token obtained")

    # Step 4 — Exchange for access_token
    checksum = hashlib.sha256(
        f"{API_KEY}{req_token}{API_SECRET}".encode()
    ).hexdigest()
    r = sess.post("https://api.kite.trade/session/token",
                  data={"api_key": API_KEY,
                        "request_token": req_token,
                        "checksum": checksum})
    r.raise_for_status()
    d = r.json()
    if d.get("status") != "success":
        raise Exception(f"Token exchange failed: {d.get('message')}")
    print(f"  Step 4 ✓  access_token received")
    return d["data"]["access_token"]

def save_token_to_db(token):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS kite_config
                    (key TEXT PRIMARY KEY, value TEXT NOT NULL)""")
    conn.execute("INSERT OR REPLACE INTO kite_config (key,value) VALUES ('access_token',?)",
                 (token,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("🔐 BudgetCraft — Kite Auto-Login")
    print("─" * 36)
    try:
        token = get_access_token()
        save_token_to_db(token)
        print(f"✅ Done!  Token saved: {token[:10]}…")
        print("   Open the Investment Tracker and click Sync Holdings.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)