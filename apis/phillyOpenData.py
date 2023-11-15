# cartoApi
import urllib.parse
import requests
import pandas
import datetime

def writeDateTimeFilter(
          end_date
        , interval
        , base_query
        , date_field
):
    # Create start date
    start_date = (
        (
                pandas.to_datetime(
                    datetime.datetime.strptime(end_date,"%m/%d/%Y")
                ) - pandas.DateOffset(months = interval)
        )
         .to_period('m')
         .strftime('%m/%d/%Y')
    )

    # truncate end_date
    end_date = (
        (
                pandas.to_datetime(
                    datetime.datetime.strptime(end_date,"%m/%d/%Y")
                ) - pandas.DateOffset(months = 1)
        )
         .to_period('m')
         .strftime('%m/%d/%Y')
    )

    # create datetime query
    query = f"{base_query} WHERE {date_field} <= '{end_date}' AND {date_field} >= '{start_date}'"

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
    
    def queryDataframe(self):
        data = pandas.read_csv(self.request_url)
        return(data)