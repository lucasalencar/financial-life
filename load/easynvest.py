import pandas as pd
import re
from load import read
import record_summary as rs
import date_helpers as dth


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
    loaded = date_from_filename(loaded, filepath)
    loaded = rename_columns(loaded)
    return loaded


def load(data_path=None):
    """Load and preprocess easynvest exported files"""
    files = earliest_by_month_exported(data_path)
    easynvest = read.read_all_csv_for(files,
                                      sep=';',
                                      encoding='latin',
                                      header=1)
    return preprocess(easynvest, data_path)
