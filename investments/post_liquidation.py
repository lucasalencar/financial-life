import pandas as pd
from investments import totals as tt


def liquidations(incomes):
    applications = tt.total_applications_by('title', incomes)
    return applications[applications.amount <= 0]


def liquidations_incomes(incomes):
    finished = liquidations(incomes).reset_index().title
    return incomes[incomes.title.isin(list(finished))]


def final_return(incomes):
    applications = tt.total_applications_by('title', incomes[incomes.amount > 0])
    liquidation_titles = tt.total_income_by('title', incomes)
    discounts = tt.total_discounts_by('title', incomes)
    net_return = liquidation_titles\
        .sub(applications, fill_value=0)\
        .add(discounts, fill_value=0)
    net_return_percentage = net_return.div(applications)

    data = {
        'Applications': applications,
        'Liquidations': liquidation_titles,
        'Discounts': discounts,
        'Net return': net_return,
        'Net return (%)': net_return_percentage,
    }

    final_returns = pd.concat(data.values(), axis=1, sort=False)
    final_returns.columns = data.keys()
    return final_returns.fillna(0)
