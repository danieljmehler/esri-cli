from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import EsriClient
    from .layer import Layer


class Service:
    def __init__(self, data: Dict, client: 'EsriClient', path: str):
        from .layer import Layer
        
        self.data = data
        self.client = client
        self.path = path
        self.name = data.get('name', '')
        self.type = data.get('type', '')
        self.layers = [Layer(layer, client, path, layer['id']) for layer in data.get('layers', [])]

    def get_layer(self, layer_id: int) -> 'Layer':
        return self.client.get_layer(self.path, layer_id)