"""Functions to plot data over time iteractivily"""

from plotly.offline import iplot
import plotly.graph_objs as go

def default_layout(margin_bottom=25, margin_top=35, height=300, **configs):
    """
    Default layout that describes how graphic looks like.
    Useful named arguments:
      - title: str
      - width: int
      - height: int
    """
    return go.Layout(
        margin=go.layout.Margin(b=margin_bottom, t=margin_top),
        height=height,
        **configs
    )

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

    fig = go.Figure(
        data=list(to_plot),
        layout=default_layout(**configs)
    )
    return iplot(fig)
