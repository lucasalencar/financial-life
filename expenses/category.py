import pandas as pd

import formatting as fmt
import record_summary as rs


def distribution_by_category(expenses, denominator):
    denominator_sum = denominator.amount.sum()
    expenses_by_category = rs.total_amount_by('category', expenses).sort_values('amount')
    return expenses_by_category / denominator_sum


def distribution(expenses, incomes):
    expenses_by_category = rs.total_amount_by('category', expenses)
    dist_by_spent = distribution_by_category(expenses, expenses)
    dist_by_income = distribution_by_category(expenses,
                                              incomes[incomes.category == 'renda']) * -1

    return pd.DataFrame({'amount #': expenses_by_category.amount,
                         '% by expenses': dist_by_spent.amount,
                         '% by income': dist_by_income.amount},
                        columns=['amount #', '% by expenses', '% by income']).sort_values('amount #')


EXPENSES_DISTRIBUTION_COLS_FORMAT = {
    'amount #': fmt.BR_CURRENCY_FORMAT,
    '% by expenses': fmt.PERC_FORMAT,
    '% by income': fmt.PERC_FORMAT
}


def style_distribution(dist):
    return dist.style.format(EXPENSES_DISTRIBUTION_COLS_FORMAT)


def display_expenses(expenses, category):
    from IPython.display import display
    print("Expenses in category", category)
    display(expenses[expenses.category == category].sort_values('amount'))


def describe_over_time(expenses, incomes, post_describe_fn):
    """Computes expenses distribution over time, for all months available in expenses"""
    return rs.describe_over_time(expenses,
                              lambda exps, date: post_describe_fn(
                                  distribution(rs.records_for_month(expenses, date),
                                               rs.records_for_month(incomes, date))))


def over_time(expenses, incomes, column):
    """Computes expenses distribution over time, for all months available in expenses"""
    post_describe_fn = None
    if column == 'amount #':
        post_describe_fn = lambda x: x['amount #'] * -1
    else:
        post_describe_fn = lambda x: x[column]
    return describe_over_time(expenses, incomes, post_describe_fn)


def food_expenses(expenses, base_date):
    data = rs.total_amount_by('category', rs.records_for_month(expenses, base_date))
    if 'mercado' in data.index and 'restaurante' in data.index:
        return pd.Series(data.loc['mercado'].amount + data.loc['restaurante'].amount) * -1
    else:
        return pd.Series(0)


def add_food_expenses(expenses, over_time_data):
    clone_data = over_time_data.copy()
    clone_data['alimentação'] = rs.describe_over_time(expenses, food_expenses)
    return clone_data
