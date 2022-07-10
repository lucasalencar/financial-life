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

def load_local(timeseries_id=None, data_path='./data', **configs):
    return pd.read_csv('%s/%s.csv' % (data_path, BC_IPCA_BY_MONTH_ID))


def load_remote(timeseries_id=None, data_path='./data', **configs):
    timeseries_url = CENTRAL_BANK_TIMESERIES_URL % timeseries_id
    try:
        timeseries = pd.read_csv(timeseries_url, sep=";")
        timeseries.to_csv('%s/%s.csv' % (data_path, BC_IPCA_BY_MONTH_ID), index=False)
    except:
        timeseries = load_local(timeseries_id=timeseries_id, data_path=data_path, **configs)
    return timeseries


def load(**configs):
    return load_remote(**configs)


def preprocess(timeseries):
    """Read Brazil Central Bank timeseries for multiple indexes (IPCA, SELIC, CDI)
    given the series ID"""
    timeseries['data'] = pd.to_datetime(timeseries['data'], format="%d/%m/%Y")
    timeseries['valor'] = timeseries['valor'].apply(lambda x: float(x.replace(',', '.')) / 100)
    timeseries = timeseries.rename(index=str, columns={'data': 'date', 'valor': 'value'})
    return timeseries


def central_bank_metric_for_month(timeseries, base_date):
    """Returns the metric given the year and month on the base_date parameter.
    Specific for time series fetched from Central Bank website."""
    metric_for_month = timeseries[timeseries.date == base_date.strftime("%Y-%m")]
    if metric_for_month.empty:
        return None
    else:
        return metric_for_month.iloc[0, 1]


def central_bank_metric(timeseries_id, base_date):
    data = preprocess(load(timeseries_id=timeseries_id, base_date=base_date))
    return central_bank_metric_for_month(data, base_date)


def ipca_for_month(base_date):
    return central_bank_metric(BC_IPCA_BY_MONTH_ID, base_date)


def selic_for_month(base_date):
    return central_bank_metric(BC_SELIC_ACCUM_MONTH_ID, base_date)


def cdi_for_month(base_date):
    return central_bank_metric(BC_CDI_BY_DAY_ACCUM_MONTH_ID, base_date)
