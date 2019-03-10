"""Plot expenses summary over time"""

from plotly.offline import iplot
import plotly.graph_objs as go

def plot(monthly_exp):
    """Plot over time"""
    return iplot([
        go.Scatter(
            x=monthly_exp.index,
            y=monthly_exp['Expenses'] * -1,
            name='Expenses',
            line=dict(color='red')
        ),
        go.Scatter(
            x=monthly_exp.index,
            y=monthly_exp['Incomes'],
            name='Incomes',
            line=dict(color='green')
        ),
        go.Scatter(
            x=monthly_exp.index,
            y=monthly_exp['Balance'],
            name='Balance',
            line=dict(color='blue')
        )
    ])
