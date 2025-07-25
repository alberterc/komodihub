import streamlit as st
import pandas as pd

from app.data.stock_data import Stocks, Commodities
from app.analysis.correlation import get_correlation_commodity_based
from app.utils.data_loader import fetch_stock_data
from app.config import SPREADSHEET_NAME, STOCK_WORKSHEET_NAME, STOCK_JSON_PATH


def lag_description(lag):
    if lag < 0:
        return f"Stock prices moves later by {abs(lag)} days from the commodity price."
    elif lag < 0:
        return f"Stock prices moves sooner by {abs(lag)} days from the commodity price."
    else:
        return "Stock prices move the same as the commodity price movement."


# Page Setup
st.set_page_config(page_title="Stock-Commodity Correlation - Komodihub", layout="wide")

# Page Body
st.title("Stock-Commodity Correlation")
st.markdown("""
    __Correlation between stock and commodity price movements from 1-month of data.__
    - Stocks are shown based on the selected commodity.
    - Each column is sortable.
    - Percentages can be formatted to actual values.
    - The closer to 100% correlation, the better chances a stock price will move according to the selected commodity price.

    _Price data is retrieved from Yahoo Finance._
""")

left, right = st.columns([0.9, 0.1], vertical_alignment="bottom")

if Stocks and Commodities:
    with right:
        if st.button("Refresh Data"):
            st.cache_data.clear()
            fetch_stock_data(SPREADSHEET_NAME, STOCK_WORKSHEET_NAME, STOCK_JSON_PATH)
            st.rerun()

    with left:
        commodity_ticker = st.selectbox(
            "What commodity should be used?",
            list(Commodities.keys()),
            format_func=lambda c: c.value.name,
            index=None,
            placeholder="Select a commodity...",
        )

    if commodity_ticker:
        correlation_res = get_correlation_commodity_based(commodity_ticker)
        res = []
        for stock, corrs in correlation_res.items():
            pos_idx, pos_val = next(iter(corrs["Pos_Top"].items()))
            neg_idx, neg_val = next(iter(corrs["Neg_Top"].items()))

            res.append(
                {
                    "Stock": stock.name,
                    "Pos_Lag": pos_idx,
                    "Pos_Top_Corr": pos_val,
                    "Neg_Lag": neg_idx,
                    "Neg_Top_Corr": neg_val,
                }
            )

        df = pd.DataFrame(res)

        # Represent data values
        df["Pos_Lag"] = df["Pos_Lag"].apply(lag_description)
        df["Neg_Lag"] = df["Neg_Lag"].apply(lag_description)
        df["Neg_Top_Corr"] = df["Neg_Top_Corr"].apply(lambda corr: abs(corr))

        st.dataframe(
            df,
            column_config={
                "Pos_Lag": st.column_config.TextColumn(
                    "Positive Corr Delay",
                    help="How much delay does it take for the stock/commodity to move in the same direction?",
                ),
                "Pos_Top_Corr": st.column_config.NumberColumn(
                    "Positive Corr (%)",
                    help="The percentage of how close a stock price moves together with the associated commodity price.",
                    format="percent",
                ),
                "Neg_Lag": st.column_config.TextColumn(
                    "Negative Corr Delay",
                    help="How much delay does it take for the stock/commodity to move in the opposite direction?",
                ),
                "Neg_Top_Corr": st.column_config.NumberColumn(
                    "Negative Corr (%)",
                    help="The percentage of how close a stock price moves opposite with the associated commodity price.",
                    format="percent",
                ),
            },
            hide_index=True,
        )
