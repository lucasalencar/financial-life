import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot

import formatting as fmt
import record_summary as rs


def expenses_by_month(expenses):
    return rs.total_amount_by(rs.groupby_month(expenses), expenses)


def incomes_by_month(incomes):
    income_salary = incomes[incomes.category == 'renda'][['date', 'amount']]
    return rs.total_amount_by(rs.groupby_month(income_salary), income_salary)


def balance(expense, income):
    """Computes balance based on expenses and incomes.
    Returns balance and its percentage."""
    balance_val = income + expense
    balance_perc = balance_val / income
    return [balance_val, balance_perc]


def summary(expenses, incomes):
    """Builds a Dataframe with the expenses,
    incomes, balance and balance percentage."""
    balance_val, balance_perc = balance(expenses, incomes)
    summary_exp = pd.concat([expenses, incomes, balance_val, balance_perc], axis=1, sort=False)
    summary_exp.columns = ['Expenses', 'Incomes', 'Balance', 'Balance (%)']
    return summary_exp.dropna().sort_index()


def month_by_month_summary(expenses, incomes):
    return summary(expenses_by_month(expenses), incomes_by_month(incomes))


def avg_month_summary(expenses, incomes):
    avg_monthly_exp = summary(expenses_by_month(expenses).mean(),
                              incomes_by_month(incomes).mean())
    avg_monthly_exp.index = ['Average monthly expenses']
    return avg_monthly_exp


MONTHLY_COST_COLS_FORMAT = {
    'Expenses': fmt.BR_CURRENCY_FORMAT,
    'Incomes': fmt.BR_CURRENCY_FORMAT,
    'Balance': fmt.BR_CURRENCY_FORMAT,
    'Balance (%)': fmt.PERC_FORMAT
}


def style_summary(summary, balance_goal):
    return summary.style\
        .format(MONTHLY_COST_COLS_FORMAT)\
        .applymap(fmt.amount_color, subset=['Expenses', 'Incomes'])\
        .applymap(fmt.red_to_green_background(balance_goal), subset=['Balance (%)'])


def plot(monthly_exp):
    """Plot expenses summary over time"""
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
