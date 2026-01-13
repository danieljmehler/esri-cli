import requests
import logging
from typing import Dict, TYPE_CHECKING
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout

if TYPE_CHECKING:
    from .services import Services
    from .folder import Folder
    from .service import Service
    from .layer import Layer

logger = logging.getLogger(__name__)


class EsriClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30

    def _get_json(self, url: str, params: Dict = None) -> Dict:
        """Make HTTP request with comprehensive error handling and retries.
        
        Args:
            url: URL to request
            params: Query parameters
            
        Returns:
            JSON response as dictionary
            
        Raises:
            ConnectionError: Network connection issues
            HTTPError: HTTP status errors
            RequestException: Other request-related errors
        """
        params = params or {}
        if 'f' not in params:
            params['f'] = 'pjson'
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, params=params, timeout=30)
                logger.debug(f"Request URL: {response.url}")
                logger.debug(f"Response status: {response.status_code}")
                response.raise_for_status()
                
                # Check if response is valid JSON
                try:
                    json_data = response.json()
                except ValueError as e:
                    raise RequestException(f"Invalid JSON response from {url}: {e}")
                
                # Check for ESRI-specific errors
                if 'error' in json_data:
                    error_info = json_data['error']
                    error_msg = error_info.get('message', 'Unknown ESRI error')
                    raise RequestException(f"ESRI API error: {error_msg}")
                
                return json_data
                
            except (ConnectionError, Timeout) as e:
                if attempt < max_retries - 1:
                    logger.debug(f"Attempt {attempt + 1} failed, retrying: {e}")
                    continue
                else:
                    raise type(e)(f"Failed after {max_retries} attempts: {e}")
            except HTTPError as e:
                if response.status_code == 404:
                    raise HTTPError(f"Resource not found: {url}")
                elif response.status_code == 403:
                    raise HTTPError(f"Access forbidden: {url}")
                elif response.status_code >= 500:
                    if attempt < max_retries - 1:
                        logger.debug(f"Server error {response.status_code}, retrying: {e}")
                        continue
                    else:
                        raise HTTPError(f"Server error ({response.status_code}): {url}")
                else:
                    raise HTTPError(f"HTTP error ({response.status_code}): {url}")
            except RequestException as e:
                raise RequestException(f"Request failed for {url}: {e}")

    def get_services(self) -> 'Services':
        from .services import Services
        url = f"{self.base_url}/rest/services"
        data = self._get_json(url)
        return Services(data, self)

    def get_folder(self, folder_name: str) -> 'Folder':
        from .folder import Folder
        url = f"{self.base_url}/rest/services/{folder_name}"
        data = self._get_json(url)
        return Folder(data, self, folder_name)

    def get_service(self, service_path: str) -> 'Service':
        from .service import Service
        url = f"{self.base_url}/rest/services/{service_path}"
        data = self._get_json(url)
        return Service(data, self, service_path)

    def get_layer(self, service_path: str, layer_id: int) -> 'Layer':
        from .layer import Layer
        url = f"{self.base_url}/rest/services/{service_path}/{layer_id}"
        data = self._get_json(url)
        return Layer(data, self, service_path, layer_id)