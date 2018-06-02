import pandas as pd
import formatting as fmt


def amount_by_month(data):
    return data.groupby(data['date'].dt.strftime("%Y-%m")).amount.sum().to_frame()


def balance(expense, income):
    """Computes balance based on expenses and incomes.
    Returns balance and its percentage."""
    balance_val = income + expense
    balance_perc = balance_val / income
    return [balance_val, balance_perc]


def summary_expenses(expenses, incomes):
    """Builds a Dataframe with the expenses,
    incomes, balance and balance percentage."""
    balance_val, balance_perc = balance(expenses, incomes)
    summary_exp = pd.concat([expenses, incomes, balance_val, balance_perc], axis=1).dropna()
    summary_exp.columns = ['Expenses', 'Incomes', 'Balance', 'Balance (%)']
    return summary_exp


MONTHLY_COST_COLS_FORMAT = {
    'Expenses': fmt.BR_CURRENCY_FORMAT,
    'Incomes': fmt.BR_CURRENCY_FORMAT,
    'Balance': fmt.BR_CURRENCY_FORMAT,
    'Balance (%)': fmt.PERC_FORMAT
}


def style_summary_expenses(summary, balance_goal):
    return summary.style\
        .format(MONTHLY_COST_COLS_FORMAT)\
        .applymap(fmt.amount_color, subset=['Expenses', 'Incomes'])\
        .applymap(fmt.red_to_green_background(balance_goal), subset=['Balance (%)'])


def total_amount_by_category(records):
    return records.groupby('category').sum().sort_values('amount')


def expenses_distribution(expenses):
    total_expenses_by_category = total_amount_by_category(expenses)
    total_expenses_by_category = total_expenses_by_category[total_expenses_by_category.amount < 0]
    total_spent_on_month = expenses.amount.sum()
    return total_expenses_by_category / total_spent_on_month
