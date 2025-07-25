import json

from dataclasses import dataclass
from collections import defaultdict
from enum import Enum
from pathlib import Path
from app.data.commodity_data import Commodity
from app.utils.data_loader import fetch_stock_data
from app.config import SPREADSHEET_NAME, STOCK_WORKSHEET_NAME, STOCK_JSON_PATH


@dataclass
class StockInfo:
    name: str
    commodities: list[str]
    alt_name: str


def load_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_json_exists():
    if not Path(STOCK_JSON_PATH).exists():
        fetch_stock_data(SPREADSHEET_NAME, STOCK_WORKSHEET_NAME, STOCK_JSON_PATH)


def build_stock_data(data):
    dict = {}
    for row in data:
        ticker = row.get("Ticker")
        if not ticker:
            continue

        commodity_str = row.get("Commodity Type", "")
        commodities = [
            Commodity.from_name(c.strip())
            for c in commodity_str.split(",")
            if c.strip()
        ]
        dict[ticker] = StockInfo(
            name=row.get("Name", ""),
            commodities=commodities,
            alt_name=row.get("Alternative Name", ""),
        )

    return Enum("Stocks", dict)


def build_commodity_data(stock_data):
    index = defaultdict(list)
    for stock in stock_data:
        for commodity in stock.value.commodities:
            index[commodity].append(stock)

    return dict(index)


# run on import
is_json_exists()
data = load_from_json(STOCK_JSON_PATH)
Stocks = build_stock_data(data)
Commodities = build_commodity_data(Stocks)
