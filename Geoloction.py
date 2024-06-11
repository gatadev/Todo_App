from functools import lru_cache
import json
from typing import Any
from urllib import request
from dataclasses import dataclass
@dataclass
class GeoData:
    ip: str
    city:str
    region:str
    country:str
    loc:str
    org:str
    postal:str
    timezone:str
    hostname:str
    readme:str

class Geoloction:
    def __init__(self) -> None:
        pass 
    @lru_cache()
    def get_location(*args):
        """
        Static method to fetch and cache geolocation data using LRU cache.
        """
        url = "https://ipinfo.io"
        with request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return GeoData(**json.loads(data))

