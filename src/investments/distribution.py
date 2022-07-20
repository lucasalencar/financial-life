"""Investment distribution functions"""

from . import totals as tt
from ..plotting import defaults, pie
from .. import filters


def describe(invest, column, base_date):
    """Returns relevant data about types"""
    current_month = filters.datetime.by_monthly_period(invest, base_date, base_date)
    return tt.total_invested_by(column, current_month).amount


def plot(invest, column, base_date, height=400, **configs):
    """Pie chart by types distribution"""
    by_type = describe(invest, column, base_date)
    return pie.plot(by_type, height=height, **configs)
