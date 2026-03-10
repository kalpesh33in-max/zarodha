import time
from telegram_bot import send
from stock_strength import calculate_strength

def start_scanner(kite):

    while True:

        symbols = [
        "NSE:HDFCBANK",
        "NSE:ICICIBANK",
        "NSE:SBIN",
        "NSE:AXISBANK",
        "NSE:KOTAKBANK"
        ]

        data = kite.quote(symbols)

        score = calculate_strength(data)

        if score > 30:

            send(f"🚀 BANKNIFTY STRONG BULLISH\nScore={score}")

        elif score < -30:

            send(f"📉 BANKNIFTY STRONG BEARISH\nScore={score}")

        time.sleep(60)
