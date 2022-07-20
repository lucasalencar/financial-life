from . import totals as tt

import pandas as pd
from .. import filters
from .. import date_helpers as dth
from .. import formatting as fmt

def summary(invest, base_date):
    last_month_date = dth.months_ago(base_date, 1)
    past_month = filters.datetime.by_monthly_period(invest, last_month_date, last_month_date)
    current_month = filters.datetime.by_monthly_period(invest, base_date, base_date)

    invest_return_for_month = tt.absolute_return_for_month(invest, base_date)
    invested_previous_month = tt.total_invested_by('title', past_month)

    invest_return_for_month_perc = invest_return_for_month / invested_previous_month

    summary = {'Total': tt.total_invested_by('title', current_month).amount,
               'Total last month': invested_previous_month.amount,
               'Return for month': invest_return_for_month.amount,
               'Return for month (%)': invest_return_for_month_perc.amount,
               'Return with inflation (%)': tt.return_with_inflation(
                   invest_return_for_month_perc, base_date).amount}

    summary_invest = pd.DataFrame(summary, columns=list(summary.keys()))
    return summary_invest[summary_invest['Total'] > 0]


MONTHLY_INVEST_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Total last month': fmt.BR_CURRENCY_FORMAT,
    'Return for month': fmt.BR_CURRENCY_FORMAT,
    'Return for month (%)': fmt.PERC_FORMAT,
    'Return with inflation (%)': fmt.PERC_FORMAT
}


def style_summary(summary, return_for_month_goal,
                              return_with_inflation_goal):
    return summary.style\
        .format(MONTHLY_INVEST_COLS_FORMAT)\
        .applymap(fmt.red_to_green_background(return_for_month_goal),
                  subset=['Return for month', 'Return for month (%)'])\
        .applymap(fmt.red_to_green_background(return_with_inflation_goal),
                  subset=['Return with inflation (%)'])

