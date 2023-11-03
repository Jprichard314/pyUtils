#from msilib import text
import pandas
import Tools_Personal
import SummaryStatistics
import text_analysis

class biFramework:
    def __init__(self,df):
        self.raw_df             = df
        self.clean_df           = None
        self.date_fields        = {}
        self.dateTables         = {}
        self.SummaryTable       = None
        self.text_analytics     = {}

    def full_clean(self, field_date,freq = 'D'):

        if freq == 'D':
            string_timeFormat = '%Y.%m.%d'
        elif freq == 'H':
            string_timeFormat = '%Y.%m.%d %H'
        else:
            string_timeFormat ="%Y.%m.%d"

        # Can we break all of these cleaning operations into columnar operations and do a join or
        # merge at the end?
        self._dates_set_dates([field_date])
        self._dates_generate_dateTables(freq)
        self.clean_df = self.raw_df.assign(
            date_merge = pandas.to_datetime(self.raw_df[field_date]).dt.strftime(string_timeFormat)
        ).merge(
              self.dateTables[field_date].assign(
                mergeField = self.dateTables[field_date][f"{field_date.lower().replace(' ','_')}_Date"].dt.strftime(string_timeFormat)
              )
            , how       = 'left'
            , right_on  = "mergeField"
            , left_on   = f'date_merge'
        )
        

    def _dates_set_dates(self, field_dates):
        '''
        Provide a list of fields considered dates.
        '''

        self.date_fields.update(
            {
                field:{
                      'start':  pandas.to_datetime(self.raw_df[field]).dt.date.min()
                    , 'end':    pandas.to_datetime(self.raw_df[field]).dt.date.max()
                }
                for field in field_dates
            }
        )
        

    def _dates_generate_dateTables(self,freq):
        self.dateTables.update({
                field:Tools_Personal.create_dateTable(
                      start     = self.date_fields[field]['start']
                    , end       = self.date_fields[field]['end']
                    , label     = field.lower().replace(' ','_')
                    , freq      = freq
            )
            for field in self.date_fields.keys()
        })
    
    def _eda_generate_summary(self):
        # This needs to be cleaned so a workflow is established before passing summary.
        self.SummaryTable = SummaryStatistics.SummarizeDataFrame(self.clean_df)




    # Turn the text analysis functions into a single object and pull them in here instead.  Have them deposit into 
    # a dictionary.   
    def _text_generate_textMatrix(self,field_aggregate,field_value):
        # This needs to be cleaned so a workflow is established before passing summary.
        self.text_analytics.update(
            {
                field_aggregate:{
                    'text_Matrix':
                        text_analysis.aggregate_and_vectorize(
                              self.clean_df
                            , field_aggregate=field_aggregate
                            , field_value=field_value
                        )
                }
            }
        )

    def _text_generate_textDrivers(self,field_aggregate,x):
        # This needs to be cleaned so a workflow is established before passing summary.
        self.text_analytics[field_aggregate].update(
                {
                    'text_Drivers':
                        text_analysis.textAnalytics_drivingTerms_dataClass(
                              self.text_analytics[field_aggregate]['text_Matrix']
                            , x = x
                        )
                }
        )

    
    
