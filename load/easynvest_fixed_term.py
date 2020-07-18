import pandas as pd
import record_summary as rs


def add_amount(easynvest):
    easynvest['amount'] = easynvest['gross amount'].map(lambda amount:
                                                        amount
                                                        .replace('R$', '')
                                                        .replace('.', '')
                                                        .replace(',', '.')).astype(float)
    return easynvest


def add_accounts(easynvest):
    account_mapping = {
        'CDB Banco Indusval':        'Magnetis',
        'CDB Voiter Banco Indusval': 'Magnetis',
        'CDB Banco Maxima':          'Magnetis',
        'LCA Banco Maxima':          'Magnetis',
        'LCI Banco Maxima':          'Magnetis',
    }

    easynvest['account'] = easynvest.title.apply(lambda row:
                                                 account_mapping[row])
    return easynvest


def add_goals(easynvest):
    goals_mapping = {
        'CDB Banco Indusval':        'Aposentadoria',
        'CDB Voiter Banco Indusval': 'Aposentadoria',
        'CDB Banco Maxima':          'Aposentadoria',
        'LCA Banco Maxima':          'Aposentadoria',
        'LCI Banco Maxima':          'Aposentadoria',
    }

    easynvest['goal'] = easynvest.title.apply(lambda row: goals_mapping[row])
    return easynvest


def preprocess(easynvest):
    # Select fixed term investments
    fixed_term = easynvest[easynvest.type.isin(['LCA', 'LCI', 'CDB'])].copy()
    # Fix description to first letter capitalized
    fixed_term['description'] = fixed_term.description.str.title()
    # Add title based on type and description
    fixed_term['title'] = fixed_term.type + ' ' + fixed_term.description
    fixed_term = add_accounts(fixed_term)
    fixed_term = add_goals(fixed_term)
    return fixed_term

