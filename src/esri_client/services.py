from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import EsriClient


class Services:
    def __init__(self, data: Dict, client: 'EsriClient'):
        from .folder import Folder
        from .service import Service
        
        self.data = data
        self.client = client
        self.folders = [Folder({'folderName': f}, client, f) for f in data.get('folders', [])]
        self.services = [Service(s, client, s['name']) for s in data.get('services', [])]