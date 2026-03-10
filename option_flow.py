def detect_flow(option_data):

    bullish = 0
    bearish = 0

    for strike in option_data:

        price_change = strike["price_change"]
        oi_change = strike["oi_change"]

        if price_change > 0 and oi_change > 0:
            bullish += 1

        if price_change < 0 and oi_change > 0:
            bearish += 1

    return bullish, bearish
