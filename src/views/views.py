import logging
import pandas as pd
import requests

from app.core.config import read_user_setting
from app.services.adapters import normalize_transaction_df
from app.service.periods import parse_datetime_flexible, month_to_date_bounds, filter_transactions_by_period
from app.services.analytics import get_greeting, calc_cards_summary, calc_top_transactions
from app.services.external_api import fetch_currency_rates_rub_per_unity, calc_top_transactions

logger = logging.getLogger(__name__)

def (
    datetime_str: str,
    transaction_df: pd.DataFrame,
    *,
    mapping=None,
    setting_path: str="user_setting_json",
    session: requests.Session | None = None
) -> dict:
    dt = parse_datetime_flexible(datetime_str)

    df = normalize_transaction_df(transaction_df, mapping=mapping)

    start_dt, end_dt = month_to_date_bounds(dt)
    df_period = filter_transactions_by_period(df, start_dt, end_dt)

    settings = read_user_setting(settings_path)
    currencies = settings.get("user_currencies", [])
    stocks = settings.get("user_stocks", [])

    return {
        "greeting": get_greeting(dt),
        "cards": calc_cards_summary(df_period),
        "top_transactions": calc_top_transactions(df_period, top_n=5),
        "currency_rates": fetch_currency_rates_rub_per_unity(currencies, session=session),
        "stock_prices": fetch_stock_prices(stocks, session=session),
    }



