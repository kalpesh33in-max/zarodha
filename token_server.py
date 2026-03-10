from flask import Flask, request
from kiteconnect import KiteConnect
from config import API_KEY, API_SECRET
from scanner import start_scanner

app = Flask(__name__)

kite = KiteConnect(api_key=API_KEY)

@app.route("/login")
def login():

    request_token = request.args.get("request_token")

    data = kite.generate_session(request_token, API_SECRET)

    access_token = data["access_token"]

    kite.set_access_token(access_token)

    start_scanner(kite)

    return "Scanner started"

def start():
    app.run(host="0.0.0.0", port=8080)
