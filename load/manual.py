"""
All functions necessary to load manual expenses entries
"""
from load import read


def load(file_pattern=None, data_path=None, **configs):
    return read.read_first_file_found(data_path, file_pattern)
