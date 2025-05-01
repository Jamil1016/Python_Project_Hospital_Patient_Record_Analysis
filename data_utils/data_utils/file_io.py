import os
import glob
import shutil
import pandas as pd
from pathlib import Path

#########################################################################################################

def load_files(folder_path, file_names, file_type='csv', delimiter=None):
    """
    Load multiple files (CSV, TSV, Excel, JSON) into a dictionary of DataFrames.

    Args:
        folder_path (str or Path): The directory where files are located.
        file_names (list of str): List of filenames (without extension).
        file_type (str): Type of file to load: 'csv', 'tsv', 'xlsx', 'xls', 'json'.
        delimiter (str, optional): For custom-delimited files (e.g., CSV, TSV).

    Returns:
        dict: A dictionary where keys are filenames and values are pandas DataFrames.
    """
    folder = Path(folder_path)
    dfs = {}

    for name in file_names:
        filepath = folder / f"{name}.{file_type}"

        if file_type == 'csv':
            df = pd.read_csv(filepath, delimiter=delimiter or ',')
        elif file_type == 'tsv':
            df = pd.read_csv(filepath, delimiter=delimiter or '\t')
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(filepath)
        elif file_type == 'json':
            df = pd.read_json(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        dfs[name] = df

    return dfs

#########################################################################################################

def merge_files(folder_path, file_type='csv', delimiter=None):
    """
    Merges multiple files of a given type from a folder into a single pandas DataFrame.

    Args:
        folder_path (str): Path to the folder containing the files.
        file_type (str): Type of files to merge ('csv', 'tsv', 'xlsx', 'xls', 'json').
        delimiter (str, optional): For CSV/TSV files. Overrides default separator.

    Returns:
        pandas.DataFrame: A combined DataFrame of all files.
    """
    folder = Path(folder_path)
    all_dfs = []

    # Set file pattern
    pattern = f"*.{file_type.lower()}"

    # Detect separator
    sep = delimiter if delimiter else (',' if file_type == 'csv' else '\t')

    for filename in glob.glob(str(folder / pattern)):
        try:
            if file_type == 'csv' or file_type == 'tsv':
                df = pd.read_csv(filename, sep=sep)
            elif file_type in ['xlsx', 'xls']:
                df = pd.read_excel(filename)
            elif file_type == 'json':
                df = pd.read_json(filename)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            all_dfs.append(df)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()  # return empty DataFrame if no files found or loaded