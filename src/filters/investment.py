"""All filters used for investments"""
from ..investments import totals


def f_invested(incomes):
    """Filter for invested values category"""
    return incomes.category == 'valor aplicado'


def invested(incomes):
    """Filters all invested values from incomes"""
    return incomes[f_invested(incomes)]


def f_applications(incomes):
    """Filter for applications category"""
    return incomes.category == 'aplicação'


def applications(incomes):
    """Filters all applications from incomes"""
    return incomes[f_applications(incomes)]


def f_income(incomes):
    """Filter for incomes/salary category"""
    return incomes.category == 'renda'


def income(incomes):
    """Filters all income from incomes"""
    return incomes[f_income(incomes)]


def f_discounts(incomes):
    """Filter for discounts category"""
    return incomes.category == 'desconto'


def discounts(incomes):
    """Filters all discounts from incomes"""
    return incomes[f_discounts(incomes)]


def liquidations(incomes):
    """Filters applications with amount lower than 0, i.e. liquidated investments"""
    total_applications = totals.total_applications_by('title', incomes)
    return total_applications[total_applications.amount <= 0]


def currently_invested_titles_by_type(invest, investment_types):
    """All investment titles currently invested filtered by type"""
    filtered_applications = applications(invest)
    titles = filtered_applications[filtered_applications.type.isin(investment_types)].title
    liquidated = liquidations(invest).reset_index().title
    return list(set(titles) - set(liquidated))
