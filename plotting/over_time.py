"""Functions to plot data over time iteractivily"""

import plotly.graph_objs as go
from plotly.offline import iplot
from plotting import defaults

def plot(data, **configs):
    """
    Plots DataFrame over time, considering index as time spans and column will represent lines.
    """
    to_plot = data.apply(
        lambda column: go.Scatter(
            x=column.index,
            y=column,
            name=column.name
        )
    )
    return iplot(defaults.figure(list(to_plot), **configs))
