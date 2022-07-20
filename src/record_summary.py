from datetime import datetime
import pandas as pd
import numpy as np
from . import date_helpers as dth


def groupby_month(data):
    """Returns groupby month given data records"""
    return data['date'].dt.strftime("%Y-%m")


def available_months(dataset):
    """All months available in dataset"""
    return pd.Series(groupby_month(dataset).unique())


def month_to_date(month):
    """Converts standard date format %Y-%m to date object"""
    return datetime.strptime(month, '%Y-%m').date()


def describe_over_time(data, describe_fn):
    """Get available months on data and computes describe_fn for each month"""
    data_over_time = {}
    for month in available_months(data):
        data_over_time[month] = describe_fn(data, month_to_date(month))
    return pd.DataFrame(data_over_time, columns=sorted(data_over_time.keys()))\
        .replace([np.inf, -np.inf], np.nan).transpose()
