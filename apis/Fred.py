# cartoApi
import urllib.parse
import requests
import polars
import pandas
import json
from datetime import datetime
from dateutil import relativedelta

class fredApi:
    
    def __init__(self,endpoint, parameters) -> None:
        self.base              = endpoint
        self.parameters        = parameters
        self.query             = "&".join([
                                        
                                        f"{key}={self.parameters[key]}" 
                                        
                                        for key in self.parameters.keys() 
                                ])
        self.request_plain     = f"{self.base}{self.query}"
        self.request_url       = f"{self.base}{urllib.parse.quote_plus(self.query)}"
        self.content           = None
        self.data_raw          = None
        self.data              = None


        # Prep Ingest Data
        self._queryRequest()
        self._prep_for_ingest()
        self._po_queryDataframe()
        

    def _queryRequest(self):
        request = requests.get(self.request_url)

        if request.status_code != 200:
            request = requests.get(self.request_plain)
        
        self.content = request.content

    def _prep_for_ingest(self):
        
        data = json.loads(self.content)['observations']
        
        self.data_raw = data
        

    
    def _po_queryDataframe(self, **kwargs):
        data = polars.DataFrame(self.data_raw)
        self.data = data
