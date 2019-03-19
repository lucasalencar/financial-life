# pylint: disable=C0111

import pandas as pd
import seaborn as sns
import formatting as fmt
import record_summary as rs

from investments import totals as tt


ASSETS_SUMMARY_COLS_FORMAT = {
    'Total': fmt.BR_CURRENCY_FORMAT,
    'Return': fmt.BR_CURRENCY_FORMAT,
    'Return / Total': fmt.PERC_FORMAT,
    'Applications': fmt.BR_CURRENCY_FORMAT,
    'Applications / Total': fmt.PERC_FORMAT
}


def summary_assets(invest):
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
