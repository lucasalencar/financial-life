import pandas as pd
import formatting as fmt
import seaborn as sns
from record_summary import total_amount_by, cumulative_amount_by, groupby_month
from date_helpers import records_for_month, past_records_for_month


def total_investiment_return_for_month(invest, base_date):
    """Total investiment return for the month on the base date."""
    invest_for_month = records_for_month(invest, base_date)
    return invest_for_month[invest_for_month.category == 'Rendimento']\
        [['title', 'amount']].set_index('title')


def investiment_return_for_month(invest, base_date):
    """Returns total investiment return for month
    and its percentage given the investment history."""
    past_invetiments = past_records_for_month(invest, base_date)
    total_past_invest_by_title = total_amount_by('title', past_invetiments)
    invest_return_for_month = total_investiment_return_for_month(invest, base_date)
    invest_return_for_month_perc = invest_return_for_month / total_past_invest_by_title
    return invest_return_for_month, invest_return_for_month_perc


def summary_investiments(invest, base_date):
    total_invest_by_title = total_amount_by('title', invest)
    invest_return_for_month, invest_return_for_month_perc = investiment_return_for_month(invest, base_date)
    summary_invest = pd.concat([total_invest_by_title, invest_return_for_month, invest_return_for_month_perc], axis=1, sort=False)
    summary_invest.columns = ['Total', 'Return for month', 'Return for month (%)']
    return summary_invest.sort_values('Return for month (%)', ascending=False).dropna()


MONTHLY_INVEST_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return for month': fmt.BR_CURRENCY_FORMAT,
    'Return for month (%)': fmt.PERC_FORMAT
}


def style_summary_investments(summary, return_goal):
    return summary.style\
        .format(MONTHLY_INVEST_COLS_FORMAT)\
        .applymap(fmt.red_to_green_background(return_goal), subset=['Return for month', 'Return for month (%)'])


def summary_invest_return(invest):
    invest_return = invest[invest.category == 'Rendimento']
    total_return_by_month = total_amount_by(groupby_month(invest_return), invest_return)
    return total_return_by_month


def summary_invest_applications(invest):
    invest_application = invest[invest.category == 'Aplicação']
    total_application_by_month = total_amount_by(groupby_month(invest_application), invest_application)
    return total_application_by_month


def summary_assets(invest):
    cumulative_assets_by_month = cumulative_amount_by(groupby_month(invest), invest)

    total_return_by_month = summary_invest_return(invest)
    total_application_by_month = summary_invest_applications(invest)

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