from typing import Any, Dict
import requests

class HttpClient():
    def __init__(self, auth: tuple, headers: Dict[str, str] = {"Conten-Type": "application/json"}) -> None:
        self.auth = auth
        self.headers = headers
    
    def get(self, url: str, **kwargs) -> Dict[str, Any]:
        full_url = f"{url}"
        if len(kwargs) > 0:
            full_url = full_url.join([f"?{key}={value}" for key, value in kwargs.items()])
        req = requests.get(full_url, headers=self.headers, auth=tuple(self.auth))
        return req.json()
    
    def post(self, url: str, payload = None, **kwargs) -> Dict[str, Any]:
        full_url = f"{url}"
        if len(kwargs) > 0:
            full_url = full_url.join([f"?{key}={value}" for key, value in kwargs.items()])
        req = requests.post(full_url, data=payload, headers=self.headers, auth=tuple(self.auth))
        return req.json()