def records_for_month(records, base_date):
    """Selects records that goes from the beginning to end of month."""
    month_range = month_day_range(base_date)
    return records[(records.date >= month_range[0]) & (records.date <= month_range[1])]


def past_records_for_month(records, base_date):
    """Returns all records past the month in the base_date parameter."""
    month_range = month_day_range(base_date)
    return records[records.date < month_range[0]]


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
