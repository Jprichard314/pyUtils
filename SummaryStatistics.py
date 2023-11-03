import pandas as pd
 
 
def SummarizeDataFrame(data):
    # ===============================================================
    # Inputs:
    #     Series -- A data set and collection of columns of interest.
    # Output
    #           Total Entrees | Count of Missing | % Missing | Unique Levels | Data Type  
    #           --------------------------------------------------------------------  
    #   Columns               |                  |           |               |   
    #     
    # ChangeLog
    #     08.29.21 -- Created -- JP
    #     09.01.21 -- Count of Missing shows actual missing data now -- JP
    # Notes
    #     Please add data validation to this -- JP
    #     
    #
    #
    #
    # ===============================================================

        df_dict = {}
        for column in data.columns:
                np_list = [len(data[column]),                                                                   #
                        data[column].isna().sum(),                                                              #
                        (data[column].isna().sum() / len(data[column])).round(4)*100,                           #
                        len(data[column].value_counts().index),                                                 #
                        data[column].dtype]                                                                     # 
                df_dict[column] = np_list
        df = pd.DataFrame.from_dict(orient = 'index', data = df_dict,columns=['Total Entrees','Count of Missing','Percent Missing','Unique Levels','Data Type'])
        
        return df
