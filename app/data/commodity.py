import yfinance as yf

from app.config import DEFAULT_PERIOD


def get_commodity_history(commodity, period=DEFAULT_PERIOD):
    commodity_data = yf.Ticker(commodity.value.ticker)
    hist = commodity_data.history(period=period, repair=True)
    hist = hist[["Close"]]
    hist.index = hist.index.tz_localize(None)
    result = hist.rename(columns={"Close": commodity})
    return result
