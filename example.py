from src.esri_client import EsriClient

# Example usage
client = EsriClient("https://hazards.fema.gov/arcgis")

# Get all services
services = client.get_services()
print(f"Found {len(services.services)} services and {len(services.folders)} folders")

# Get a specific folder
kmz_folder = client.get_folder("KMZ")
print(f"KMZ folder has {len(kmz_folder.services)} services")

# Get a specific service
service = client.get_service("MapSearch/MapSearch_v5/MapServer")
print(f"Service '{service.name}' has {len(service.layers)} layers")

# Get and query a layer
layer = service.get_layer(0)
results = layer.query(where="1=1", returnGeometry=True, resultRecordCount=10)
print(f"Query returned {len(results.get('features', []))} features")