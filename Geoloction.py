from functools import lru_cache
import json
from typing import Any, Optional
from urllib import request
from dataclasses import dataclass
@dataclass
class GeoData:
    ip: Optional[str] = None
    city:Optional[str] = "Unknown"
    region:Optional[str] = "Unknown" 
    country:Optional[str] = "Unknown" 
    loc:Optional[str] = None
    org:Optional[str] = None
    postal:Optional[str] = None
    timezone:Optional[str] = None
    hostname:Optional[str] = None
    readme:Optional[str] = None

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

