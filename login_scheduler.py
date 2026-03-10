from kiteconnect import KiteConnect
import schedule
import time
from config import API_KEY, LOGIN_TIME
from telegram_bot import send

kite = KiteConnect(api_key=API_KEY)

def send_login():

    login_url = kite.login_url()

    msg = f"""
🔐 Zerodha Login Required

Click link below:

{login_url}

After login scanner starts automatically.
"""

    send(msg)

schedule.every().day.at(LOGIN_TIME).do(send_login)

while True:

    schedule.run_pending()

    time.sleep(1)
