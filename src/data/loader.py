import datetime as dt
from functools import partial, reduce
from typing import Callable

import babel.dates
import i18n
import pandas as pd

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    # This seems kind of hideous but can't find another way to convert to abbreviated month names.
    df[DataSchema.MONTH] = list(map(lambda x: x.strftime("%b"), df[DataSchema.DATE].dt.to_pydatetime()))
    return df


def create_category(df: pd.DataFrame, category: dict) -> pd.DataFrame:
    df[DataSchema.CATEGORY] = df[DataSchema.CATEGORY].apply(lambda s: category[s])
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_transaction_data(path: str, category: dict) -> pd.DataFrame:
    # load the data from the CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str,
            DataSchema.DATE: str,
        },
        parse_dates=[DataSchema.DATE],
    )
    preprocessor = compose(
        create_year_column,
        create_month_column,
        partial(create_category, category=category),
    )
    return preprocessor(data)
