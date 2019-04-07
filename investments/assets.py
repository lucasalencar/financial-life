import pandas as pd
import seaborn as sns
import record_summary as rs
import formatting as fmt

from datetime import date
from investments import totals as tt

def summary(invest, start_date, end_date):
    total = rs.describe_over_time(invest,
                                  lambda data, date:
                                  tt.invested_for_month_by('title', invest, date)
                                  .sum()).amount
    invest_return = rs.describe_over_time(invest,
                                          lambda data, date:
                                          tt.absolute_return_for_month(data, date)
                                          .sum()).amount
    applications = rs.describe_over_time(invest,
                                         lambda data, date:
                                         tt.applications_for_month(data, date)
                                         .sum()).amount

    summary = {'Total': total,
               'Return': invest_return,
               'Return / Total': invest_return / total,
               'Applications': applications,
               'Applications / Total': applications / total}

    assets_summary = pd.DataFrame(summary, columns=list(summary.keys()))
    return assets_summary.loc[start_date.strftime('%Y-%m'):end_date.strftime('%Y-%m')]


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Applications / Total': fmt.PERC_FORMAT
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


## TODO Add annualized return according to this article
## https://www.fool.com/knowledge-center/how-to-calculate-a-monthly-return-on-investment.aspx
def annualized_return(invest, start_date, end_date):
    return summary(invest, start_date, end_date)['Return / Total'].mean() * 12


def pnif(expenses, annualized_return):
    return pmr(expenses) / annualized_return


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
