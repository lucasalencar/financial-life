"""
Helper functions to preprocess incomes and expenses data
"""
import pandas as pd


def export_to_sheets(expenses, filepath):
    expenses_to_export = expenses.copy()
    expenses_to_export['date'] = expenses['date'].dt.strftime("%m/%Y")
    expenses_to_export.sort_values(by=['date'], inplace=True)
    expenses_to_export.to_csv(filepath + '/expenses.csv', index=False)


def export_raw_expenses(expenses, filepath):
    expenses_to_export = expenses.copy()
    expenses_to_export.sort_values(by=['date'], inplace=True)
    expenses_to_export.to_csv(filepath + '/raw_expenses.csv', index=False)
