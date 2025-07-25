import streamlit as st
import gspread
import json


def save_to_json(data, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@st.cache_resource
def get_data_sheet(sheet_name):
    client = gspread.service_account_from_dict(st.secrets.db_credentials)
    result = client.open(sheet_name)
    return result


@st.cache_data(ttl=300)
def fetch_stock_data(sheet_name, worksheet_title, json_path):
    sheet = get_data_sheet(sheet_name)
    worksheet = sheet.worksheet(worksheet_title)
    raw_data = worksheet.get_all_values()

    table_data = [row for row in raw_data if any(cell.strip() for cell in row)]
    headers = table_data[0]
    rows = table_data[1:]
    result = [dict(zip(headers, row)) for row in rows]

    save_to_json(result, json_path)

    return result
