import calendar
import pandas as pd

def by_monthly_period(data, start, end):
    """Filter data from the beggining of month on start until the end of month on end."""
    month_last_day = calendar.monthrange(start.year, end.month)[1]
    return data[(data.date >= pd.Timestamp(start.replace(day=1))) &
                (data.date <= pd.Timestamp(end.replace(day=month_last_day)))]
