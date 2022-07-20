#!/usr/bin/env python3


def total_amount_by(groupby, records):
    """Sums total amount given a column to group by"""
    return records.groupby(groupby).sum()

