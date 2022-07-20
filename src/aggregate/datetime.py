#!/usr/bin/env python3

from datetime import datetime
import pandas as pd

def groupby_month(data):
    """Returns groupby month given data records"""
    return data['date'].dt.strftime("%Y-%m")

def available_months(dataset):
    """All months available in dataset"""
    return pd.Series(groupby_month(dataset).unique())

def month_to_date(month):
    """Converts standard date format %Y-%m to date object"""
    return datetime.strptime(month, '%Y-%m').date()
