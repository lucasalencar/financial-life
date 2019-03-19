import pandas as pd
import seaborn as sns
import record_summary as rs
import formatting as fmt

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
