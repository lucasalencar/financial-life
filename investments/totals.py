"""All totals for all investments categories"""

import pandas as pd
import numpy as np
from investments import filters as ft
from record_summary import total_amount_by
from date_helpers import records_for_month, records_for_previous_month


def total_invested_by(column, invest):
    """Total invested grouped by column"""
    return total_amount_by(column, ft.invested(invest))


def invested_previous_month_by(column, invest, base_date):
    """Total invested on previous month given base_date"""
    invest_previous_month = records_for_previous_month(invest, base_date)
    return total_invested_by(column, invest_previous_month)


def invested_for_month_by(column, invest, base_date):
    """Total invested on current month given base_date"""
    invested = records_for_month(invest, base_date)
    return total_invested_by(column, invested)


def applications_for_month(incomes, base_date):
    """Total applications on current month given base_date"""
    applications = records_for_month(ft.applications(incomes), base_date)
    return total_amount_by('title', applications)


def discounts_for_month(incomes, base_date):
    """Total discounts on current month given base_date"""
    discounts = records_for_month(ft.discounts(incomes), base_date)
    return total_amount_by('title', discounts)


def return_for_month(invest, base_date):
    """Total return on current month given base_date"""
    invested_previous_month = invested_previous_month_by('title', invest,
                                                         base_date)
    invested_for_month = invested_for_month_by('title', invest, base_date)
    applications_month = applications_for_month(invest, base_date)
    discounts_month = discounts_for_month(invest, base_date)

    return invested_for_month \
        .sub(invested_previous_month, fill_value=0) \
        .sub(applications_month, fill_value=0) \
        .add(discounts_month, fill_value=0)


def return_for_month_percentage(invest_return_for_month,
                                invested_previous_month):
    """Total return on percentage for current month given base_date"""
    return invest_return_for_month / invested_previous_month


def return_for_month_percentage_heavy(invest, base_date):
    """Total return on percentage for current month given base_date.
    This operation is heavier than return_for_month_percentage
    because it computes all data dependencies instead of receiving
    some of the pre computed"""
    month_return = return_for_month(invest, base_date)
    invested_last_month = invested_previous_month_by('title', invest,
                                                     base_date)
    return return_for_month_percentage(month_return, invested_last_month)


def return_with_inflation(return_perc, base_date):
    """Total return on percentage with inflation discounted
    for current month given base_date"""
    from central_bank_data import central_bank_metric, BC_IPCA_BY_MONTH_ID
    ipca = central_bank_metric(BC_IPCA_BY_MONTH_ID, base_date)
    if ipca is not None:
        return return_perc - ipca
    return pd.DataFrame(np.nan, index=return_perc.index, columns=['amount'])
