import pandas as pd
import numpy as np
import formatting as fmt
import seaborn as sns
from record_summary import total_amount_by, cumulative_amount_by, groupby_month
from date_helpers import records_for_month, past_records_for_month, records_for_previous_month
from central_bank_data import central_bank_metric, BC_IPCA_BY_MONTH_ID
from datetime import datetime

def total_invested_by_title(invest):
    invested = invest[invest.category == 'valor aplicado']
    return total_amount_by('title', invested)


def invested_previous_month(invest, base_date):
    invest_previous_month = records_for_previous_month(invest, base_date)
    return total_invested_by_title(invest_previous_month)


def invested_for_month(invest, base_date):
    invested = records_for_month(invest, base_date)
    return total_invested_by_title(invested)


def applications_for_month(incomes, base_date):
    applications = records_for_month(incomes[incomes.category == 'aplicação'], base_date)
    return total_amount_by('title', applications)


def return_for_month(invest, base_date):
    total_invested_previous_month = invested_previous_month(invest, base_date)
    total_invested_for_month = invested_for_month(invest, base_date)
    total_applications_for_month = applications_for_month(invest, base_date)

    return total_invested_for_month \
        .sub(total_invested_previous_month, fill_value=0) \
        .sub(total_applications_for_month, fill_value=0)


def describe_return_for_month(invest, base_date):
    """Returns total investiment return for month
    and its percentage given the investment history."""
    invest_return_for_month = return_for_month(invest, base_date)
    total_invested_previous_month = invested_previous_month(invest, base_date)
    invest_return_for_month_perc = invest_return_for_month / total_invested_previous_month
    return invest_return_for_month, invest_return_for_month_perc


def return_with_inflation(return_perc, base_date):
    ipca = central_bank_metric(BC_IPCA_BY_MONTH_ID, base_date)
    if ipca is not None:
        return return_perc - ipca
    else:
        return pd.DataFrame(np.nan, index=return_perc.index, columns=[0])


def summary_investiments_current_month(invest, base_date):
    invest_return_for_month, return_for_month_perc = describe_return_for_month(invest, base_date)

    summary_columns = [
        invested_for_month(invest, base_date),
        invested_previous_month(invest, base_date),
        invest_return_for_month,
        return_for_month_perc,
        return_with_inflation(return_for_month_perc, base_date)
    ]

    summary_invest = pd.concat(summary_columns, axis=1, sort=False)
    summary_invest.columns = [
        'Total',
        'Total last month',
        'Return for month',
        'Return for month (%)',
        'Return with inflation (%)'
    ]
    return summary_invest[summary_invest['Total'] > 0]


MONTHLY_INVEST_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Total last month': fmt.BR_CURRENCY_FORMAT,
    'Return for month': fmt.BR_CURRENCY_FORMAT,
    'Return for month (%)': fmt.PERC_FORMAT,
    'Return with inflation (%)': fmt.PERC_FORMAT
}


def style_summary_investments(summary, return_for_month_goal, return_with_inflation_goal):
    return summary.style\
        .format(MONTHLY_INVEST_COLS_FORMAT)\
        .applymap(fmt.red_to_green_background(return_for_month_goal),
                  subset=['Return for month', 'Return for month (%)'])\
        .applymap(fmt.red_to_green_background(return_with_inflation_goal),
                  subset=['Return with inflation (%)'])


def month_to_date(month):
    return datetime.strptime(month, '%Y-%m').date()


def sum_amount_by_month(invest, months, select_data):
    return months.map(lambda month: select_data(invest, month_to_date(month)).sum().amount)


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Applications / Total': fmt.PERC_FORMAT
}


def summary_assets(invest):
    months = pd.Series(groupby_month(invest).unique())

    total = sum_amount_by_month(invest, months, invested_for_month)
    invest_return = sum_amount_by_month(invest, months, return_for_month)
    applications = sum_amount_by_month(invest, months, applications_for_month)

    columns = ['date'] + list(ASSETS_SUMMARY_COLS_FORMAT.keys())

    assets_summary = pd.DataFrame({'date': months,
                                   'Total': total,
                                   'Return': invest_return,
                                   'Return / Total': invest_return / total,
                                   'Applications': applications,
                                   'Applications / Total': applications / total},
                                  columns=columns).set_index('date')
    return assets_summary



def style_summary_assets(summary):
    cm = sns.light_palette("green", as_cmap=True)
    background_subset = pd.IndexSlice['2018-02':, ['Total',
                                                   'Return',
                                                   'Return / Total',
                                                   'Applications',
                                                   'Applications / Total']]

    return summary.style\
        .format(ASSETS_SUMMARY_COLS_FORMAT)\
        .background_gradient(cmap=cm, subset=background_subset)


def style_assets_goals(assets_goals, assets_thresh):
    return assets_goals.style\
        .format({'amount': fmt.BR_CURRENCY_FORMAT})\
        .applymap(fmt.green_background_threshold(assets_thresh))
