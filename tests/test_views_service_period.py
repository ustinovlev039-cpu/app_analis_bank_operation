import pytest
import pandas as pd
from datetime import datetime

from src.views.service.period import parse_datetime_flexible, month_to_date_bounds, filter_transactions_by_period

def test_parse_ok_date():
    assert parse_datetime_flexible("2021-12-20") == datetime(2021, 12, 20)
    assert parse_datetime_flexible("2021-12-20 10:11:12") == datetime(2021, 12, 20, 10, 11, 12)
    assert parse_datetime_flexible("2021-12-20T10:11:12") == datetime(2021, 12, 20, 10, 11, 12)

def test_parse_bad():
    with pytest.raises(ValueError):
        parse_datetime_flexible("abc")


def test_month_to_date_bounds():
    dt = datetime(2021, 12, 20, 10, 0, 0)
    start, end = month_to_date_bounds(dt)

    assert start == datetime(2021, 12, 1, 0, 0, 0,0)
    assert end == datetime(2021, 12, 20, 23, 59, 59, 0)


def test_moth_to_date_erro():
    with pytest.raises(TypeError):
        month_to_date_bounds("123142")


def test_filter_transactions_by_period():
    df_good = pd.DataFrame({"date": ["2021-12-01", "2021-12-20 23:59:59", "2021-12-21"], "x": [1, 2, 3]})

    df_bad = pd.DataFrame({"date": ["abc", "2021-12-10"], "x": [1, 2]})

    df_empty = pd.DataFrame(columns=["date", "x"])

    start_df = datetime(2021, 12, 1, 0, 0, 0, 0)
    end_df = datetime(2021, 12, 20, 23, 59, 59, 0)

    start_bad_df = datetime(2021, 12, 1)
    end_bad_df = datetime(2021, 12, 31, 23, 59, 59)

    res_good = filter_transactions_by_period(df_good, start_df, end_df)

    res_bad = filter_transactions_by_period(df_bad, start_bad_df, end_bad_df)

    res_empty = filter_transactions_by_period(df_empty, start_bad_df, end_bad_df)
    assert res_good["x"].tolist() == [1, 2]
    assert res_bad["x"].tolist() == [2]
    assert res_empty.empty
    assert len(res_empty.columns) == ["date", "x"]

def test_filter_transactions_by_period_error():
    df = pd.DataFrame({"amount": [1, 2, 3]})
    with pytest.raises(KeyError):
        filter_transactions_by_period(df, datetime(2021, 1, 1), datetime(2021, 1, 2))







