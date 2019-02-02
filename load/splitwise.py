"""
All Splitwise functions necessary to load and preprocess its data
"""
from load import read


# Splitwise column names to convert
COLUMN_NAMES = {
    'Data': 'date',
    'Descrição': 'title',
    'Categoria': 'category',
}


def preprocess(expenses, person_name):
    # Convert col names to default ones
    expenses = expenses.rename(index=str, columns={**COLUMN_NAMES, **{person_name: 'amount'}})
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    # Remove Saldo total expense
    expenses = expenses.loc[expenses['title'] != 'Saldo total']
    # Because default preprocess converts values to negative, return amount to original values
    expenses['amount'] = expenses['amount'] * -1
    return expenses[['date', 'title', 'category', 'amount']]


def load(file_pattern=None, data_path=None, person_who_pays=None, **configs):
    file_content = read.read_first_file_found(data_path, file_pattern)
    return preprocess(file_content, person_who_pays)
