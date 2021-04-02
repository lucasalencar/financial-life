import pandas as pd
import record_summary as rs
import date_helpers

from investments import filters

TITLES_TABLE = {
    'Brasil Plural Yield Fundo de Investimento Renda Fixa Referen': {
        'type': 'Fundos DI',
        'account': 'Magnetis',
        'goal': 'Aposentadoria',
    },
    'Magnetis Diversificação Ações': {
        'type': 'Fundos Ações',
        'account': 'Magnetis',
        'goal': 'Aposentadoria',
    },
    'Magnetis Diversificação Multimercados': {
        'type': 'Fundos Multimercado',
        'account': 'Magnetis',
        'goal': 'Aposentadoria',
    },
    'Magnetis Diversificação Renda Fixa': {
        'type': 'Fundos Renda Fixa',
        'account': 'Magnetis',
        'goal': 'Aposentadoria',
    },
    'TARPON GT FIC FIA': {
        'type': 'Fundos Ações',
        'account': 'Easynvest',
        'goal': 'Aposentadoria',
    },
    'BRAX11': {
        'type': 'ETF',
        'account': 'Magnetis',
        'goal': 'Aposentadoria',
    },
    'GTWR11': {
        'type': 'Fundos Imobiliários',
        'account': 'Easynvest',
        'goal': 'Aposentadoria',
    },
    'BCFF11': {
        'type': 'Fundos Imobiliários',
        'account': 'Easynvest',
        'goal': 'Aposentadoria',
    },
    'IVVB11': {
        'type': 'ETF',
        'account': 'Easynvest',
        'goal': 'Aposentadoria',
    },
    'BOVA11': {
        'type': 'ETF',
        'account': 'Easynvest',
        'goal': 'Aposentadoria',
    },
    'SMAL11': {
        'type': 'ETF',
        'account': 'Easynvest',
        'goal': 'Aposentadoria',
    },
    'DISB34': {
        'type': 'BDR',
        'account': 'Easynvest',
        'goal': 'Experimento',
    },
    'MGLU3': {
        'type': 'Ações',
        'account': 'Easynvest',
        'goal': 'Experimento',
    },
}

def add_title(data):
    title_mapping = {
        'BRASIL PLURAL YIELD FIRF REFERENCIADO DI':    'Brasil Plural Yield Fundo de Investimento Renda Fixa Referen',
        'MAGNETIS DIVERSIFICAÇÃO AÇÕES FI':            'Magnetis Diversificação Ações',
        'Magnetis Diversif Ações FIA':                 'Magnetis Diversificação Ações',
        'MAGNETIS DIVERSIFICAÇÃO MULTIMERCADO FIC FI': 'Magnetis Diversificação Multimercados',
        'Magnetis Diversif FIM FIC':                   'Magnetis Diversificação Multimercados',
        'MAGNETIS DIVERSIFICAÇÃO RF FIC CP':           'Magnetis Diversificação Renda Fixa',
        'Magnetis Diversif RF FIC CP':                 'Magnetis Diversificação Renda Fixa',
        'Tarpon GT FIC FIA':                           'TARPON GT FIC FIA',
    }
    data['title'] = data.description.apply(lambda row: title_mapping.get(row, row))
    return data


def add_type(data):
    data['type'] = data.title.apply(lambda row: TITLES_TABLE[row]['type'])
    return data


def add_account(data):
    data['account'] = data.title.apply(lambda row: TITLES_TABLE[row]['account'])
    return data


def add_goals(data):
    data['goal'] = data.title.apply(lambda row: TITLES_TABLE[row]['goal'])
    return data


def preprocess(data):
    # Select only funds and stocks
    funds = data[data.type.isin(['Fundos de investimentos', 'Ações'])].copy()

    # Add new columns
    funds = add_title(funds)
    funds = add_type(funds)
    funds = add_account(funds)
    funds = add_goals(funds)
    return funds
