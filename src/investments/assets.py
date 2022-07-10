import pandas as pd
import seaborn as sns
from .. import record_summary as rs
from .. import formatting as fmt
import plotly.graph_objs as go

from datetime import date
from plotly.offline import iplot
from . import totals as tt
from . import filters as ft
from ..plotting import defaults

def roi(incomes, base_date):
    """https://www.investopedia.com/terms/r/returnoninvestment.asp"""
    invested = tt.invested_for_month_by('title', incomes, base_date).amount.sum()
    previous_incomes = incomes[incomes.date < pd.Timestamp(base_date.replace(day=1))]
    applications = ft.applications(previous_incomes).amount.sum()

    if applications == 0:
        return 0.0

    return (invested - applications) / applications


def invested_over_time(invest):
    return rs.describe_over_time(invest,
                                 lambda data, date:
                                 tt.invested_for_month_by('title', invest, date)
                                 .sum()).amount


def return_over_time(invest):
    return rs.describe_over_time(invest,
                                 lambda data, date:
                                 tt.absolute_return_for_month(data, date)
                                 .sum()).amount


def applications_over_time(invest):
    return rs.describe_over_time(invest,
                                 lambda data, date:
                                 tt.applications_for_month(data, date)
                                 .sum()).amount


def monthly_return_over_time(invest):
    return rs.describe_over_time(invest,
                                 lambda data, date:
                                 pd.Series(tt.total_monthly_return(data, date),
                                           index=['amount'])).amount


def roi_over_time(invest):
    return rs.describe_over_time(invest,
                                 lambda data, date:
                                 pd.Series(roi(data, date), index=['amount'])).amount


def cumulative_return_over_time(invest):
    return return_over_time(invest).cumsum()


def summary(invest, start_date, end_date):
    invested = invested_over_time(invest)
    invest_return = return_over_time(invest)
    cumulative_return = cumulative_return_over_time(invest)
    applications = applications_over_time(invest)
    monthly_return = monthly_return_over_time(invest)
    invest_roi = roi_over_time(invest)

    summary = {'Total': invested,
               'Return': invest_return,
               'Cumulative Return': cumulative_return,
               'Return / Total': invest_return / invested,
               'Applications': applications,
               'Monthly Return': monthly_return,
               'ROI': invest_roi}

    assets_summary = pd.DataFrame(summary, columns=list(summary.keys()))
    return assets_summary.loc[start_date.strftime('%Y-%m'):end_date.strftime('%Y-%m')]


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Cumulative Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Monthly Return': fmt.PERC_FORMAT,
    'ROI': fmt.PERC_FORMAT,
}


def style_summary(summary):
    return summary.style\
        .format(ASSETS_SUMMARY_COLS_FORMAT)\
        .background_gradient(cmap=sns.light_palette("green", as_cmap=True))

def pms(expenses):
    return 6 * expenses.mean() * -1


def pmr(expenses):
    return 12 * expenses.mean() * -1


def pi(expenses, age):
    return 0.1 * pmr(expenses) * age


def projected_return_for_year(invest, start_date, end_date):
    return summary(invest, start_date, end_date)['Return / Total'].mean() * 12


def pnif(expenses, projected_return_for_year):
    return pmr(expenses) / projected_return_for_year


def total(invest, base_date):
    return tt.invested_for_month_by('title', invest, base_date).sum()


def age(birth_year):
    return date.today().year - birth_year


def goals(expenses, invest, start_date, base_date, birth_year):
    """Returns table with summary for assets goal, considering (PMS, PMR, PI, PNIF).

    expenses: list of expenses (will consider all records, if need for a month,
    pass expenses for the month)
    invest: list of investments
    start_date: when will the analysis start (this is used by annualized return)
    base_date: date which these goals are being analysed. If passed previous month
    will return a snapshot for this goals in the previous month
    birth_year: important to compute age and pass to PI metric
    """
    return pd.DataFrame([pms(expenses),
                         pmr(expenses),
                         pi(expenses, age(birth_year)),
                         pnif(expenses, annualized_return(invest, start_date, base_date)),
                         total(invest, base_date)], index=['PMS', 'PMR', 'PI', 'PNIF', 'Total'])


def style_goals(assets_goals):
    threshold = assets_goals.loc['Total', 'amount']
    return assets_goals.style\
        .format({'amount': fmt.BR_CURRENCY_FORMAT})\
        .applymap(fmt.green_background_threshold(threshold))


def annualized_return(invest, start_date, end_date):
    """https://www.fool.com/knowledge-center/how-to-calculate-a-monthly-return-on-investment.aspx"""
    return ((1 + summary(invest, start_date, end_date)['Return / Total'].mean()) ** 12) - 1


def investment_goals(incomes, invest_goals):
    total_invested = tt.total_invested_by('goal', incomes)
    return total_invested\
        .join(pd.DataFrame.from_dict(invest_goals, orient='index', columns=['goals']))


def investment_goals_plot(invest_goals):
    bar_x = list(invest_goals.index)

    fig = go.Figure(data=[
        go.Bar(name='Goal', x=bar_x, y=invest_goals.goals.values),
        go.Bar(name='Invested', x=bar_x, y=invest_goals.amount.values)
    ], layout=defaults.layout(yaxis={'type': 'log'}, height=400))

    iplot(fig)
