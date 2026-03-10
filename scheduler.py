import schedule
import time
import send_login_link

schedule.every().day.at("08:00").do(send_login_link)

while True:
    schedule.run_pending()
    time.sleep(1)
