import pandas as pd
import numpy as np
def reduce_memory_usage(df:pd.DataFrame, verbose:bool=True) -> pd.DataFrame:
    """Function to reduce the memory usage of a dataframe.

    Will reduce numerics' (integer and float) memory usage significantly while not decreasing overall model fit much, if at all.

    Args:
    1. df (pd.DataFrame): Pandas DataFrame.
    2. verbose (bool): Flag to make the result more verbose than normal.

    Returns the given dataframe with its numeric columns transformed to reduce memory.
    """
    numerics = ["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
    if isinstance(df, pd.Series):
        start_mem = df.memory_usage() / 1024 ** 2
    else:
        start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if (
                    c_min > np.finfo(np.float16).min
                    and c_max < np.finfo(np.float16).max
                ):
                    df[col] = df[col].astype(np.float16)
                elif (
                    c_min > np.finfo(np.float32).min
                    and c_max < np.finfo(np.float32).max
                ):
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    if isinstance(df, pd.Series):
        end_mem = df.memory_usage() / 1024 ** 2
    else:
        end_mem = df.memory_usage().sum() / 1024 ** 2

    if verbose:
        print(
            "Mem. usage decreased to {:.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df

