import pandas as pd
import calendar

from .. import date_helpers as dth


def by_monthly_period(data, start, end):
    """Filter data from the beggining of month on start until the end of month on end."""
    month_last_day = calendar.monthrange(end.year, end.month)[1]
    return data[(data.date >= pd.Timestamp(start.replace(day=1))) &
                (data.date <= pd.Timestamp(end.replace(day=month_last_day)))]


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

