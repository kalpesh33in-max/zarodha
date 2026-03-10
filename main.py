from threading import Thread
import login_scheduler
import token_server

def start_scheduler():
    login_scheduler.start()

def start_server():
    token_server.start()

Thread(target=start_scheduler).start()
Thread(target=start_server).start()
