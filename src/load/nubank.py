"""
All Nubank functions necessary to load and preprocess its data
"""
from . import read
from . import data_processing


def fix_empty_category(category):
    if isinstance(category, str):
        return category
    return 'Outros'


def preprocess(expenses, category_conversion_table):
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    expenses = expenses.loc[expenses['title'] != 'Pagamento recebido']

    print('Warning: replacing nubank empty category to Outros')
    expenses['category'] = expenses['category'].apply(fix_empty_category)
    expenses['category'] = data_processing\
        .convert_categories(expenses, category_conversion_table)
    # Update amount to reflect expenses as negative value
    expenses['amount'] = expenses['amount'] * -1
    return expenses[['date', 'title', 'category', 'amount']]


def load(file_pattern=None,
         data_path=None,
         category_conversion_table=None,
         **configs):
    expenses = read.read_all_csv_found(data_path, file_pattern)
    return preprocess(expenses, category_conversion_table)
