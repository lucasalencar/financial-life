"""Pie plot related functions"""

import plotly.graph_objs as go
from plotly.offline import iplot

from . import defaults


def plot(series, **configs):
    """Pie plot given a series"""
    plot_data = [go.Pie(labels=series.index, values=series.values)]
    return iplot(defaults.figure(plot_data, **configs))
