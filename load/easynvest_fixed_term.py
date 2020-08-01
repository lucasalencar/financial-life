import pandas as pd
import record_summary as rs


def add_amount(easynvest):
    easynvest['amount'] = easynvest['gross amount'].map(lambda amount:
                                                        amount
                                                        .replace('R$', '')
                                                        .replace('.', '')
                                                        .replace(',', '.')).astype(float)
    return easynvest


def add_title(fixed_term):
    # Fix description to first letter capitalized
    fixed_term['description'] = fixed_term.description.str.title()
    # Add title based on type and description
    fixed_term['title'] = fixed_term.type + ' ' + fixed_term.description + ' ' + fixed_term['index']
    renamings = {
        'CDB Voiter Banco Indusval 130% do CDI': 'CDB Banco Indusval',
        'CDB Banco Indusval 130% do CDI': 'CDB Banco Indusval',
        'CDB Banco Maxima 107% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 114% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 116% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 117% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 119% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 120% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 124% do CDI': 'CDB Banco Maxima',
        'CDB Banco Maxima 128% do CDI': 'CDB Banco Maxima',
        'LCI Banco Maxima 107% do CDI': 'LCI Banco Maxima',
        'LCA Banco Maxima 100% do CDI': 'LCA Banco Maxima',
        'LCA Banco Maxima 101% do CDI': 'LCA Banco Maxima',
    }
    return fixed_term.replace(renamings)


def add_accounts(easynvest):
    account_mapping = {
        'CDB Banco Indusval':        'Magnetis',
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
        'CDB Banco Maxima':          'Aposentadoria',
        'LCA Banco Maxima':          'Aposentadoria',
        'LCI Banco Maxima':          'Aposentadoria',
    }

    easynvest['goal'] = easynvest.title.apply(lambda row: goals_mapping[row])
    return easynvest


def preprocess(easynvest):
    # Select fixed term investments
    fixed_term = easynvest[easynvest.type.isin(['LCA', 'LCI', 'CDB'])].copy()
    fixed_term = add_title(fixed_term)
    fixed_term = add_accounts(fixed_term)
    fixed_term = add_goals(fixed_term)
    return fixed_term

