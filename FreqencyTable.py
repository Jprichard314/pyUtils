import pandas as pd

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
    sums = pd.DataFrame({'Normalized':table[table.columns[0]].sum().round(4),
            'Absolute':table[table.columns[1]].sum()},index = ['Totals']  )
    table = table.append(sums)
    return table