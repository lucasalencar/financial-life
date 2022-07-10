import pandas as pd
from . import totals as tt
from . import filters


def liquidations_incomes(incomes):
    finished = filters.liquidations(incomes).reset_index().title
    return incomes[incomes.title.isin(list(finished))]


def first_application_date(title, incomes):
    t = incomes[incomes.title == title]
    return t[t.category == 'aplicação'].sort_values('date').iloc[0].date


def liquidation_date(title, incomes):
    t = incomes[incomes.title == title]
    return t[t.category == 'renda'].sort_values('date').iloc[0].date


def application_months(title, incomes):
    application_time = liquidation_date(title, incomes) - first_application_date(title, incomes)
    return application_time.days / 30


def application_years(title, incomes):
    application_time = liquidation_date(title, incomes) - first_application_date(title, incomes)
    return application_time.days / 365


def applications_durations(liquidation_titles, incomes):
    durations = {'title': [], 'Duration months': [], 'Duration years': []}

    for title in liquidation_titles.index:
        durations['title'].append(title)
        durations['Duration months'].append(application_months(title, incomes))
        durations['Duration years'].append(application_years(title, incomes))

    return pd.DataFrame(durations).set_index('title')


def compute_net_return(liquidation_titles, applications, discounts):
    return liquidation_titles\
    .sub(applications, fill_value=0)\
    .add(discounts, fill_value=0)


def monthly_return(net_return, durations):
    return net_return.amount / durations['Duration months']


def yearly_return(net_return, durations):
    applicable_titles = durations[durations['Duration years'] > 1]
    return net_return.amount / applicable_titles['Duration years']


def final_return(incomes):
    applications = tt.total_applications_by('title', incomes[incomes.amount > 0])
    liquidation_titles = tt.total_income_by('title', incomes)
    discounts = tt.total_discounts_by('title', incomes)
    net_return = compute_net_return(liquidation_titles, applications, discounts)
    net_return_percentage = net_return.div(applications)
    durations = applications_durations(liquidation_titles, incomes)

    data = {
        'Applications': applications,
        'Liquidations': liquidation_titles,
        'Discounts': discounts,
        'Net return': net_return,
        'Net return (%)': net_return_percentage,
        'Duration months': durations['Duration months'],
        'Return a.m.': monthly_return(net_return, durations),
        'Duration years': durations['Duration years'],
        'Return a.y.': yearly_return(net_return, durations),
    }

    final_returns = pd.concat(data.values(), axis=1, sort=False)
    final_returns.columns = data.keys()
    return final_returns.fillna(0)
