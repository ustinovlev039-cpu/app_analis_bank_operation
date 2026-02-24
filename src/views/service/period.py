from datetime import datetime
import pandas as pd

def parse_datetime_flexible(value: str) -> datetime:
    """ Выводит дату и время в формате "YYYY-MM-DD" и "YYYY-MM-DD HH:MM:SS" """
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Строка должна быть не пустой")

    s = value.strip()

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass

    dt = pd.to_datetime(s, errors="coerce")
    if pd.isna(dt):
        raise ValueError(f"Неверный формат даты: {value}")
    return dt.to_pydatetime()

def month_to_date_bounds(dt: datetime):
    """ Возвращает границы периода: с начала месяца до текущей даты включительно. """
    if not isinstance(dt, datetime):
        raise TypeError("dt должен быть datetime")

    start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = dt.replace(hour=23, minute=59, second=59, microsecond=0)
    return start, end


def filter_transactions_by_period(df: pd.DataFrame, start_dt: datetime, end_dt: datetime):
    """ Возвращает те строки, которые находятся в диапазоне start_dt <= data <= end_dt """
    if df is None or df.empty:
        return pd.DataFrame(columns=df.columns if df is not None else None)

    if "date" not in df.columns:
        raise KeyError("Не пойдет ошибка, ошибка, ошибка!!!, ну и нет колонки 'data'")

    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")

    mask = (out["date"] >= start_dt) & (out["date"] <= end_dt)
    return out.loc[mask].reset_index(drop=True)


