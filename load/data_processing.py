"""
Helpers to preprocess data
"""

def convert_categories(expenses, category_conversion_hash):
    return expenses.category\
        .apply(lambda x: x.lower())\
        .replace(category_conversion_hash)
