# pylint: disable=C0111

import pandas as pd
import seaborn as sns
import formatting as fmt
import record_summary as rs

from investments import totals as tt


def style_assets_goals(assets_goals, assets_thresh):
    return assets_goals.style\
        .format({'amount': fmt.BR_CURRENCY_FORMAT})\
        .applymap(fmt.green_background_threshold(assets_thresh))
