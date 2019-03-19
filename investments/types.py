import plotly.graph_objs as go
from plotly.offline import iplot

from investments import totals as tt
from plotting import defaults
import record_summary as rs

def describe(invest, base_date):
    """Returns relevant data about types"""
    current_month = rs.records_for_month(invest, base_date)
    invested_by_type = tt.total_invested_by('type', current_month)
    return (invested_by_type / invested_by_type.sum()).sort_values('amount')


def plot(invest, base_date, **configs):
    """Plots pie chart with types distribution"""
    by_type = describe(invest, base_date)
    data = [go.Pie(labels=by_type.index, values=by_type.amount)]
    return iplot(defaults.figure(data, height=400, **configs))
