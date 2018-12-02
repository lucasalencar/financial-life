import pandas as pd
import numpy as np
import formatting as fmt
import seaborn as sns
from record_summary import *
from date_helpers import records_for_month, past_records_for_month, records_for_previous_month
from central_bank_data import central_bank_metric, BC_IPCA_BY_MONTH_ID
from datetime import datetime

def total_invested_by(invest, column):
    invested = invest[invest.category == 'valor aplicado']
    return total_amount_by(column, invested)


def invested_previous_month_by(invest, base_date, column):
    invest_previous_month = records_for_previous_month(invest, base_date)
    return total_invested_by(invest_previous_month, column)


def invested_for_month_by(invest, base_date, column):
    invested = records_for_month(invest, base_date)
    return total_invested_by(invested, column)


def applications_for_month(incomes, base_date):
    applications = records_for_month(incomes[incomes.category == 'aplicação'], base_date)
    return total_amount_by('title', applications)


def return_for_month(invest, base_date):
    total_invested_previous_month = invested_previous_month_by(invest, base_date, 'title')
    total_invested_for_month = invested_for_month_by(invest, base_date, 'title')
    total_applications_for_month = applications_for_month(invest, base_date)

    return total_invested_for_month \
        .sub(total_invested_previous_month, fill_value=0) \
        .sub(total_applications_for_month, fill_value=0)


def return_for_month_percentage(invest_return_for_month, invested_previous_month):
    return invest_return_for_month / invested_previous_month


def return_for_month_percentage_heavy(invest, base_date):
    """Computes percentage of return but starting from the raw data,
    without depending on preprocessed data."""
    return return_for_month_percentage(return_for_month(invest, base_date),
                                       invested_previous_month_by(invest, base_date, 'title'))


def return_with_inflation(return_perc, base_date):
    ipca = central_bank_metric(BC_IPCA_BY_MONTH_ID, base_date)
    if ipca is not None:
        return return_perc - ipca
    else:
        return pd.DataFrame(np.nan, index=return_perc.index, columns=['amount'])


def summary_investments_current_month(invest, base_date):
    invest_return_for_month = return_for_month(invest, base_date)
    invested_previous_month = invested_previous_month_by(invest, base_date, 'title')
    invest_return_for_month_perc = return_for_month_percentage(invest_return_for_month, invested_previous_month)

    summary = {'Total': invested_for_month_by(invest, base_date, 'title').amount,
               'Total last month': invested_previous_month.amount,
               'Return for month': invest_return_for_month.amount,
               'Return for month (%)': invest_return_for_month_perc.amount,
               'Return with inflation (%)': return_with_inflation(invest_return_for_month_perc, base_date).amount}

    summary_columns = summary.keys()
    summary_invest = pd.DataFrame(summary, columns=list(summary_columns))
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


def return_over_time(invest):
    return describe_over_time(invest,
                              lambda data, date:
                                return_for_month(data, date).amount)


def return_percentage_over_time(invest):
    return describe_over_time(invest,
                              lambda data, date:
                                return_for_month_percentage_heavy(data, date).amount)


def cumulative_return_over_time(invest):
    return describe_over_time(invest,
                              lambda data, date:
                                return_for_month(data, date).amount).cumsum()


def plot_return_over_time(return_over_time, title):
    data = return_over_time.reset_index().rename(columns={'index': 'date'})
    plt = data.plot(title=title, figsize=(20, 7), grid=True, fontsize=15, xticks=data.index)
    plt.set_xticklabels(data.date)
    plt.legend(fontsize=15)
    return plt


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
    months = available_months(invest)

    total = sum_amount_by_month(invest, months,
                                lambda invest, base_date: invested_for_month_by(invest, base_date, 'title'))
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


def plot_invest_type_distribution(invest, base_date):
    invested_by_type = invested_for_month_by(invest, base_date, 'type')
    type_distribution = (invested_by_type / invested_by_type.sum()).sort_values('amount')
    return type_distribution.plot.pie(y='amount', figsize=(10,10), autopct='%1.1f%%', fontsize=15,
                                      legend=False, title="Distribuição por categoria")


def plot_assets_summary(data, start_date):
    summary = data.loc[start_date:].reset_index()
    plt = summary.plot(figsize=(20, 5), grid=True, fontsize=15, xticks=summary.index)
    plt.set_xticklabels(summary.date)
    plt.legend(fontsize=15)
    return plt


def style_assets_goals(assets_goals, assets_thresh):
    return assets_goals.style\
        .format({'amount': fmt.BR_CURRENCY_FORMAT})\
        .applymap(fmt.green_background_threshold(assets_thresh))
