import pandas as pd
import seaborn as sns
import numpy as np


def FrequencyTable(Series):   
    # ===============================================================
    # Inputs:
    #     Series -- A series to be turned into a frequency table.
    # Output
    #     A frequency table dataframe describing the frequency of values found in the given series.
    #     Great to build a table to go with a histogram.
    # ChangeLog
    #     08.29.21 -- Created -- JP
    # Notes
    #     Please add data validation to this -- JP
    # ===============================================================
    table_structure = {
        'Normalized':Series.value_counts(normalize = True).round(4)*100,
        'Absolute':Series.value_counts(normalize = False)
    }
    table = pd.concat(table_structure,axis=1)
    sums = pd.DataFrame(
            {
            'Normalized':table[table.columns[0]].sum().round(4),
            'Absolute':table[table.columns[1]].sum()
            },
            index = ['Totals']  )
    table = table.append(sums)
    return table
  
  
  
 

 
 
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
    

def PadZero(x,pad_to):
    '''
    Input
        x = integer, number to be padded
        pad_to = integer, number to be padded to

    return
        string(x) if at appropriate length or x left padded to length pad_to

    Changelog
        11.01.21 -- Created
    '''

    if len(str(x)) == pad_to:
        return(str(x))
    elif len(str(x)) < pad_to:
        return str(0 * (pad_to - len(str(x)))) + str(x)
    else:
        return("Error: Size Overflow")
    
def printColumnLevels(df):
    '''
    input
        x = dataframe with columns 
    output
        print to host the levels found in each columns of the given dataframe.
    

    Notes
        JP -- 11.12.21 -- This can't receive series objects because the iterator for a series is the element, not the column.  Add in validation to check for type. 
    '''
    for x in df:
        print(f'{x}\n{len(x)*"="}\n\tVALUES\n\t------\n{df[x].unique()}\n')


def ECDF(x):
    '''
    input:
        x: series of ordinal data.
    output:
        ECDF plot
    '''

    list_yaxis = np.arange(
        0,
        110,
        10 
    ) 
    list_xaxis = np.arange(
        np.min(x),
        np.max(x)+5,
        5
    ) 


    _ = sns.relplot(
        x = x.sort_values(),
        y = (np.arange(
                1,
                len(x)+1
            ) / len(x)) * 100,
        kind = 'scatter',
        aspect= 2,
        height= 10
    ).set(
        yticks = list_yaxis,
        xticks = list_xaxis,
        ylabel = 'Cumulative Percentage'
    ).set_xticklabels(
        list_xaxis,
        rotation = 45
    ).set_yticklabels(
        list_yaxis
    )


def print_DataSample(df,x):
    [print(f"{'='*100}\n{row[1]}\n\n{'='*100}") for row in df.sample(x).iterrows()]

def print_LongString(df, field_note,field_id, x):
    [print(f"{'='*100}\nID:{row[1][field_id]}\n\nNote:\n{row[1][field_note]}\n\n{'='*100}") for row in df.sample(x).iterrows()]

def create_dateTable(start, end, label, freq):
    '''
    input
        Start:  String -- Starting date for the date table
        End:    String -- Ending date for the table
        Close:  String -- Label for all columns
    Output
        Table including from Start to End date with the following fields, broken down
        by hour.
            Date:       Datetime for the listed date
            Hour:       Hour period for listed date
            Month:      Month period for the listed date
            Week:       Week (ending sat) period for the listed date
            Quarter:    Quarter period for the listed date
            DayName:    Day of the week for the listed date
    
    '''
    array_dateRange = pd.date_range(
                      start = start
                    , end= end
                    , freq = freq
                )
    dict_calendar = {
          f"{label}_Date"       :array_dateRange
        , f"{label}_Hour"       :array_dateRange.to_period('H')
        , f"{label}_Month"      :array_dateRange.to_period('M')
        , f"{label}_Week"       :array_dateRange.to_period('W-SAT')
        , f"{label}_Quarter"    :array_dateRange.to_period('Q')
        , f"{label}_DayName"    :array_dateRange.day_name()
    }
    data_product = pd.DataFrame(
          dict_calendar
    )
    
    return data_product
