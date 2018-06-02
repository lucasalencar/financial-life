def amount_by_month(data):
    """Sums amount grouping by Year-Month"""
    return data.groupby(data['date'].dt.strftime("%Y-%m")).amount.sum().to_frame()


def total_amount_by(groupby, records):
    """Sums total amount given a column to group by"""
    return records.groupby(groupby).sum().sort_values('amount')
