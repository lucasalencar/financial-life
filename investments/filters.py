"""All filters used for investments"""


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
