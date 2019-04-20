"""All totals for all investments categories"""

from investments import filters as ft
import pandas as pd
import numpy as np
import record_summary as rs


def total_invested_by(column, invest):
    """Total invested grouped by column"""
    return rs.total_amount_by(column, ft.invested(invest))


def total_applications_by(column, invest):
    """Total applications grouped by column"""
    return rs.total_amount_by(column, ft.applications(invest))


def total_income_by(column, incomes):
    """Total incomes/salaries grouped by column"""
    return rs.total_amount_by(column, ft.income(incomes))


def total_discounts_by(column, incomes):
    """Total discounts grouped by column"""
    return rs.total_amount_by(column, ft.discounts(incomes))


def invested_for_month_by(column, invest, base_date):
    """Total invested on current month given base_date"""
    invested = rs.records_for_month(invest, base_date)
    return total_invested_by(column, invested)


def applications_for_month(incomes, base_date):
    """Total applications on current month given base_date"""
    applications = rs.records_for_month(ft.applications(incomes), base_date)
    return rs.total_amount_by('title', applications)


def absolute_return_for_month(invest, base_date):
    """Total return on current month given base_date"""
    past_month = rs.records_for_previous_month(invest, base_date)
    current_month = rs.records_for_month(invest, base_date)

    invested_previous_month = total_invested_by('title', past_month)
    invested_for_month = total_invested_by('title', current_month)
    applications_month = total_applications_by('title', current_month)
    discounts_month = total_discounts_by('title', current_month)

    return invested_for_month \
        .sub(invested_previous_month, fill_value=0) \
        .sub(applications_month, fill_value=0) \
        .add(discounts_month, fill_value=0)


def absolute_return_for_month_percentage(invest, base_date):
    """Total return on percentage for current month given base_date.
    This operation is heavier than return_for_month_percentage
    because it computes all data dependencies instead of receiving
    some of the pre computed"""
    month_return = absolute_return_for_month(invest, base_date)
    past_month = rs.records_for_previous_month(invest, base_date)
    invested_last_month = total_invested_by('title', past_month)
    return month_return / invested_last_month


def monthly_return_percentage(invest, base_date):
    """Monthly return percentage given investments.
    Even though it has a different calculation, it returns the same results
    as absolute_return_for_month_percentage"""
    past_month = rs.records_for_previous_month(invest, base_date)
    current_month = rs.records_for_month(invest, base_date)

    invested_previous_month = total_invested_by('title', past_month)
    invested_for_month = total_invested_by('title', current_month)
    applications_month = total_applications_by('title', current_month)
    discounts_month = total_discounts_by('title', current_month)

    return invested_for_month\
        .sub(applications_month, fill_value=0)\
        .add(discounts_month, fill_value=0)\
        .div(invested_previous_month, fill_value=0) - 1


def return_with_inflation(return_perc, base_date):
    """Total return on percentage with inflation discounted
    for current month given base_date"""
    from load import central_bank
    ipca = central_bank.ipca_for_month(base_date)
    if ipca is not None:
        return return_perc - ipca
    return pd.DataFrame(np.nan, index=return_perc.index, columns=['amount'])
