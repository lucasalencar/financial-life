import pandas as pd
import formatting as fmt
from record_summary import total_amount_by
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
