# cartoApi
import urllib.parse
import requests
import polars
import pandas
from datetime import datetime
from dateutil import relativedelta

def writeDateTimeFilter(
          end_date
        , interval
        , base_query
        , date_field
):

    # truncate end_date
    end_date = (datetime.strptime(end_date, '%m/%d/%Y'))

    # Create start date
    start_date = end_date - relativedelta.relativedelta(months = interval)

    # create datetime query
    query = f"{base_query} WHERE {date_field} <= '{end_date:%m/%d/%Y}' AND {date_field} >= '{start_date:%m/%d/%Y}'"

    return(query)


class cartoApi:
    
    def __init__(self,query,format = "CSV") -> None:
        self.base              = "https://phl.carto.com/api/v2/sql?q="
        self.query             = query
        self.format            = format
        self.request_plain     = f"{self.base}{self.query}&format={self.format}"
        self.request_url       = f"{self.base}{urllib.parse.quote_plus(self.query)}&format={self.format}"

    def queryRequest(self):
        request = requests.get(self.request_url)
        return request.content
    
    def queryDataframe(self, **kwargs):
        data = polars.read_csv(self.request_url, 
                               infer_schema_length = kwargs['infer_schema_length'] if kwargs['infer_schema_length'] is not None else 100,
                               schema_overrides = kwargs['schema_overrides'] if kwargs['schema_overrides'] is not None else None)
        return(data)
    


