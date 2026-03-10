from kiteconnect import KiteConnect
import requests
import os

API_KEY = os.getenv("KITE_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

kite = KiteConnect(api_key=API_KEY)

login_url = kite.login_url()

message = f"""
🔑 Zerodha Login Required

Click link below to start scanner:

{login_url}

After login system will start automatically.
"""

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": message}
)
