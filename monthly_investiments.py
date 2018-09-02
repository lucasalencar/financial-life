import pandas as pd
import numpy as np
import formatting as fmt
import seaborn as sns
from record_summary import total_amount_by, cumulative_amount_by, groupby_month
from date_helpers import records_for_month, past_records_for_month
from central_bank_data import central_bank_metric, BC_IPCA_BY_MONTH_ID


def total_return_for_month(invest, base_date):
    """Total investiment return for the month on the base date."""
    invest_for_month = records_for_month(invest, base_date)
    return invest_for_month[invest_for_month.category == 'rendimento']\
        [['title', 'amount']].set_index('title')


def return_for_month(invest, base_date):
    """Returns total investiment return for month
    and its percentage given the investment history."""
    past_invetiments = past_records_for_month(invest, base_date)
    total_past_invest_by_title = total_amount_by('title', past_invetiments)
    invest_return_for_month = total_return_for_month(invest, base_date)
    invest_return_for_month_perc = invest_return_for_month / total_past_invest_by_title
    return invest_return_for_month, invest_return_for_month_perc


def return_with_inflation(return_perc, base_date):
    ipca = central_bank_metric(BC_IPCA_BY_MONTH_ID, base_date)
    if ipca is not None:
        return return_perc - ipca
    else:
        return pd.DataFrame(np.nan, index=return_perc.index, columns=[0])


def summary_investiments(invest, base_date):
    invest_return_for_month, return_for_month_perc = return_for_month(invest, base_date)

    summary_columns = [
        total_amount_by('title', invest),
        invest_return_for_month,
        return_for_month_perc,
        return_with_inflation(return_for_month_perc, base_date)
    ]

    summary_invest = pd.concat(summary_columns, axis=1, sort=False)
    summary_invest.columns = [
        'Total',
        'Return for month',
        'Return for month (%)',
        'Return with inflation (%)'
    ]
    return summary_invest.sort_values('Return for month (%)', ascending=False).dropna()


MONTHLY_INVEST_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
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


def summary_invest_by_category(invest, category):
    invest_by_category = invest[invest.category == category]
    total_invest_by_month = total_amount_by(groupby_month(invest_by_category), invest_by_category)
    return total_invest_by_month


def summary_assets(invest):
    cumulative_assets_by_month = cumulative_amount_by(groupby_month(invest), invest)

    total_return_by_month = summary_invest_by_category(invest,'rendimento')
    total_application_by_month = summary_invest_by_category(invest, 'aplicação')

    return_proportion_by_month = total_return_by_month / cumulative_assets_by_month
    application_proportion_by_month = total_application_by_month / cumulative_assets_by_month

    assets_summary = pd.concat([cumulative_assets_by_month,
                                total_return_by_month,
                                return_proportion_by_month,
                                total_application_by_month,
                                application_proportion_by_month], axis=1, sort=False)

    assets_summary.columns = ['Total', 'Return', 'Return / Total', 'Applications', 'Applications / Total']
    return assets_summary


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Applications / Total': fmt.PERC_FORMAT
}


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
