from datetime import timedelta
import pandas as pd
import re

from . import read
from . import easynvest_fixed_term
from . import easynvest_variable

from .. import filters
from .. import record_summary as rs
from .. import date_helpers as dth


FILENAME_PATTERN = '/Exportar_custodia_([0-9\-]+).csv'


def list_exported_files(filepath):
    file_pattern = 'Exportar_custodia_*.csv'
    return read.list_all_files_for(filepath, file_pattern)


def parse_file_names(all_files, filepath):
    pattern = re.compile(filepath + FILENAME_PATTERN)

    files = []

    for file in all_files:
        exported_at = pattern.match(file).group(1)
        files.append({'exported_at': exported_at,
                      'filename': file})

    return pd.DataFrame(files, columns=['exported_at', 'filename'])


def earliest_each_month(parsed_files):
    months = rs.available_months(parsed_files)
    earliest = []

    for month in months:
        first_day, last_day = dth.month_day_range(rs.month_to_date(month))
        files_for_month = parsed_files[(parsed_files.date >= pd.Timestamp(first_day)) &
                                       (parsed_files.date <= pd.Timestamp(last_day))]
        earliest.append(files_for_month.min().filename)

    return earliest


def earliest_by_month_exported(filepath):
    all_files = list_exported_files(filepath)
    parsed_files = parse_file_names(all_files, filepath)
    parsed_files['date'] = pd.to_datetime(parsed_files['exported_at'],
                                          format="%Y-%m-%d")
    return earliest_each_month(parsed_files)

# Preprocess functions


def date_from_filename(loaded, filepath):
    """Add date that data was collected based on the filename"""
    pattern = re.compile(filepath + FILENAME_PATTERN)
    loaded['date'] = loaded.filename.map(lambda filename:
                                         pattern.match(filename).group(1))
    return loaded


def move_date_end_previous_month(easynvest):
    easynvest['date'] = pd.to_datetime(easynvest['date'], format="%Y-%m-%d")
    easynvest['date'] = easynvest.date.map(lambda date: date.replace(day=1) - timedelta(days=1))
    return easynvest


def rename_columns(loaded):
    """Rename columns to more programmable ones."""
    column_names = {
        'TIPO DE INVESTIMENTO': 'type',
        'DESCRIÇÃO': 'description',
        'VENCIMENTO': 'maturity date',
        'TAXA NEGOCIADA': 'index',
        'QUANTIDADE': 'quantity',
        'VALOR APLICADO': 'application',
        'VALOR BRUTO': 'gross amount',
        'VALOR LÍQUIDO': 'net amount',
    }
    return loaded.rename(index=str, columns=column_names)


def preprocess(loaded, filepath):
    """Preprocess easynvest exported files"""
    loaded = rename_columns(loaded)
    loaded = date_from_filename(loaded, filepath)
    loaded = move_date_end_previous_month(loaded)
    content = [
        easynvest_fixed_term.preprocess(loaded),
        easynvest_variable.preprocess(loaded),
    ]
    return pd.concat(content, sort=False)


def normalize_amount(data, column):
    data['amount'] = data[column]\
        .dropna()\
        .map(lambda amount:
             amount
             .replace('R$', '')
             .replace('.', '')
             .replace(',', '.')).astype(float)
    return data


def preprocess_invested(funds):
    funds = normalize_amount(funds, 'gross amount')
    funds = rs.total_amount_by(['date', 'title', 'type', 'account', 'goal'], funds).reset_index()
    funds['category'] = 'valor aplicado'
    return funds


APPLICATIONS_GROUPBY = ['title', 'type', 'account', 'goal']


def compute_applications(data, base_date):
    previous_month_data = filters.datetime.records_for_month(data,
                                               dth.months_ago(base_date, 1))
    current_month_data = filters.datetime.records_for_month(data, base_date)
    difference = rs.total_amount_by(APPLICATIONS_GROUPBY,
                                    current_month_data) - rs.total_amount_by(APPLICATIONS_GROUPBY,
                                                                             previous_month_data)
    return difference.amount


def preprocess_applications(funds):
    funds = normalize_amount(funds, 'application')
    funds = rs.total_amount_by(['date', 'title', 'type', 'account', 'goal'], funds).reset_index()
    funds = rs.describe_over_time(funds, compute_applications)\
        .transpose()\
        .reset_index()\
        .melt(id_vars=APPLICATIONS_GROUPBY,
              var_name='date',
              value_name='amount')

    # Fix date to be in the beginning of month
    funds['date'] = pd.to_datetime(funds.date
                                   .map(lambda d:
                                        dth.beginning_of_month(rs.month_to_date(d))))
    funds['category'] = 'aplicação'

    # Remove first month because there is no record for its previous month
    funds = funds[funds.date > funds.date.min()]
    return funds


def compute_liquidations(date, title, invested):
    begin, end = dth.month_day_range(dth.months_ago(date, 1))

    amount = invested[(invested.date >= pd.Timestamp(begin)) &
                      (invested.date <= pd.Timestamp(end)) &
                      (invested.title == title)].amount
    if amount.empty:
        return 0
    else:
        return amount.iloc[0] * -1


def preprocess_liquidations(funds):
    applications = filters.investment.applications(funds)
    invested = filters.investment.invested(funds)
    liquidations = applications[applications.amount.isna()].copy()
    liquidations['amount'] = liquidations.apply(lambda row: compute_liquidations(row.date, row.title, invested), axis=1)
    return liquidations


def load(data_path=None):
    """Load and preprocess easynvest exported files"""
    files = earliest_by_month_exported(data_path)
    easynvest = read.read_all_csv_for(files,
                                      sep=';',
                                      encoding='latin',
                                      header=1)

    easynvest = preprocess(easynvest, data_path)

    content = [
        preprocess_invested(easynvest),
        preprocess_applications(easynvest),
    ]
    funds = pd.concat(content, sort=False)
    funds = pd.concat([funds, preprocess_liquidations(funds)], sort=False)
    return funds.dropna()



def raw_load(data_path=None):
    """Load and preprocess easynvest exported files"""
    files = earliest_by_month_exported(data_path)
    easynvest = read.read_all_csv_for(files,
                                      sep=';',
                                      encoding='latin',
                                      header=1)
    return preprocess(easynvest, data_path)
