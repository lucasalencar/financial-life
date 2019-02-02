"""
Helper functions to read files from data folder
"""
import glob
import os
import pandas as pd


def read_all_csvs(files_path, filename_pattern):
    """Reads all files content given a filname pattern and
    joins all of them into a single DataFrame"""
    full_pattern = os.path.join(files_path, filename_pattern)
    all_files = glob.glob(full_pattern)
    all_dfs = [pd.read_csv(filename) for filename in all_files]
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        print("WARNING: No files found with pattern %s" % full_pattern)
        return None


def read_first_file_found(filepath, file_pattern):
    """Read content of the first file found given a regex pattern"""
    full_pattern = os.path.join(filepath, file_pattern)
    found_files = glob.glob(full_pattern)
    if found_files:
        return pd.read_csv(found_files[0])
    else:
        print("WARNING: No files found with pattern %s" % full_pattern)
        return None
