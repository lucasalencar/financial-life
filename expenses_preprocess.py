import glob
import pandas as pd


def read_all_csvs(files_path, filename_pattern):
    """Reads all csvs given a filname pattern and
    joins all of them into a single DataFrame"""
    all_files = glob.glob(files_path + filename_pattern)
    all_dfs = [pd.read_csv(filename) for filename in all_files]
    return pd.concat(all_dfs, ignore_index=True)


def nubank_preprocess(expenses, category_conversion_hash):
    # Replace categories to the official ones
    expenses['category'] = expenses['category'].replace(category_conversion_hash)
    # Update amount to reflect expenses as negative value
    expenses['amount'] = expenses['amount'] * -1
    # Parse date
    expenses['date'] = pd.to_datetime(expenses.date, format="%Y-%m-%d")
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    return expenses


def splitwise_preprocess(expenses, category_conversion_hash):
    # Replace categories to the official ones
    expenses['Categoria'] = expenses['Categoria'].replace(category_conversion_hash)
    # Parse date
    expenses['Data'] = pd.to_datetime(expenses['Data'], format="%Y-%m-%d")
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['Categoria'] != 'Pagamento']
    # Remove Saldo total expense
    expenses = expenses.loc[expenses['Descrição'] != 'Saldo total']
    return expenses


def splitwise_focused_on(person_name, expenses, convert_col_names):
    expenses = expenses.rename(index=str, columns={**convert_col_names, **{person_name: 'amount'}})
    return expenses[['date', 'title', 'category', 'amount']]


def other_accounts_preprocess(expenses):
    # Parse date
    expenses['date'] = pd.to_datetime(expenses['date'], format="%Y-%m-%d")
    # Update amount to reflect expenses as negative value
    expenses['amount'] = expenses['amount'] * -1
    # Select only necessary columns
    return expenses[['date', 'title', 'category', 'amount']]


def export_to_sheets(expenses, filepath):
    expenses_to_export = expenses.copy()
    expenses_to_export['date'] = expenses['date'].dt.strftime("%m/%Y")
    expenses_to_export.sort_values(by=['date'], inplace=True)
    expenses_to_export.to_csv(filepath + '/expenses.csv', index=False)


def export_raw_expenses(expenses, filepath):
    expenses_to_export = expenses.copy()
    expenses_to_export.sort_values(by=['date'], inplace=True)
    expenses_to_export.to_csv(filepath + '/raw_expenses.csv', index=False)
