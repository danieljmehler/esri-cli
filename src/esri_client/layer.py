from typing import Dict, TYPE_CHECKING
from requests.exceptions import RequestException

if TYPE_CHECKING:
    from .client import EsriClient

class Layer:
    def __init__(self, data: Dict, client: 'EsriClient', service_path: str, layer_id: int):
        self.data = data
        self.client = client
        self.service_path = service_path
        self.id = layer_id
        self.name = data.get('name', '')

    def query(self, where: str = "1=1", format: str = "pjson", **kwargs) -> Dict:
        """Query the layer with error handling.
        
        Args:
            where: SQL where clause
            format: Output format (pjson, geojson, kml)
            **kwargs: Additional query parameters
            
        Returns:
            Query results as dictionary
            
        Raises:
            RequestException: If query fails
        """
        url = f"{self.client.base_url}/rest/services/{self.service_path}/{self.id}/query"
        
        # Handle KML format by querying with geojson
        query_format = 'geojson' if format == 'kml' else format
        
        # Set defaults
        params = {'where': where, 'f': query_format, 'resultRecordCount': 100, **kwargs}
        
        # Convert string parameters to integers where needed
        if 'resultRecordCount' in params and isinstance(params['resultRecordCount'], str):
            params['resultRecordCount'] = int(params['resultRecordCount'])
        if 'resultOffset' in params and isinstance(params['resultOffset'], str):
            params['resultOffset'] = int(params['resultOffset'])
        
        try:
            # Only paginate if resultOffset is not provided by the user
            if 'resultOffset' not in kwargs:
                all_features = []
                offset = 0
                
                while True:
                    params['resultOffset'] = offset
                    response = self.client._get_json(url, params)
                    
                    features = response.get('features', [])
                    all_features.extend(features)
                    
                    # Break if we got fewer records than requested
                    if len(features) < params['resultRecordCount']:
                        break
                        
                    offset += params['resultRecordCount']
                
                # Return combined response
                response['features'] = all_features
            else:
                # Single page request
                response = self.client._get_json(url, params)
            
            return response
            
        except RequestException as e:
            raise RequestException(f"Layer query failed for layer {self.id}: {e}")