#!/usr/bin/env python3

from datetime import datetime
import pandas as pd
import pytest

from ..test_helpers import assert_dataframe_equals
from src import aggregate

@pytest.fixture
def df_example():
    return pd.DataFrame(
        [
            [datetime(2022, 1, 1), 'Title 1', 'Renda Fixa', 100],
            [datetime(2022, 2, 1), 'Title 1', 'Renda Variável', 100],
            [datetime(2022, 1, 1), 'Title 2', 'Renda Fixa', 500],
            [datetime(2022, 2, 1), 'Title 2', 'Renda Variável', 300]
        ],
        columns=['date', 'title', 'category', 'amount']
    )

# total_amount_by

def test_total_amount_by_title(df_example):
    result = aggregate.amount.total_amount_by('title', df_example)

    expected = pd.DataFrame(
        [
            ['Title 1', 200],
            ['Title 2', 800]
        ],
        columns=['title', 'amount']
    ).set_index('title')

    pd.testing.assert_frame_equal(result, expected)

def test_total_amount_by_category(df_example):
    result = aggregate.amount.total_amount_by('category', df_example)

    expected = pd.DataFrame(
        [
            ['Renda Fixa', 600],
            ['Renda Variável', 400]
        ],
        columns=['category', 'amount']
    ).set_index('category')

    pd.testing.assert_frame_equal(result, expected)

def test_total_amount_by_date(df_example):
    result = aggregate.amount.total_amount_by('date', df_example)

    expected = pd.DataFrame(
        [
            [datetime(2022, 1, 1), 600],
            [datetime(2022, 2, 1), 400]
        ],
        columns=['date', 'amount']
    ).set_index('date')

    pd.testing.assert_frame_equal(result, expected)
