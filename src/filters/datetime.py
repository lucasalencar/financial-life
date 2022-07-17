import pandas as pd
import calendar


def by_monthly_period(data, start, end):
    """Filter data from the beggining of month on start until the end of month on end."""
    start_period_beginning_of_month = start.replace(day=1)
    month_last_day = calendar.monthrange(end.year, end.month)[1]
    end_period_end_of_month = end.replace(day=month_last_day)
    return data[(data.date >= pd.Timestamp(start_period_beginning_of_month)) &
                (data.date <= pd.Timestamp(end_period_end_of_month))]
