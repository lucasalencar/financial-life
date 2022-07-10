from datetime import datetime
import pandas as pd
import numpy as np
from . import date_helpers as dth


def records_for_month(records, base_date):
    """Selects records that goes from the beginning to end of month."""
    month_range = dth.month_day_range(base_date)
    beginning_of_month = pd.Timestamp(month_range[0])
    end_of_month = pd.Timestamp(month_range[1])
    return records[(records.date >= beginning_of_month) &
                   (records.date <= end_of_month)]


def records_for_previous_month(records, base_date):
    """Selects records that are in the previous month given the base_date."""
    month_range = dth.month_day_range(dth.months_ago(base_date, 1))
    return records[(records.date >= pd.Timestamp(month_range[0])) &
                   (records.date <= pd.Timestamp(month_range[1]))]


def past_records_for_month(records, base_date):
    """Returns all records past the month in the base_date parameter."""
    month_range = dth.month_day_range(base_date)
    beginning_of_month = pd.Timestamp(month_range[0])
    return records[records.date < beginning_of_month]


def groupby_month(data):
    """Returns groupby month given data records"""
    return data['date'].dt.strftime("%Y-%m")


def total_amount_by(groupby, records):
    """Sums total amount given a column to group by"""
    return records.groupby(groupby).sum()


def cumulative_amount_by(groupby, records):
    """Cumulative total amount given a column to group by"""
    return total_amount_by(groupby, records).sort_index().cumsum()


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
