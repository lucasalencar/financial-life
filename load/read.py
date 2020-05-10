"""
Helper functions to read files from data folder
"""
import glob
import os
import pandas as pd


def list_all_files_for(filepath, file_pattern):
    """List all files given a path and a regex pattern"""
    full_pattern = os.path.join(filepath, file_pattern)
    all_files = glob.glob(full_pattern)
    if not all_files:
        print("WARNING: No files found with pattern %s" % full_pattern)
    return all_files


def read_all_csv_for(filenames, **opts):
    """Read all csvs listed into a DataFrame"""
    all_dfs = [pd.read_csv(filename, **opts) for filename in filenames]
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True, sort=False)
    return None


def read_all_csv_found(filepath, filename_pattern):
    """Reads all files content given a filname pattern and
    joins all of them into a single DataFrame"""
    all_files = list_all_files_for(filepath, filename_pattern)
    return read_all_csv_for(all_files)


def read_first_csv_found(filepath, file_pattern):
    """Read content of the first file found given a regex pattern"""
    found_files = list_all_files_for(filepath, file_pattern)
    if found_files:
        return pd.read_csv(found_files[0])
    return None
