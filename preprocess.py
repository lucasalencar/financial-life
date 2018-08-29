import glob
import os
import pandas as pd


def read_all_csvs(files_path, filename_pattern):
    """Reads all csvs given a filname pattern and
    joins all of them into a single DataFrame"""
    full_pattern = os.path.join(files_path, filename_pattern)
    all_files = glob.glob(full_pattern)
    all_dfs = [pd.read_csv(filename) for filename in all_files]
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        print("WARNING: No files found with pattern %s" % full_pattern)
        return None


def read_first_file_found(filepath, file_pattern):
    """Read content of the first file found given a regex pattern"""
    full_pattern = os.path.join(filepath, file_pattern)
    found_files = glob.glob(full_pattern)
    if found_files:
        return pd.read_csv(found_files[0])
    else:
        print("WARNING: No files found with pattern %s" % full_pattern)
        return None


def incomes_preprocess(incomes):
    # Convert categories to lower case
    incomes['category'] = incomes['category'].apply(lambda x: x.lower())
    # Parse date to datetime format
    incomes['date'] = pd.to_datetime(incomes['date'], format="%Y-%m-%d")
    # Convert amount to float
    if incomes.amount.dtype != float:
        incomes['amount'] = incomes['amount'].apply(lambda x: float(x.replace(',', '')))
    return incomes


def expenses_preprocess(expenses, category_conversion_hash):
    # Replace categories to the official ones and convert to lower case
    expenses['category'] = expenses['category']\
        .replace(category_conversion_hash)\
        .apply(lambda x: x.lower())
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


# Splitwise column names to convert
SPLITWISE_COLUMN_NAMES = {
    'Data': 'date',
    'Descrição': 'title',
    'Categoria': 'category',
}


def splitwise_preprocess(expenses, person_name):
    # Convert col names to default ones
    expenses = expenses.rename(index=str, columns={**SPLITWISE_COLUMN_NAMES, **{person_name: 'amount'}})
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


# URL to fetch data from Central Bank
CENTRAL_BANK_TIMESERIES_URL = "http://api.bcb.gov.br/dados/serie/bcdata.sgs.%s/dados?formato=csv"

# IDs to series from Central Bank (BC) from Brazil
BC_IPCA_BY_MONTH_ID = 433
BC_SELIC_BY_DAY_ID = 11
BC_SELIC_ACCUM_MONTH_ID = 4390
BC_SELIC_BY_MONTH_ACCUM_YEAR_ID = 4189
BC_CDI_BY_DAY_ID = 12
BC_CDI_BY_DAY_ACCUM_MONTH_ID = 4389

# Where to find which is the timeseries ID to insert in thr BC URL
# https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries

def read_central_bank_data(timeseries_id, value_column_name):
    """Read Brazil Central Bank timeseries for multiple indexes (IPCA, SELIC, CDI)
    given the series ID"""
    timeseries_url = CENTRAL_BANK_TIMESERIES_URL % timeseries_id
    timeseries = pd.read_csv(timeseries_url, sep=";")
    timeseries['data'] = pd.to_datetime(timeseries['data'], format="%d/%m/%Y")
    timeseries['valor'] = timeseries['valor'].apply(lambda x: float(x.replace(',', '.')))
    timeseries = timeseries.rename(index=str, columns={'data': 'date', 'valor': value_column_name})
    return timeseries


def central_bank_metric_for_month(timeseries, base_date):
    """Returns the metric given the year and month on the base_date parameter.
    Specific for time series fetched from Central Bank website."""
    return timeseries[timeseries.date == base_date.strftime("%Y-%m")].iloc[0,1]
