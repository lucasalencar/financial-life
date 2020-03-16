from load import read
from load import data_processing
from load import nubank
from load import splitwise
from load import incomes
from load import manual
import pandas as pd


def preprocess(expenses, category_conversion_table):
    # Replace categories to the official ones and convert to lower case
    expenses['category'] = data_processing\
        .convert_categories(expenses, category_conversion_table)
    # Parse date
    expenses['date'] = pd.to_datetime(expenses['date'], format="%Y-%m-%d")
    # Convert amount to float
    if expenses.amount.dtype != float:
        expenses['amount'] = expenses['amount'].apply(lambda x: float(x.replace(',', '')))
    # Update amount to reflect expenses as negative value
    expenses['amount'] = expenses['amount'] * -1
    # Select only necessary columns
    return expenses[['date', 'title', 'category', 'amount']]


def load(category_conversion_table=None, **configs):
    content = [
        nubank.load(file_pattern=configs['nubank_file_pattern'],
                    category_conversion_table=configs.get('nubank_category_table', {}),
                    **configs),

        splitwise.load(category_conversion_table=configs.get('splitwise_category_table', {}),
                       **configs),

        manual.load(file_pattern=configs['manual_file_pattern'],
                    **configs)
    ]
    return preprocess(pd.concat(content, sort=False), category_conversion_table)
