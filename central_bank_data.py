import pandas as pd

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
    timeseries['valor'] = timeseries['valor'].apply(lambda x: float(x.replace(',', '.')) / 100)
    timeseries = timeseries.rename(index=str, columns={'data': 'date', 'valor': value_column_name})
    return timeseries


def central_bank_metric_for_month(timeseries, base_date):
    """Returns the metric given the year and month on the base_date parameter.
    Specific for time series fetched from Central Bank website."""
    metric_for_month = timeseries[timeseries.date == base_date.strftime("%Y-%m")]
    if metric_for_month.empty:
        return None
    else:
        return metric_for_month.iloc[0, 1]

def central_bank_metric(timeseries_id, base_date, value_column_name='value'):
    timeseries = read_central_bank_data(timeseries_id, value_column_name)
    return central_bank_metric_for_month(timeseries, base_date)
