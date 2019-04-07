import pandas as pd
import seaborn as sns
import record_summary as rs
import formatting as fmt

from datetime import date
from investments import totals as tt

def summary(invest):
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
    return assets_summary


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Applications / Total': fmt.PERC_FORMAT
}


def style_summary(summary):
    cm = sns.light_palette("green", as_cmap=True)
    background_subset = pd.IndexSlice['2018-02':, ['Total',
                                                   'Return',
                                                   'Return / Total',
                                                   'Applications',
                                                   'Applications / Total']]

    return summary.style\
        .format(ASSETS_SUMMARY_COLS_FORMAT)\
        .background_gradient(cmap=cm, subset=background_subset)

def pms(expenses):
    return 6 * expenses.mean() * -1


def pmr(expenses):
    return 12 * expenses.mean() * -1


def pi(expenses, age):
    return 0.1 * pmr(expenses) * age


## TODO Add annualized return according to this article
## https://www.fool.com/knowledge-center/how-to-calculate-a-monthly-return-on-investment.aspx
def annualized_return(invest, start_date, end_date):
    return summary(invest).loc[start_date:end_date, 'Return / Total'].mean() * 12


def pnif(expenses, annualized_return):
    return pmr(expenses) / annualized_return


def total(invest, base_date):
    return tt.invested_for_month_by('title', invest, base_date).sum()


def age(birth_year):
    return date.today().year - birth_year


def goals(expenses, invest, base_date, birth_year):
    return pd.DataFrame([pms(expenses),
                         pmr(expenses),
                         pi(expenses, age(birth_year)),
                         pnif(expenses, annualized_return(invest,
                                                          '2018-04',
                                                          base_date.strftime('%Y-%m'))),
                         total(invest, base_date)], index=['PMS', 'PMR', 'PI', 'PNIF', 'Total'])


def style_goals(assets_goals, assets_thresh):
    return assets_goals.style\
        .format({'amount': fmt.BR_CURRENCY_FORMAT})\
        .applymap(fmt.green_background_threshold(assets_thresh))
