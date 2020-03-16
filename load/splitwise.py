"""
All Splitwise functions necessary to load and preprocess its data
"""
import pandas as pd
import re
from load import read
from load import data_processing


def parse_file_names(all_files, parse_regex):
    pattern = re.compile(parse_regex)

    files = []

    for file in all_files:
        export_date = pattern.match(file).group(1)
        files.append({'exported_at': export_date, 'filename': file})

    return pd.DataFrame(files, columns=['exported_at', 'filename'])


def list_exported_files(filepath, file_prefix):
    file_pattern = file_prefix + '*_export.csv'
    return read.list_all_files_for(filepath, file_pattern)


def most_recently_exported(filepath, file_prefix):
    all_files = list_exported_files(filepath, file_prefix)
    parse_regex = filepath + '/' + file_prefix + '_([0-9\-]+)_export.csv'
    parsed_files = parse_file_names(all_files, parse_regex)
    return parsed_files.max().filename

def all_recently_exported_files(filepath, groups):
    return list(map(lambda group: most_recently_exported(filepath, group), groups))



# Splitwise column names to convert
COLUMN_NAMES = {
    'Data': 'date',
    'Descrição': 'title',
    'Categoria': 'category',
}


def preprocess(expenses, person_name, category_conversion_hash):
    # Convert col names to default ones
    expenses = expenses.rename(index=str, columns={**COLUMN_NAMES, **{person_name: 'amount'}})
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    # Remove Saldo total expense
    expenses = expenses.loc[expenses['title'] != 'Saldo total']
    # Remove Saldo total expense
    expenses = expenses.loc[expenses['title'] != 'Quitar todos os saldos']

    expenses['category'] = data_processing.convert_categories(expenses, category_conversion_hash)
    return expenses[['date', 'title', 'category', 'amount']]


def load(splitwise_groups=None,
         data_path=None,
         person_who_pays=None,
         category_conversion_table=None,
         **configs):
    files = all_recently_exported_files(data_path, splitwise_groups)
    expenses = read.read_all_csv_for(files)
    return preprocess(expenses, person_who_pays, category_conversion_table)
