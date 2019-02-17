# pylint: disable=C0111

import pandas as pd
import seaborn as sns
import formatting as fmt
from record_summary import describe_over_time
from date_helpers import records_for_month, records_for_previous_month

from investments import totals as tt


def summary_investments_current_month(invest, base_date):
    past_month = records_for_previous_month(invest, base_date)
    current_month = records_for_month(invest, base_date)

    invest_return_for_month = tt.return_for_month(invest, base_date)
    invested_previous_month = tt.total_invested_by('title', past_month)

    invest_return_for_month_perc = tt.return_for_month_percentage(
        invest_return_for_month, invested_previous_month)

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


def style_summary_investments(summary, return_for_month_goal,
                              return_with_inflation_goal):
    return summary.style\
        .format(MONTHLY_INVEST_COLS_FORMAT)\
        .applymap(fmt.red_to_green_background(return_for_month_goal),
                  subset=['Return for month', 'Return for month (%)'])\
        .applymap(fmt.red_to_green_background(return_with_inflation_goal),
                  subset=['Return with inflation (%)'])


def return_over_time(invest):
    return describe_over_time(invest,
                              lambda data, date:
                              tt.return_for_month(data, date).amount)


def return_percentage_over_time(invest):
    return describe_over_time(invest,
                              lambda data, date:
                              tt.return_for_month_percentage_heavy(
                                  data, date).amount)


def cumulative_return_over_time(invest):
    return describe_over_time(invest,
                              lambda data, date:
                              tt.return_for_month(data, date).amount).cumsum()


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Applications / Total': fmt.PERC_FORMAT
}


def summary_assets(invest):
    total = describe_over_time(invest,
                               lambda data, date:
                               tt.invested_for_month_by('title', invest, date)
                               .sum()).amount
    invest_return = describe_over_time(invest,
                                       lambda data, date:
                                       tt.return_for_month(data, date)
                                       .sum()).amount
    applications = describe_over_time(invest,
                                      lambda data, date:
                                      tt.applications_for_month(data, date)
                                      .sum()).amount

    summary = {'Total': total,
               'Return': invest_return,
               'Return / Total': invest_return / total,
               'Applications': applications,
               'Applications / Total': applications / total}

    assets_summary = pd.DataFrame(summary, columns=list(summary.keys()))
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


def plot_invest_type_distribution(invest, base_date):
    current_month = records_for_month(invest, base_date)
    invested_by_type = tt.total_invested_by('type', current_month)
    type_distribution = (invested_by_type / invested_by_type.sum()).sort_values('amount')
    return type_distribution.plot.pie(y='amount', figsize=(10,10), autopct='%1.1f%%', fontsize=15,
                                      legend=False, title="Distribuição por categoria")


def style_assets_goals(assets_goals, assets_thresh):
    return assets_goals.style\
        .format({'amount': fmt.BR_CURRENCY_FORMAT})\
        .applymap(fmt.green_background_threshold(assets_thresh))


def finished_invests(invest):
    applications = tt.total_applications_by('title', invest)
    return applications[applications.amount <= 0]


def invests_final_return(incomes):
    applications = tt.total_applications_by('title', incomes[incomes.amount > 0])
    liquidations = tt.total_income_by('title', incomes)
    discounts = tt.total_discounts_by('title', incomes)

    return liquidations.sub(applications, fill_value=0).add(discounts, fill_value=0)
