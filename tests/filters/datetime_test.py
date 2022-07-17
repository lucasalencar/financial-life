#!/usr/bin/env python3

from datetime import datetime, date
from IPython.display import display
import pandas as pd
import numpy as np
import pytest

from src import filters

@pytest.fixture
def df_with_multiple_dates():
   return pd.DataFrame(
       [
           [datetime(2022, 1, 1), 100],
           [datetime(2022, 1, 15), 200],
           [datetime(2022, 2, 1), 100],
           [datetime(2022, 2, 20), 300],
           [datetime(2022, 2, 28), 300],
           [datetime(2022, 3, 12), 100],
           [datetime(2022, 3, 30), 300]
       ],
       columns=['date', 'amount']
   )


def assert_filters_successfully(result, expected):
    assert np.array_equal(result.values, expected.values)
    assert np.array_equal(result.columns, expected.columns)

# by_monthly_period

def test_by_monthly_period_returns_whole_month(df_with_multiple_dates):
    start_date = date(2022, 1, 10)
    end_date = date(2022, 2, 25)
    expected = pd.DataFrame(
        [
            [datetime(2022, 1, 1), 100],
            [datetime(2022, 1, 15), 200],
            [datetime(2022, 2, 1), 100],
            [datetime(2022, 2, 20), 300],
            [datetime(2022, 2, 28), 300],
        ],
        columns=['date', 'amount']
    )
    result = filters.datetime.by_monthly_period(df_with_multiple_dates, start_date, end_date)
    assert_filters_successfully(result, expected)


def test_by_monthly_period_same_start_and_end(df_with_multiple_dates):
    base_date = date(2022, 2, 25)
    expected = pd.DataFrame(
        [
            [datetime(2022, 2, 1), 100],
            [datetime(2022, 2, 20), 300],
            [datetime(2022, 2, 28), 300],
        ],
        columns=['date', 'amount']
    )
    result = filters.datetime.by_monthly_period(df_with_multiple_dates, base_date, base_date)
    assert_filters_successfully(result, expected)


def test_by_monthly_period_dates_on_edges(df_with_multiple_dates):
    start_date = date(2022, 1, 1)
    end_date = date(2022, 2, 28)
    expected = pd.DataFrame(
        [
            [datetime(2022, 1, 1), 100],
            [datetime(2022, 1, 15), 200],
            [datetime(2022, 2, 1), 100],
            [datetime(2022, 2, 20), 300],
            [datetime(2022, 2, 28), 300],
        ],
        columns=['date', 'amount']
    )
    result = filters.datetime.by_monthly_period(df_with_multiple_dates, start_date, end_date)
    assert_filters_successfully(result, expected)
