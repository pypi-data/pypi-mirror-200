from typing import Any, Dict, TypeVar
import requests

class HttpClient():
    def __init__(self, url: str, auth: tuple) -> None:
        self.url = url
        self.auth = auth
        self.headers = {"Conten-Type": "application/json"}
    
    def get(self, type, id = None) -> Dict[str, Any]:
        full_url = f"{self.url}/storage/{type}/{id}"
        req = requests.get(full_url, headers=self.headers, auth=self.auth)
        return req.json()
    
    def post(self, type, id = None, payload = None) -> Dict[str, Any]:
        full_url = f"{self.url}/storage/{type}/{id}"
        req = requests.post(full_url, data=payload, headers=self.headers, auth=self.auth)
        return req.json()