from load import read
from load import nubank
from load import splitwise
from load import incomes
from load import manual
import pandas as pd


def expenses_preprocess(expenses, category_conversion_hash):
    # Replace categories to the official ones and convert to lower case
    expenses['category'] = expenses['category']\
        .replace(category_conversion_hash)\
        .apply(lambda x: x.lower())
    # Parse date
    expenses['date'] = pd.to_datetime(expenses['date'], format="%Y-%m-%d")
    # Convert amount to float
    if expenses.amount.dtype != float:
        expenses['amount'] = expenses['amount'].apply(lambda x: float(x.replace(',', '')))
    # Update amount to reflect expenses as negative value
    expenses['amount'] = expenses['amount'] * -1
    # Select only necessary columns
    return expenses[['date', 'title', 'category', 'amount']]


def preprocess(expenses_input_files, category_conversion_table=None, **configs):
    return expenses_preprocess(pd.concat(expenses_input_files, sort=False), category_conversion_table)


def load(**configs):
    content = [
        nubank.load(file_pattern=configs['nubank_file_pattern'], **configs),
        splitwise.load(file_pattern=configs['splitwise_file_pattern'], **configs),
        manual.load(file_pattern=configs['manual_file_pattern'], **configs)
    ]
    return preprocess(content, **configs)
