import pandas as pd
import numpy as np

def dummy_code(
    df:pd.DataFrame,
    dv=None,
    columns="all",
    categorical:bool=True,
    numeric:bool=True,
    categorical_max_levels:int=20,
    numeric_max_levels:int=10,
    dummy_na:bool=False,
    output_file = None, 
    output_method = 'a') -> pd.DataFrame:

    """
    Dummy code (AKA "one-hot encode") categorical and numeric columns based on the paremeters specificed below. Note: categorical columns will be dropped after they are dummy coded; numeric columns will not
    
    Ex: gitlabds.dummy_code(df, dv=None, columns='all', categorical=True, numeric=True, categorical_max_levels = 20, numeric_max_levels = 10, dummy_na=False):

    Parameters:


    df : your pandas dataframe

    dv : The column name of your outcome. Entering your outcome variable in will prevent it from being dummy coded. May be left blank there is no outcome variable.

    columns : Will examine at all columns by default. To limit to just  a subset of columns, pass a list of column names.

    categorical : Set to True to attempt to dummy code any categorical column passed via the columns parameter.

    numeric : Set to True to attempt to dummy code any numeric column passed via the columns parameter.

    categorical_max_levels : Maximum number of levels a categorical column can have to be eligible for dummy coding.

    categorical_max_levels : Maximum number of levels a numeric column can have to be eligible for dummy coding.

    dummy_na : Set to True to create a dummy coded column for missing values.


    Returns

    DataFrame with dummy-coded columns. Categorical columns that were dummy coded will be dropped from the dataframe.
    """
    
    if columns == "all":
        var_list = df.columns.tolist()
        print("Will examine all variables as candidate for dummy coding")

    else:
        var_list = columns
        print(f"Will examine the following variables as candidates for dummy coding: {var_list}")

    # Do not dummy code dv outcome
    if (dv != None) & (dv in var_list):
        var_list.remove(dv)

    new_df = df.copy(deep=True)

    if categorical == True:

        # Determine number of levels for each field
        cat_levels = (df[var_list].select_dtypes(include="object").nunique(dropna=True, axis=0))
        print(f"\nCategorical columns selected for dummy coding: \n{cat_levels}")
        
        cat_levels = cat_levels[(cat_levels <= categorical_max_levels) & (cat_levels > 1)]
        print(f"\nCategorical columns below categorical_max_levels threshold of {categorical_max_levels}: \n{cat_levels}\n\n")

        # Get columns to dummy code
        cat_columns = cat_levels.index.tolist()

        # Dummy Code. Will drop categorical field after dummy is created
        new_df = pd.get_dummies(data=new_df, prefix_sep="_dummy_", columns=cat_columns, dummy_na=dummy_na)
        
        

        # Remove dummy coded categorical fields from var_list because pandas removes them automatically from the df
        var_list = [elem for elem in var_list if elem not in cat_columns]

    if numeric == True:

        num_levels = df[var_list].select_dtypes(include=["number"]).nunique(dropna=True, axis=0)
        print(f"\nNumeric columns selected for dummy coding: \n{num_levels}")
        
        num_levels = num_levels[(num_levels <= numeric_max_levels) & (num_levels > 2)]
        print(f"\nNumeric columns below numeric_max_levels threshold of {numeric_max_levels}: \n{num_levels}\n\n")

        # Get columns to dummy code
        num_columns = num_levels.index.to_list()

        # pd.get_dummies will drop fields by default. Creating a df of numeric field to be dummy coded so they can be added back on
        num_df = new_df[num_columns].copy(deep=True)

        # Dummy code
        new_df = pd.get_dummies(data=new_df, prefix_sep="_dummy_", columns=num_columns, dummy_na=dummy_na)

        # Concat back together
        new_df = pd.concat([new_df, num_df], axis=1)
        
    if output_file != None:
        f = open(output_file, output_method)
        f.write("\n\ndef dummy_code(df):")   
        f.write("\n    import pandas as pd")
        f.write("\n    import numpy as np")
        f.write("\n    import warnings")
        f.write("\n    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)")
        
        #Get list of new columns that were created
        dummy_cols = new_df.columns[~new_df.columns.isin(df.columns)].tolist()
        
        for d in dummy_cols:
            #Convert numbers to numbers. Leave strings as strings
            try:
                float(d.split('_dummy_')[1])
                
                if d.split('_dummy_')[1] == 'nan':
                    f.write(f"\n    df['{d}'] = np.where(df['{d.split('_dummy_')[0]}'].isna(), 1, 0)")
            
                else:
                    f.write(f"\n    df['{d}'] = np.where(df['{d.split('_dummy_')[0]}'] == {d.split('_dummy_')[1]}, 1, 0)")
                
            except ValueError:
                f.write(f"\n    df['{d}'] = np.where(df['{d.split('_dummy_')[0]}'] == '{d.split('_dummy_')[1]}', 1, 0)")
        
        #model_pte_df['max_historical_user_count_change_dummy_1.0'] = np.where(model_pte_df['max_historical_user_count_change'] == 1, 1, 0)
        f.write('\n\n    return df')
        f.close()

    return new_df


def dummy_top(
    df:pd.DataFrame=None,
    dv:str=None,
    columns="all",
    min_threshold:float=0.05,
    drop_categorial:bool=True,
    verbose:bool=True,
    output_file = None, 
    output_method = 'a') -> pd.DataFrame:

    """
    Dummy codes only categorical levels above a certain threshold of the population. Useful when a column contains many levels but there is not a need or desire to dummy code every level. Currently only works for categorical columns.
    
    Ex: gitlabds.dummy_top(df=None, dv=None, columns = 'all', min_threshold = 0.05, drop_categorial=True, verbose=True):

    Parameters:


    df : your pandas dataframe

    dv : The column name of your outcome. Entering your outcome variable in will prevent it from being dummy coded. May be left blank there is no outcome variable.

    columns : Will examine at all columns by default. To limit to just  a subset of columns, pass a list of column names.

    min_threshold: The threshold at which levels will be dummy coded. For example, the default value of 0.05 will dummy code any categorical level that is in at least 5% of all rows.
    _ drop_categorical: Set to True to drop categorical columns after they are considered for dummy coding. Set to False to keep the original categorical columns in the dataframe.

    verbose : Set to True to print detailed list of all dummy columns being created. Set to False to suppress.


    Returns

    DataFrame with dummy coded columns.
    """
    
    
    if output_file != None:
        f = open(output_file, output_method)
        f.write("\n\ndef dummy_top(df):")
        f.write("\n    import pandas as pd")
        f.write("\n    import numpy as np")
        f.write("\n    import warnings")
        f.write("\n    warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)")

    if columns == "all":
        var_list = df.columns.tolist()
        print("Will examine all remaining categorical variables as candidate for dummy top coding")

    else:
        var_list = columns
        print("Will examine the following categorical variables as candidate for dummy top coding: {var_list}")

    # Do not dummy code dv outcome
    if dv != None:
        var_list.remove(dv)

    new_df = df.copy(deep=True)

    # Determine number of levels for each field
    cat_levels = df[var_list].select_dtypes(include="object").nunique(dropna=True, axis=0)
    
    print(f"\nCategorical columns selected for dummy top coding using threshold of {min_threshold*100}%: \n{cat_levels}\n")

    # Get columns to dummy code
    cat_columns = cat_levels.index.tolist()

    # Create dummy codes for those categorical fields that exceed min_threshold
    for d in cat_columns:
        levels = df[d].value_counts() / len(df)

        if verbose == True:
            print(d)
            print(f"The following levels exceed min_threshold:\n{levels.loc[levels > min_threshold]}\n\n")
            
        levels = levels.loc[levels > min_threshold].index.tolist()

        for l in levels:
            dummy_name = str(d) + "_dummy_" + str(l)
            new_df[dummy_name] = np.where(new_df[d] == str(l), 1, 0)
            
            if output_file != None: 
                
                if l == 'nan':
                    f.write(f"\n    df['{dummy_name}'] = np.where(df['{d}'].isna(), 1, 0)")
                    
                else:    
                    f.write(f"\n    df['{dummy_name}'] = np.where(df['{d}'] == '{l}', 1, 0)")

        # drop categorical fields after they have been dummy coded
        if drop_categorial == True:
            new_df.drop(columns=[d], inplace=True)
            
    if output_file != None: 
        f.write('\n\n    return df')
        f.close()

    return new_df
