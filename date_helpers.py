import calendar
import pandas as pd


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
    import calendar
    first_day = date.replace(day=1)
    last_day = date.replace(day=calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day


def previous_month(date):
    """Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month later.

    Note that the resultant day of the month might change if the following
    month has fewer days:

        >>> subtract_one_month(datetime.date(2010, 3, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_earlier = date - one_day
    while one_month_earlier.month == date.month or one_month_earlier.day > date.day:
        one_month_earlier -= one_day
    return one_month_earlier


def weekdays_in_month(base_date):
    """Return number of weekdays in passed month"""
    month_calendar = calendar.monthcalendar(base_date.year, base_date.month)
    weekdays = 0
    for week in month_calendar:
        for day in filter(lambda x: x > 0, week):
            if calendar.weekday(base_date.year, base_date.month, day) < 5:
                weekdays += 1
    return weekdays
