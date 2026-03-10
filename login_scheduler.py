import schedule
import time
from kiteconnect import KiteConnect
from config import API_KEY, LOGIN_TIME
from telegram_bot import send

kite = KiteConnect(api_key=API_KEY)

def send_login():

    login_url = kite.login_url()

    send(f"""
🔐 Zerodha Login Required

Click link below:

{login_url}
""")

def start():

    schedule.every().day.at(LOGIN_TIME).do(send_login)

    while True:
        schedule.run_pending()
        time.sleep(1)
