"""
All Nubank functions necessary to load and preprocess its data
"""
from load import read
from load import data_processing


def fix_empty_category(category):
    if isinstance(category, str):
        return category
    print('Warning: nubank empty category changed to Outros')
    return 'Outros'


def preprocess(expenses, category_conversion_table):
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    expenses = expenses.loc[expenses['title'] != 'Pagamento recebido']
    expenses['category'] = expenses['category'].apply(fix_empty_category)
    expenses['category'] = data_processing\
        .convert_categories(expenses, category_conversion_table)
    return expenses[['date', 'title', 'category', 'amount']]


def load(file_pattern=None,
         data_path=None,
         category_conversion_table=None,
         **configs):
    expenses = read.read_all_csv_found(data_path, file_pattern)
    return preprocess(expenses, category_conversion_table)
