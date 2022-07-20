import pandas as pd
import numpy as np

from . import aggregate

def describe_over_time(data, describe_fn):
    """Get available months on data and computes describe_fn for each month"""
    data_over_time = {}
    for month in aggregate.datetime.available_months(data):
        data_over_time[month] = describe_fn(data, aggregate.datetime.month_to_date(month))
    return pd.DataFrame(data_over_time, columns=sorted(data_over_time.keys()))\
        .replace([np.inf, -np.inf], np.nan).transpose()
