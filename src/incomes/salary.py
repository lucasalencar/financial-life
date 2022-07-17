from .. import filters
from .. import record_summary as rs
from .. import date_helpers as dh


def earned_for_month(incomes, base_date):
    return filters.datetime.records_for_month(incomes[incomes.category == 'renda'], base_date).amount.sum()


def hours_worked_for_month(hours_worked_by_day, base_date):
    return hours_worked_by_day * dh.weekdays_in_month(base_date)
