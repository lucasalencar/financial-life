"""
All Nubank functions necessary to load and preprocess its data
"""
from load import read


def preprocess(expenses):
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    return expenses[['date', 'title', 'category', 'amount']]


def load(file_pattern=None, data_path=None, **configs):
    return preprocess(read.read_all_csvs(data_path, file_pattern))
