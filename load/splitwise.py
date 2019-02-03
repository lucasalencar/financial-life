"""
All Splitwise functions necessary to load and preprocess its data
"""
import pandas as pd
from load import read


SPLITWISE_FILE_REGEX = './data/(\d+)-mozi-e-eu_([0-9\-]*).*\.csv'


def parse_files(all_files):
    import re
    pattern = re.compile(SPLITWISE_FILE_REGEX)

    files = []

    for file in all_files:
        year, export_date = pattern.match(file).group(1, 2)
        files.append({'year': year, 'exported_at': export_date, 'filename': file})

    return pd.DataFrame(files, columns=['year', 'exported_at', 'filename'])


def most_recent_exported_files(filepath, file_pattern):
    files = parse_files(read.list_all_files_for(filepath, file_pattern))
    selected_files = files.groupby('year').exported_at.max().reset_index()
    selected_files = files[(files.year.isin(selected_files.year)) &
                           (files.exported_at.isin(selected_files.exported_at))]
    return list(selected_files.filename)


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
    # Because default preprocess converts values to negative,
    # return amount to original values
    expenses['amount'] = expenses['amount'] * -1
    return expenses[['date', 'title', 'category', 'amount']]


def load(file_pattern=None, data_path=None, person_who_pays=None, **configs):
    files = most_recent_exported_files(data_path, file_pattern)
    expenses = read.read_all_csv_for(files)
    return preprocess(expenses, person_who_pays)
