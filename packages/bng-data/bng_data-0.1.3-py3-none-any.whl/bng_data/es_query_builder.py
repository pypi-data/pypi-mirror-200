import json
from typing import Any, Dict, List, TypeVar

class ESQueryBuilder():
    """
    Query builder for elasticsearch
    """

    def __init__(self, is_bool: bool = True, page: int = 0, size: int = 1000) -> None:
        self._query: Dict[str, Any] = {}
        self._query["_source"]: Any = True
        self._query["from"]: int = page
        self._query["size"]: int = size
        self._query["query"]: Dict[str, Any] = {}
        self._query_cursor: Dict[str, Any] = self._query["query"]
        if is_bool:
            self._query_cursor["bool"] = {}
            self._query_cursor: Dict[str, Any] = self._query_cursor["bool"]
    
    T = TypeVar("T", bound="ESQueryBuilder")

    def __dict__(self) -> Dict[str, Any]:
        """Return the full query as a dictionary"""

        return self._query
    
    def __str__(self) -> str:
        """Return the full query as a string"""

        return json.dumps(self._query)

    def src(self: T, source: bool) -> T:
        """Update the value of the _source node with a boolean value"""

        self._query["_source"] = source
        return self
    
    def src(self: T, *args: str) -> T:
        """Update the value of the _source node with a list of fields"""

        source: List[Dict[str, Any]] = self._get_list(args)

        self._query["_source"] = source
        return self

    def sort_by(self: T, *args: Dict[str, Any]) -> T:
        """Update the value of the sort node with one or more sorting options"""

        sort: List[Dict[str, Any]] = self._get_list(args)

        self._query["sort"] = sort
        return self

    def filter(self: T, *args: Dict[str, Any]) -> T:
        """List of parameters to perform a filter query"""

        filters: List[Dict[str, Any]] = self._get_list(args)

        self._query_cursor["filter"] = filters
        return self
    
    def must(self: T, *args: List[Dict[str, Any]]) -> T:
        """List of parameters that must match"""

        musts: List[Dict[str, Any]] = self._get_list(args)

        self._query_cursor["must"] = musts
        return self
    
    def must_not(self: T, *args: List[Dict[str, Any]]) -> T:
        """List of parameters that must not match"""

        must_nots: List[Dict[str, Any]] = self._get_list(args)

        self._query_cursor["must_not"] = must_nots
        return self

    def _get_list(self: T, args) -> List[Dict[str, Any]]:
        """Utility function to convert args to a list"""

        items: List[Dict[str, Any]] = []
        for item in args:
            items.append(item)
        return items