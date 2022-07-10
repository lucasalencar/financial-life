"""Functions with default configs for plotly plots"""
import plotly.graph_objs as go

def layout(margin_bottom=25, margin_top=35, height=300, **configs):
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
        hovermode='x',
        **configs
    )

def figure(data, **configs):
    """Defatul figure that get default layout"""
    return go.Figure(
        data=data,
        layout=layout(**configs)
    )
