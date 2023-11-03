# cartoApi
import urllib.parse
import requests


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