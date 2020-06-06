import pandas as pd
import record_summary as rs


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


def add_amount(data):
    data['amount'] = data['gross amount'].map(lambda amount:
                                              amount
                                              .replace('R$', '')
                                              .replace('.', '')
                                              .replace(',', '.')).astype(float)
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
        'TARPON GT FIC FIA':                           'Easynvest',
        'BRAX11':                                      'Magnetis',
    }
    data['account'] = data.description.apply(lambda row: account_mapping[row])
    return data


def add_goals(data):
    goals_mapping = {
        'Brasil Plural Yield Fundo de Investimento Renda Fixa Referen': 'Aposentadoria',
        'Magnetis Diversificação Ações':                                'Aposentadoria',
        'Magnetis Diversificação Multimercados':                        'Aposentadoria',
        'Magnetis Diversificação Renda Fixa':                           'Aposentadoria',
        'TARPON GT FIC FIA':                                            'Aposentadoria',
        'BRAX11':                                                       'Aposentadoria',
    }
    data['goals'] = data.title.apply(lambda row: goals_mapping[row])
    return data


def preprocess(data):
    # Select only funds and stocks
    funds = data[data.type.isin(['Fundos de investimentos', 'Ações'])].copy()
    funds = add_title(funds)
    funds = add_amount(funds)
    funds = add_type(funds)
    # Sum total amont by date, title and type
    funds = rs.total_amount_by(['date', 'title', 'type'], funds).reset_index()
    funds['category'] = 'valor aplicado'
    funds = add_goals(funds)
    return funds
