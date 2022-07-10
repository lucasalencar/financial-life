"""
All functions necessary to load manual expenses entries
"""
from . import read


def load(file_pattern=None, data_path=None, **configs):
    return read.read_all_csv_found(data_path, file_pattern)
