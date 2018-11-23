from datetime import datetime
import pandas as pd

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
