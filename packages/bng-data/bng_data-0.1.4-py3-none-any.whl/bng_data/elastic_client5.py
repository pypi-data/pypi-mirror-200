from elasticsearch5 import Elasticsearch as Elasticsearch5
from typing import Dict, Any

class ElasticClient5():
    def __init__(self, host: str, port: str, auth: tuple) -> None:
        self.client = Elasticsearch5([f"{host}:{port}"], http_auth=auth)
    
    def query(self, es_query: Dict[str, Any], index: str, page: int, size: int) -> Dict[str, Any]:
        """Run an elasticsearch query against the provided index"""

        return self.client.search(index=index, pretty=True, human=True, body=es_query)  
    
    def get_by_id(self, index: str, doc_id: str) -> Dict[str, Any]:
        """Retrieve a single document from the provided index"""

        return self.client.get(index=index, id=doc_id, pretty=True, human=True)
      
    def update(self, index: str, doc_id: str, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Updates a document in the provided index"""

        return self.client.update(index=index, id=doc_id, body={"doc": doc})
    
    def get_mapping(self, index: str) -> Dict[str, Any]:
        """Retrieves the mapping data for the provided index"""

        return self.client.indices.get_mapping(index)
    
    def get_mapping_template(self, index: str) -> Dict[str, Any]:
        """Retrieves the mapping data for the provided index"""

        return self.client.indices.get_template(index)