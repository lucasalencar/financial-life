import pandas as pd
import numpy as np
import seaborn
import formatting as fmt
import record_summary as rs


def expense_distribution(expenses, denominator):
    denominator_sum = denominator.amount.sum()
    expenses_by_category = rs.total_amount_by('category', expenses).sort_values('amount')
    return expenses_by_category / denominator_sum


def describe_expenses(expenses, incomes):
    expenses_by_category = rs.total_amount_by('category', expenses)
    dist_by_spent = expense_distribution(expenses, expenses)
    dist_by_income = expense_distribution(expenses,
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


def style_expenses_distribution(dist):
    return dist.style.format(EXPENSES_DISTRIBUTION_COLS_FORMAT)


def _expenses_over_time_(expenses, incomes, post_describe_fn):
    """Computes expenses distribution over time, for all months available in expenses"""
    return rs.describe_over_time(expenses,
                              lambda exps, date: post_describe_fn(
                                  describe_expenses(rs.records_for_month(expenses, date),
                                                    rs.records_for_month(incomes, date))))


def expenses_over_time(expenses, incomes, column):
    """Computes expenses distribution over time, for all months available in expenses"""
    post_describe_fn = None
    if column == 'amount #':
        post_describe_fn = lambda x: x['amount #'] * -1
    else:
        post_describe_fn = lambda x: x[column]
    return _expenses_over_time_(expenses, incomes, post_describe_fn)
