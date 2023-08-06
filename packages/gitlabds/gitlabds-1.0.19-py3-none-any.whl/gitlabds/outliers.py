import pandas as pd
from scipy import stats
import numpy as np

def mad_outliers(
    df:pd.DataFrame,
    dv:str=None,
    min_levels:int=10,
    columns="all",
    threshold=4,
    inplace:bool=False,
    verbose:bool=True,
    windsor_threshold:float=0.01,
    output_file = None,
    output_method = 'a'
) -> pd.DataFrame:
    """
    Median Absoutely Deviation for outlier detection and correction. By default will windsor all numeric values in your dataframe that are more than 4 standard deviations above or below the median ('threshold').

    Ex: gitlabds.mad_outliers(df, dv=None, min_levels=10, columns = 'all', threshold=4, inplace=False, verbose=True, windsor_threshold=0.01):

    Parameters:


    df : your pandas dataframe

    dv : The column name of your outcome. Entering your outcome variable in will prevent it from being windsored. May be left blank there is no outcome variable.

    min_levels : Only include columns that have at least the number of levels specified.

    columns : Will examine at all numeric columns by default. To limit to just  a subset of columns, pass a list of column names. Doing so will ignore any constraints put on by the 'dv' and 'min_levels' paramaters.

    threshold : Windsor values greater than this number of standard deviations from the median.

    inplace : Set to True to replace existing dataframe. Set to false to create a new one. Set to False to suppress

    verbose : Set to True to print outputs of windsoring being done. Set to False to suppress.

    windsor_threshold : Only windsor values that affect less than this percentage of the population.


    Returns

    DataFrame with windsored values or None if inplace=True.

    """

    print("\nOutliers\n")
    
    if output_file != None:
        f = open(output_file, output_method)
        f.write("def outliers(df):")
        f.write("\n    import pandas as pd")
        f.write("\n    import numpy as np")
        
    

    if columns == "all":
        var_list = pd.DataFrame(df.select_dtypes(include=["number"]).nunique(dropna=True, axis=0))

        # Exclude DV from outliers if one is provided
        if (dv != None) & (dv in var_list.index.to_list()):
            var_list.drop(dv, inplace=True)

        # Exclude Numeric values that are below min_levels threshold
        var_list = var_list[var_list[0] >= min_levels]

        # Set as List
        var_list = var_list.index.to_list()

    else:
        var_list = columns

    # Make copy of DF to preserve original
    if inplace == True:
        for v in var_list:

            old_min = df[v].min()
            old_max = df[v].max()

            # Determine MAD
            median = np.nanmedian(df[v])
            mad = stats.median_abs_deviation(df[v], axis=0, scale=1)

            # Calculate Z Scores and new max/min to be considered within the acceptable range
            # If more than half of the observations are equal to zero then normalization does not make sense.
            if mad == 0:
                z_scores = [0.6745 * (x - mad) for x in df[v]]  # 0.6745 to standardize it to 1 SD
                new_min = old_min
                new_max = old_max
            else:
                z_scores = [0.6745 * (x - median) / mad for x in df[v]]  # 0.6745 to standardize it to 1 SD

                new_min = np.nanmedian(df[v]) - ((mad * threshold) / 0.6745)
                new_max = np.nanmedian(df[v]) + ((mad * threshold) / 0.6745)

            if df[v].dtypes == int:
                new_min = np.floor(new_min)
                new_max = np.ceil(new_max)

            # Add Z Score to DF
            df["z_score"] = z_scores

            # Determine number of rows affected by new min/max
            min_aff = len(df[df["z_score"] < -threshold])
            max_aff = len(df[df["z_score"] > threshold])

            # Windsor values if they fall below the windsor_threshold
            if ((min_aff / len(df) < windsor_threshold) and (min_aff > 0) and (new_min != old_min)):
                
                df[v].clip(lower=new_min, inplace=True)

                if verbose == True:
                    print(f"{v} - MAD: {mad}; Lower Windsor Value: {new_min}, Rows affected {min_aff} ({min_aff/len(df)*100})")
                    
                if output_file != None:
                    f.write(f"\n    df['{v}'] = np.where(df['{v}'] < {new_min}, {new_min}, df['{v}'])")

            if ((max_aff / len(df) < windsor_threshold) and (max_aff > 0) and (new_max != old_max)):
                
                df[v].clip(upper=new_max, inplace=True)

                if verbose == True:
                    print(f"{v} - MAD: {mad}; Upper Windsor Value: {new_max}, Rows affected {max_aff} ({max_aff/len(df)*100}%)")
                    
                if output_file != None:
                    f.write(f"\n    df['{v}'] = np.where(df['{v}'] > {new_max}, {new_max}, df['{v}'])")

            # Cleanup
            df.drop(["z_score"], inplace=True, axis=1)

        return

    else:
        new_df = df.copy(deep=True)

        for v in var_list:

            old_min = new_df[v].min()
            old_max = new_df[v].max()

            # Determine MAD
            median = np.nanmedian(new_df[v])
            mad = stats.median_abs_deviation(new_df[v], axis=0, scale=1)

            # Calculate Z Scores and new max/min to be considered within the acceptable range
            # If more than half of the observations are equal to zero then normalization does not make sense.
            if mad == 0:
                
                z_scores = [0.6745 * (x - mad) for x in new_df[v]]  # 0.6745 to standardize it to 1 SD
                new_min = old_min
                new_max = old_max
                
            else:
                
                z_scores = [0.6745 * (x - median) / mad for x in new_df[v]]  # 0.6745 to standardize it to 1 SD
                new_min = np.nanmedian(new_df[v]) - ((mad * threshold) / 0.6745)
                new_max = np.nanmedian(new_df[v]) + ((mad * threshold) / 0.6745)

            if df[v].dtypes == int:
                new_min = np.floor(new_min)
                new_max = np.ceil(new_max)

            # Add Z Score to DF
            new_df["z_score"] = z_scores

            # Determine number of rows affected by new min/max
            min_aff = len(new_df[new_df["z_score"] < -threshold])
            max_aff = len(new_df[new_df["z_score"] > threshold])

            # Windsor values if they fall below the windsor_threshold
            if ((min_aff / len(df) < windsor_threshold) and (min_aff > 0) and (new_min != old_min)):
                
                new_df[v].clip(lower=new_min, inplace=True)

                if verbose == True:
                    print(f"{v} - MAD: {mad}; Lower Windsor Value: {new_min}, Rows affected {min_aff} ({min_aff/len(df)*100})")
                    
                if output_file != None:
                    f.write(f"\n    df['{v}'] = np.where(df['{v}'] < {new_min}, {new_min}, df['{v}'])")

            if ((max_aff / len(df) < windsor_threshold) and (max_aff > 0) and (new_max != old_max)):
                
                new_df[v].clip(upper=new_max, inplace=True)

                if verbose == True:
                    print(f"{v} - MAD: {mad}; Upper Windsor Value: {new_max}, Rows affected {max_aff} ({max_aff/len(df)*100}%)")
                    
                if output_file != None:
                    f.write(f"\n    df['{v}'] = np.where(df['{v}'] > {new_max}, {new_max}, df['{v}'])")

            # Cleanup
            new_df.drop(["z_score"], inplace=True, axis=1)
            
        if output_file != None: 
            f.write('\n\n    return')
            f.close()

        return new_df
