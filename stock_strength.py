weights = {
"HDFCBANK":26,
"ICICIBANK":19,
"SBIN":17,
"AXISBANK":9,
"KOTAKBANK":8
}

symbols = [
"NSE:HDFCBANK",
"NSE:ICICIBANK",
"NSE:SBIN",
"NSE:AXISBANK",
"NSE:KOTAKBANK"
]

def calculate_strength(data):

    score = 0

    for s in data:

        ltp = data[s]["last_price"]
        open_price = data[s]["ohlc"]["open"]

        change = ((ltp-open_price)/open_price)*100

        sym = s.split(":")[1]

        score += change * weights[sym]

    return score
