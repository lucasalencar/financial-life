import pandas as pd
import record_summary as rs
import date_helpers

from investments import filters

def add_title(data):
    title_mapping = {
        'BRASIL PLURAL YIELD FIRF REFERENCIADO DI':    'Brasil Plural Yield Fundo de Investimento Renda Fixa Referen',
        'MAGNETIS DIVERSIFICAÇÃO AÇÕES FI':            'Magnetis Diversificação Ações',
        'MAGNETIS DIVERSIFICAÇÃO MULTIMERCADO FIC FI': 'Magnetis Diversificação Multimercados',
        'MAGNETIS DIVERSIFICAÇÃO RF FIC CP':           'Magnetis Diversificação Renda Fixa',
        'Magnetis Diversif RF FIC CP':                 'Magnetis Diversificação Renda Fixa',
        'TARPON GT FIC FIA':                           'TARPON GT FIC FIA',
        'BRAX11':                                      'BRAX11',
    }
    data['title'] = data.description.apply(lambda row: title_mapping[row])
    return data


def add_type(data):
    type_mapping = {
        'BRASIL PLURAL YIELD FIRF REFERENCIADO DI':    'Fundos DI',
        'MAGNETIS DIVERSIFICAÇÃO AÇÕES FI':            'Fundos Ações',
        'MAGNETIS DIVERSIFICAÇÃO MULTIMERCADO FIC FI': 'Fundos Multimercado',
        'MAGNETIS DIVERSIFICAÇÃO RF FIC CP':           'Fundos Renda Fixa',
        'Magnetis Diversif RF FIC CP':                 'Fundos Renda Fixa',
        'TARPON GT FIC FIA':                           'Fundos Ações',
        'BRAX11':                                      'Ações',
    }
    data['type'] = data.description.apply(lambda row: type_mapping[row])
    return data


def add_account(data):
    account_mapping = {
        'BRASIL PLURAL YIELD FIRF REFERENCIADO DI':    'Magnetis',
        'MAGNETIS DIVERSIFICAÇÃO AÇÕES FI':            'Magnetis',
        'MAGNETIS DIVERSIFICAÇÃO MULTIMERCADO FIC FI': 'Magnetis',
        'MAGNETIS DIVERSIFICAÇÃO RF FIC CP':           'Magnetis',
        'Magnetis Diversif RF FIC CP':                 'Magnetis',
        'TARPON GT FIC FIA':                           'Easynvest',
        'BRAX11':                                      'Magnetis',
    }
    data['account'] = data.description.apply(lambda row: account_mapping[row])
    return data


def add_goals(data):
    goals_mapping = {
        'BRASIL PLURAL YIELD FIRF REFERENCIADO DI':    'Aposentadoria',
        'MAGNETIS DIVERSIFICAÇÃO AÇÕES FI':            'Aposentadoria',
        'MAGNETIS DIVERSIFICAÇÃO MULTIMERCADO FIC FI': 'Aposentadoria',
        'MAGNETIS DIVERSIFICAÇÃO RF FIC CP':           'Aposentadoria',
        'Magnetis Diversif RF FIC CP':                 'Aposentadoria',
        'TARPON GT FIC FIA':                           'Aposentadoria',
        'BRAX11':                                      'Aposentadoria',
    }
    data['goal'] = data.description.apply(lambda row: goals_mapping[row])
    return data


def normalize_amount(data, column):
    data['amount'] = data[column]\
        .dropna()\
        .map(lambda amount:
             amount
             .replace('R$', '')
             .replace('.', '')
             .replace(',', '.')).astype(float)
    return data


def preprocess_invested(funds):
    funds = normalize_amount(funds, 'gross amount')
    funds = rs.total_amount_by(['date', 'title', 'type', 'account', 'goal'], funds).reset_index()
    funds['category'] = 'valor aplicado'
    return funds


APPLICATIONS_GROUPBY = ['title', 'type', 'account', 'goal']


def compute_applications(data, base_date):
    previous_month_data = rs.records_for_month(data,
                                               date_helpers.previous_month(base_date))
    current_month_data = rs.records_for_month(data, base_date)
    difference = rs.total_amount_by(APPLICATIONS_GROUPBY,
                                    current_month_data) - rs.total_amount_by(APPLICATIONS_GROUPBY,
                                                                             previous_month_data)
    return difference.amount


def preprocess_applications(funds):
    funds = normalize_amount(funds, 'application')
    funds = rs.total_amount_by(['date', 'title', 'type', 'account', 'goal'], funds).reset_index()
    funds = rs.describe_over_time(funds, compute_applications)\
        .transpose()\
        .reset_index()\
        .melt(id_vars=APPLICATIONS_GROUPBY,
              var_name='date',
              value_name='amount')

    # Fix date to be in the beginning of month
    funds['date'] = pd.to_datetime(funds.date
                                   .map(lambda d:
                                        date_helpers.beginning_of_month(rs.month_to_date(d))))
    funds['category'] = 'aplicação'

    # Remove first month because there is no record for its previous month
    funds = funds[funds.date > funds.date.min()]
    return funds


def compute_liquidations(row, invested):
    begin, end = date_helpers.month_day_range(date_helpers.previous_month(row.date))
    amount = invested[(invested.date >= pd.Timestamp(begin)) &
                      (invested.date <= pd.Timestamp(end)) &
                      (invested.title == row.title)].amount
    return amount * -1


def preprocess_liquidations(funds):
    applications = filters.applications(funds)
    invested = filters.invested(funds)
    liquidations = applications[applications.amount.isna()].copy()
    liquidations['amount'] = liquidations.apply(lambda row: compute_liquidations(row, invested), axis=1)
    return liquidations


def preprocess(data):
    # Select only funds and stocks
    funds = data[data.type.isin(['Fundos de investimentos', 'Ações'])].copy()

    # Add new columns
    funds = add_title(funds)
    funds = add_type(funds)
    funds = add_account(funds)
    funds = add_goals(funds)

    content = [
        preprocess_invested(funds),
        preprocess_applications(funds),
    ]
    funds = pd.concat(content, sort=False)
    funds = pd.concat([funds, preprocess_liquidations(funds)], sort=False)
    return funds.dropna()
