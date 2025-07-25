import yfinance as yf

from app.config import DEFAULT_PERIOD
from app.utils.string import get_stock_ticker


def get_stock_history(stock, period=DEFAULT_PERIOD):
    stock_data = yf.Ticker(get_stock_ticker(stock.name))
    hist = stock_data.history(period=period, repair=True)
    hist = hist[["Close"]]
    hist.index = hist.index.tz_localize(None)
    result = hist.rename(columns={"Close": stock})
    return result
