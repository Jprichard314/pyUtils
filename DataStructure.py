import pandas as pd

def GenerateStructure(data):

# Output
#       A dictionary containing to data set statistics.
# Input
#       A dataframe
# Notes
#   This hsould be the super structure of this entire funtion.  All other necessary functions should fall into this.
#   Should eventually include support for data type specific graphs and information on each field.
#   
#   For DataFrame:
#       # Columns
#       # Shape
#       # duplicates
#       # SummarizeData
#   
#   
#   For Fields:
        # if data type == int | float
            # Box and Whisker Chart
            # Quartile Information
        # if data type == object | categorical
            # Histogram
            # Frequency Table
        # if data type == datetime

############################# Define Field Type Structure

    # def structure_numeric(field):
    #     # input
    #         # field name for a numeric field   
    #     report_structure_field_numeric = {
    #         "Description":"",
    #         "Box and Whisker Plot":""
    #     }
    #         return report_structure_field_numeric

    # def structure_categorical(field):
    #     # input
    #         # field name for a categorical field

    #     report_structure_field_categorical = {
    #         "frequency table": FrequencyTable(data[field]),
    #         "histogram":"",
    #         "values table": data[field].value_counts(),
    #         "bar chart":"",
    #     }
    #         return report_structure_field_categorical

############################# Generate Structure
    report_structure = {}
    report_structure['DataFrame'] = {
        "Columns":data.columns,
        "Shape":data.shape,
        "Duplicates":data[data.duplicated()],
        "Summary":SummarizeDataFrame(data)
        }
