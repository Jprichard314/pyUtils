# cartoApi
import urllib.parse
import requests
import polars
import pandas
import json
import sys
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
    
    def po_queryDataframe(self, **kwargs):
        data = polars.read_csv(self.request_url, 
                               infer_schema_length = kwargs['infer_schema_length'] if kwargs['infer_schema_length'] is not None else 100,
                               schema_overrides = kwargs['schema_overrides'] if kwargs['schema_overrides'] is not None else None)
        return(data)
    
    def pa_queryDataframe(self):
        data = pandas.read_csv(self.request_url)
        return(data)
    


class cartoApi_v2:

    def __init__(self,config,format = "CSV") -> None:

        # ATTR: Config
        self._config                = config
        self._format                = format
        self._raw_query             = None
        self._format                = None
        self._lookback              = None

        # ATTR: Query
        self._base                   = "https://phl.carto.com/api/v2/sql?q="
        self._query                  = None
        self._request_plain          = None
        self._request_url            = None

        # ATTR: Data
        self._infer_schema_length   = None
        self._schema_overrides      = None
        self.data                   = None

        # DO: Parse Config Files:
        self._parse_configs()
        self._generate_url()



    # ========== Parse Config ==========
    def _parse_schema_overides(self):
        
        if "schema_overrides" in self._config.keys():
            self._schema_overrides = {
                key: getattr( sys.modules['polars.datatypes'], self._config["schema_overrides"][key]) for key in self._config["schema_overrides"]
            }

    def _parse_configs(self):

        self._parse_schema_overides()
        self._raw_query = self._config['query']
        self._format = self._config['format']
        self._infer_schema_length = self._config["infer_schema_length"] if "infer_schema_length" in self._config.keys() else None
        self._lookback = self._config["lookback"] if "lookback" in self._config.keys() else None

    # ========== Generate Query ==========

    def _writeDateTimeFilter(
        self
    ):
        # Lookback From Current Date:
        if self._lookback['end_date'] == "current":

            # Create start date
            start_date = datetime.today() - relativedelta.relativedelta(months = self._lookback['interval'])

            # create datetime query
            query = f"{self._raw_query} WHERE {self._lookback['date_field']} <= '{datetime.today():%m/%d/%Y}' AND {self._lookback['date_field']} >= '{start_date:%m/%d/%Y}'"

        self._query = query
    
    def _generate_url(self):

        if "lookback" in self._config.keys():
            self._writeDateTimeFilter()

        self._request_plain = f"{self._base}{self._query}&format={self._format}"
        self._request_url = f"{self._base}{urllib.parse.quote_plus(self._query)}&format={self._format}"
        

    # ========== Get Data ==========

    def queryRequest(self):
        request = requests.get(self._request_url)
        return request.content
    
    def po_queryDataframe(self, **kwargs):
        data = polars.read_csv(self._request_url, 
                               infer_schema_length = self._infer_schema_length if self._infer_schema_length is not None else 100,
                               schema_overrides = self._schema_overrides if self._schema_overrides is not None else None)
        return(data)