from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import EsriClient


class Folder:
    def __init__(self, data: Dict, client: 'EsriClient', name: str):
        from .service import Service
        
        self.data = data
        self.client = client
        self.name = name
        self.services = [Service(s, client, f"{name}/{s['name']}") for s in data.get('services', [])]