import pandas as pd

from app.data.stock_data import Commodities
from app.data.stock import get_stock_history
from app.data.commodity import get_commodity_history


def get_correlation(stock_ticker, commodity_ticker, stock_df=None, commodity_df=None):
    corrs = {}
    max_lag = -5

    if stock_df is None:
        stock_df = get_stock_history(stock_ticker)
    if commodity_df is None:
        commodity_df = get_commodity_history(commodity_ticker)

    stock_pct_change_df = stock_df.pct_change(periods=1).dropna() * 100
    commodity_pct_change_df = commodity_df.pct_change(periods=1).dropna() * 100

    combined_df = commodity_pct_change_df.join(stock_pct_change_df, how="inner")

    if combined_df.empty:
        return None

    for lag in range(max_lag, 1):
        corr = combined_df[commodity_ticker].corr(
            combined_df[stock_ticker].shift(lag), method="pearson"
        )
        corrs[lag] = corr

    corr_series = pd.Series(corrs)
    result = {
        "Pos_Top": corr_series[corr_series > 0].nlargest(1).to_dict(),
        "Neg_Top": corr_series[corr_series < 0].nsmallest(1).to_dict(),
    }

    return (
        result,
        combined_df,
        stock_df,
        stock_pct_change_df,
        commodity_df,
        commodity_pct_change_df,
    )


def get_correlation_commodity_based(commodity_ticker):
    result = {}
    commodity_df = get_commodity_history(commodity_ticker)
    for stock_ticker in Commodities[commodity_ticker]:
        corrs, _, _, _, _, _ = get_correlation(
            stock_ticker=stock_ticker,
            commodity_ticker=commodity_ticker,
            commodity_df=commodity_df,
        )
        result[stock_ticker] = corrs

    return result
