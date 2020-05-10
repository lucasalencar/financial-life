"""
All functions necessary to load and preprocess incomes
"""
import pandas as pd
from load import read
from load import easynvest


def preprocess(incomes):
    # Convert categories to lower case
    incomes['category'] = incomes['category'].apply(lambda x: x.lower())
    # Parse date to datetime format
    incomes['date'] = pd.to_datetime(incomes['date'], format="%Y-%m-%d")
    # Convert amount to float
    if incomes.amount.dtype == object:
        incomes['amount'] = incomes['amount'].apply(lambda x: float(x.replace(',', '')))
    return incomes


def load(file_pattern=None, incomes_file_pattern=None, data_path=None, **configs):
    pattern = file_pattern or incomes_file_pattern
    content = [
        preprocess(read.read_all_csv_found(data_path, pattern)),
        easynvest.load(data_path),
    ]

    return pd.concat(content, sort=False)
