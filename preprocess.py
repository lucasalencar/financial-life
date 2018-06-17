import glob
import os
import pandas as pd


def read_all_csvs(files_path, filename_pattern):
    """Reads all csvs given a filname pattern and
    joins all of them into a single DataFrame"""
    full_pattern = os.path.join(files_path, filename_pattern)
    all_files = glob.glob(full_pattern)
    all_dfs = [pd.read_csv(filename) for filename in all_files]
    if not all_dfs:
        raise Exception("No files found with pattern %s" % full_pattern)
    return pd.concat(all_dfs, ignore_index=True)


def read_first_file_found(filepath, file_pattern):
    """Read content of the first file found given a regex pattern"""
    full_pattern = os.path.join(filepath, file_pattern)
    found_files = glob.glob(full_pattern)
    if not found_files:
        raise Exception("No files found with pattern %s" % full_pattern)
    return pd.read_csv(found_files[0])


def incomes_preprocess(incomes):
    # Parse date to datetime format
    incomes['date'] = pd.to_datetime(incomes['date'], format="%Y-%m-%d")
    # Convert amount to float
    if incomes.amount.dtype != float:
        incomes['amount'] = incomes['amount'].apply(lambda x: float(x.replace(',', '')))
    return incomes[['date', 'title', 'category', 'amount']]


def expenses_preprocess(expenses, category_conversion_hash):
    # Replace categories to the official ones
    expenses['category'] = expenses['category'].replace(category_conversion_hash)
    # Parse date
    expenses['date'] = pd.to_datetime(expenses['date'], format="%Y-%m-%d")
    # Convert amount to float
    if expenses.amount.dtype != float:
        expenses['amount'] = expenses['amount'].apply(lambda x: float(x.replace(',', '')))
    # Update amount to reflect expenses as negative value
    expenses['amount'] = expenses['amount'] * -1
    # Select only necessary columns
    return expenses[['date', 'title', 'category', 'amount']]


def nubank_preprocess(expenses):
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    return expenses[['date', 'title', 'category', 'amount']]


def splitwise_preprocess(expenses, person_name, convert_col_names):
    # Convert col names to default ones
    expenses = expenses.rename(index=str, columns={**convert_col_names, **{person_name: 'amount'}})
    # Remove cagegory Pagamento
    expenses = expenses.loc[expenses['category'] != 'Pagamento']
    # Remove Saldo total expense
    expenses = expenses.loc[expenses['title'] != 'Saldo total']
    # Because default preprocess converts values to negative, return amount to original values
    expenses['amount'] = expenses['amount'] * -1
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
