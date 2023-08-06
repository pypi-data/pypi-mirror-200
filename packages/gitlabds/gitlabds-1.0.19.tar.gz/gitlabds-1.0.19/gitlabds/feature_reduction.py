import pandas as pd
import numpy as np

def drop_categorical(df:pd.DataFrame, inplace:bool=False) -> pd.DataFrame:

    """
    Drop all categorical columns from the dataframe. A useful step before regression modeling, as categorical variables are not used.
    
    Ex: gitlabds.drop_categorical(df, inplace=False):

    Parameters:


    df : your pandas dataframe

    inplace : Set to True to replace existing dataframe. Set to false to create a new one. Set to False to suppress


    Returns

    DataFrame with categorical columns dropped or None if inplace=True.
    """

    cats = list(df.select_dtypes(exclude="number"))
    print(f"Dropping {len(cats)} categorical columns: {cats}")

    if inplace == True:
        df.drop(columns=cats, inplace=True)

        return

    else:
        new_df = df.drop(columns=cats, inplace=False)

        return new_df


def remove_low_variation(df:pd.DataFrame=None, dv:str=None, columns:list="all", threshold:float=0.98, inplace:bool=False, verbose:bool=True) -> pd.DataFrame:

    """
    Remove columns from a dataset that do not meet the variation threshold. That is, columns will be dropped that contain a high percentage of one value.
    
    Ex: gitlabds.remove_low_variation(df=None, dv=None, columns='all', threshold=.98, inplace=False, verbose=True):

    Parameters:


    df : your pandas dataframe

    dv : The column name of your outcome. Entering your outcome variable in will prevent it from being removed due to low variation. May be left blank there is no outcome variable.

    columns : Will examine at all columns by default. To limit to just  a subset of columns, pass a list of column names.

    threshold: The maximum percentage one value in a column can represent. columns that exceed this threshold will be dropped. For example, the default value of 0.98 will drop any column where one value is present in more than 98% of rows.

    inplace : Set to True to replace existing dataframe. Set to false to create a new one. Set to False to suppress

    verbose : Set to True to print outputs of windsoring being done. Set to False to suppress.


    Returns

    DataFrame with low variation columns dropped or None if inplace=True.
    """

    print("\nRemoval of Low Variance Fields\n")

    if columns == "all":
        var_list = df.columns.tolist()
        print("\nWill examine all variables as candidate for removal")

    else:
        var_list = columns
        print(
            "\nWill examine the following variables as candidates for removal: {var_list}"
        )

    # Do not remove dv outcome
    if (dv != None) and (dv in var_list):
        var_list.remove(dv)

    removal_list = []

    # Loop through each column. This is slower than all at once but processing the entire df at once is very memory intensive
    for v in var_list:
        # Get levels of variable
        lvls = pd.DataFrame(df[v].value_counts(normalize=True, sort=True, ascending=False, dropna=False))

        # Select highest freq and drop if exceeds threshold
        if lvls.iloc[0][0] > threshold:

            if verbose == True:
                print(f"In field {v}, the value {lvls.index[0]} accounts for {lvls.iloc[0][0]*100}% of the values and the column will be dropped.")
                
            removal_list.append(v)

    print(f"{len(removal_list)} fields removed due to low variance")

    if removal_list:
        if inplace == True:

            df.drop(columns=removal_list, inplace=True)

            return

        else:
            
            new_df = df.drop(columns=removal_list, inplace=False)

            return new_df


def dv_proxies(df:pd.DataFrame, dv:str, threshold:float=0.8, inplace:bool=False) -> pd.DataFrame:

    """
    Remove columns that are highly correlated with the outcome (target) column.
    
    Ex: gitlabds.dv_proxies(df, dv, threshold=.8, inplace=False):

    Parameters:


    df : your pandas dataframe

    dv : The column name of your outcome.

    threshold : The Pearson's correlation value to the outcome above which columns will be dropped. For example, the default value of 0.80 will identify and drop columns that have correlations greater than 80% to the outcome.

    inplace : Set to True to replace existing dataframe. Set to false to create a new one. Set to False to suppress


    Returns

    DataFrame with outcome proxy columns dropped or None if inplace=True.
    """

    corrs = df.corr(method="pearson")[dv]
    corrs = pd.DataFrame(corrs.dropna().drop([dv], axis=0))
    corrs = corrs[corrs[dv] > threshold].index.to_list()

    print(corrs)

    if inplace == True:
        df.drop(columns=corrs, inplace=True)

        return

    else:
        new_df = df.drop(columns=corrs, inplace=False)

        return new_df


def correlation_reduction(df:pd.DataFrame=None, dv:str=None, threshold:float=0.90, inplace:bool=False, verbose:bool=True) -> pd.DataFrame:

    """
    Reduce the number of columns on a dataframe by dropping columns that are highly correlated with other columns. Note: only one of the two highly correlated columns will be dropped. uses Pearson's correlation coefficient.
    
    Ex: gitlabds.correlation_reduction(df=None, dv=None, threshold = 0.90, inplace=False, verbose=True):

    Parameters:


    df : your pandas dataframe

    dv : The column name of your outcome. Entering your outcome variable in will prevent it from being dropped. May be left blank there is no outcome variable.

    threshold: The threshold above which columns will be dropped. If two variables exceed this threshold, one will be dropped from the dataframe. For example, the default value of 0.90 will identify columns that have correlations greater than 90% to each other and drop one of those columns.

    inplace : Set to True to replace existing dataframe. Set to false to create a new one. Set to False to suppress

    verbose : Set to True to print outputs of windsoring being done. Set to False to suppress.


    Returns

    DataFrame with half of highly correlated columns dropped or None if inplace=True.
    """

    corrs = df.drop([dv], axis=1).corr()

    # Drop repeats by just selecting the upperhalf of the matrix
    upper = pd.DataFrame(np.triu(np.ones(corrs.shape)).astype("bool").reshape(corrs.size),columns=["to_keep"],)
    corrs = corrs.stack().reset_index()
    corrs = pd.concat([corrs, upper], axis=1)
    corrs = corrs[corrs["to_keep"] == True]
    corrs.drop(columns=["to_keep"], inplace=True)
    corrs.columns = ["var1", "var2", "corr"]

    # Drop self-correlations
    corrs = corrs[corrs["var1"] != corrs["var2"]]

    # Sort by highest correlations
    corrs["abs_corr"] = np.abs(corrs["corr"])
    corrs.sort_values(by=["abs_corr"], ascending=False, inplace=True)
    corrs = corrs[corrs["abs_corr"] > threshold]

    # Drop Var2
    if verbose == True:
        print(f"Variables to be dropped:\n{corrs.var2.unique()}")
    else:
        print(f"{corrs.var2.nunique()} variables will be dropped")

    if inplace == True:
        df.drop(columns=corrs.var2.unique(), inplace=True)

        return

    else:
        new_df = df.drop(columns=corrs.var2.unique(), inplace=False)

        return new_df
