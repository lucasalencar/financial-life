import pandas as pd
import numpy as np
from datetime import datetime
from record_summary import describe_over_time
from investments import totals as tt

def absolute_return_amount_by_date(data, date):
    return tt.absolute_return_for_month(data, date).amount


def return_over_time(invest):
    return describe_over_time(invest, absolute_return_amount_by_date)


def absolute_return_amount_percentage_by_date(data, date):
    return tt.absolute_return_for_month_percentage(data, date).amount


def return_percentage_over_time(invest):
    return describe_over_time(invest, absolute_return_amount_percentage_by_date)


def cumulative_return_over_time(invest):
    return describe_over_time(invest, absolute_return_amount_by_date).cumsum()
