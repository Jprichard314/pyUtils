import pandas as pd

def FrequencyTable(series_data):   
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
    
    print('test')
    table_structure = {
          'Normalized':series_data.value_counts(normalize = True).round(4)
        , 'Absolute':series_data.value_counts(normalize = False)
    }
    table = pd.concat(table_structure,axis=1)
    sums = pd.DataFrame(
            {
                'Normalized':series_data.value_counts(normalize = True).sum().round(4),
                'Absolute':series_data.value_counts(normalize = False).sum()
            }
            ,index = ['Totals'] )
    table = pd.concat([table,sums])
    return table