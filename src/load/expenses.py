from . import read
from . import data_processing
from . import nubank
from . import splitwise
from . import investments
from . import manual
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
