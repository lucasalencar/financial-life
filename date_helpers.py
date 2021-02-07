import calendar
import pandas as pd

from dateutil.relativedelta import relativedelta


def beginning_of_month(date):
    return date.replace(day=1)


def end_of_month(date):
    import calendar
    return date.replace(day=calendar.monthrange(date.year, date.month)[1])


def month_day_range(date):
    """
    For a date 'date' returns the start and end date for the month of 'date'.

    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))

    https://gist.github.com/waynemoore/1109153
    """
    return beginning_of_month(date), end_of_month(date)


def weekdays_in_month(base_date):
    """Return number of weekdays in passed month"""
    month_calendar = calendar.monthcalendar(base_date.year, base_date.month)
    weekdays = 0
    for week in month_calendar:
        for day in filter(lambda x: x > 0, week):
            if calendar.weekday(base_date.year, base_date.month, day) < 5:
                weekdays += 1
    return weekdays


def years_ago(base_date, years):
    """Get date years ago based on base date"""
    return base_date - relativedelta(years=years)


def months_ago(base_date, months):
    """Get date months ago based on base date"""
    return base_date - relativedelta(months=months)
