import requests
import pandas as pd
from kiteconnect import KiteConnect

BANK_WEIGHTS = {
"HDFCBANK":26,
"SBIN":20,
"ICICIBANK":19,
"KOTAKBANK":8,
"AXISBANK":7
}

BANK_SYMBOLS = [
"NSE:HDFCBANK",
"NSE:SBIN",
"NSE:ICICIBANK",
"NSE:KOTAKBANK",
"NSE:AXISBANK"
]

BANK_FUTURES = [
"HDFCBANK",
"SBIN",
"ICICIBANK",
"KOTAKBANK",
"AXISBANK"
]

class BankNiftyFlow:

    def __init__(self,kite):

        self.kite = kite
        self.instrument_df = self.load_instruments()

    def load_instruments(self):

        url = "https://api.kite.trade/instruments"

        data = requests.get(url).text

        df = pd.read_csv(pd.compat.StringIO(data))

        return df

    def get_bank_strength(self):

        data = self.kite.quote(BANK_SYMBOLS)

        score = 0

        details = []

        for s in data:

            ltp = data[s]["last_price"]
            open_price = data[s]["ohlc"]["open"]

            change = ((ltp-open_price)/open_price)*100

            name = s.split(":")[1]

            weighted = change * BANK_WEIGHTS[name]

            score += weighted

            details.append((name,change))

        return score,details

    def get_bank_futures(self):

        fut_df = self.instrument_df[
        (self.instrument_df["segment"]=="NFO-FUT") &
        (self.instrument_df["name"].isin(BANK_FUTURES))
        ]

        nearest = fut_df.sort_values("expiry").groupby("name").first()

        symbols = []

        for row in nearest.itertuples():

            symbols.append("NFO:"+row.tradingsymbol)

        data = self.kite.quote(symbols)

        return data

    def get_banknifty_future(self):

        fut = self.instrument_df[
        (self.instrument_df["segment"]=="NFO-FUT") &
        (self.instrument_df["name"]=="BANKNIFTY")
        ]

        fut = fut.sort_values("expiry").iloc[0]

        symbol = "NFO:"+fut.tradingsymbol

        data = self.kite.quote([symbol])

        return data

    def get_banknifty_price(self):

        ltp = self.kite.ltp("NSE:NIFTY BANK")

        price = ltp["NSE:NIFTY BANK"]["last_price"]

        return price

    def get_option_symbols(self):

        price = self.get_banknifty_price()

        atm = round(price/100)*100

        strikes = []

        for i in range(-10,11):

            strikes.append(atm + i*100)

        opt_df = self.instrument_df[
        (self.instrument_df["segment"]=="NFO-OPT") &
        (self.instrument_df["name"]=="BANKNIFTY")
        ]

        expiry = opt_df.sort_values("expiry").iloc[0]["expiry"]

        opt_df = opt_df[opt_df["expiry"]==expiry]

        symbols = []

        for s in strikes:

            ce = opt_df[
            (opt_df["strike"]==s) &
            (opt_df["instrument_type"]=="CE")
            ]

            pe = opt_df[
            (opt_df["strike"]==s) &
            (opt_df["instrument_type"]=="PE")
            ]

            if not ce.empty:
                symbols.append("NFO:"+ce.iloc[0]["tradingsymbol"])

            if not pe.empty:
                symbols.append("NFO:"+pe.iloc[0]["tradingsymbol"])

        return symbols

    def get_option_data(self):

        symbols = self.get_option_symbols()

        data = self.kite.quote(symbols)

        return data

    def detect_option_flow(self,option_data):

        bullish = 0
        bearish = 0

        for s in option_data:

            price = option_data[s]["last_price"]
            oi = option_data[s]["oi"]
            open_price = option_data[s]["ohlc"]["open"]

            change = price-open_price

            if change>0 and oi>0:

                bullish += 1

            if change<0 and oi>0:

                bearish += 1

        return bullish,bearish

    def detect_futures_flow(self,fut_data):

        signals = {}

        for s in fut_data:

            ltp = fut_data[s]["last_price"]
            open_price = fut_data[s]["ohlc"]["open"]
            oi = fut_data[s]["oi"]

            change = ltp-open_price

            if change>0 and oi>0:
                signals[s] = "LONG BUILDUP"

            elif change<0 and oi>0:
                signals[s] = "SHORT BUILDUP"

            elif change>0 and oi<=0:
                signals[s] = "SHORT COVERING"

            else:
                signals[s] = "LONG UNWINDING"

        return signals

    def final_bias(self):

        score,details = self.get_bank_strength()

        option_data = self.get_option_data()

        bullish,bearish = self.detect_option_flow(option_data)

        if score>30 and bullish>bearish:

            bias = "STRONG BULLISH"

        elif score<-30 and bearish>bullish:

            bias = "STRONG BEARISH"

        else:

            bias = "NEUTRAL"

        return bias,score,details
