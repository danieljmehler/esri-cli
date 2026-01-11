# ESRI Services API

A Python client and CLI tool for interacting with ESRI ArcGIS REST services.

## Installation

```bash
pip install -e .
```

## CLI Usage

The CLI provides commands to explore and query ESRI ArcGIS REST services.

### Basic Commands

**List all folders:**
```bash
esri-cli folders --url https://your-server.com
```

**Get folder details:**
```bash
esri-cli folder folder_name --url https://your-server.com
```

**List services (root):**
```bash
esri-cli services --url https://your-server.com
```

**List services in folder:**
```bash
esri-cli services --folder folder_name --url https://your-server.com
```

**Get service details:**
```bash
esri-cli service service_name --url https://your-server.com
esri-cli service service_name --folder folder_name --url https://your-server.com
```

**List layers in service:**
```bash
esri-cli layers --service service_name --url https://your-server.com
esri-cli layers --service service_name --folder folder_name --url https://your-server.com
```

**Get layer details:**
```bash
esri-cli layer --service service_name --id 0 --url https://your-server.com
esri-cli layer --service service_name --name layer_name --url https://your-server.com
```

### Query Features

**Basic query:**
```bash
esri-cli query --service service_name --id 0 --url https://your-server.com
```

**Query with WHERE clause:**
```bash
esri-cli query --service service_name --id 0 --where "OBJECTID < 10" --url https://your-server.com
```

**Export formats:**
```bash
# GeoJSON format
esri-cli query --service service_name --id 0 --format geojson --url https://your-server.com

# KML format
esri-cli query --service service_name --id 0 --format kml --url https://your-server.com
```

**Save to file:**
```bash
esri-cli query --service service_name --id 0 --output results.json --url https://your-server.com
```

**Pagination control:**
```bash
# Get specific page
esri-cli query --service service_name --id 0 --resultOffset 100 --resultRecordCount 50 --url https://your-server.com

# Auto-pagination (default behavior when no resultOffset specified)
esri-cli query --service service_name --id 0 --url https://your-server.com
```

### Advanced Query Parameters

The query command supports all ESRI REST API parameters:

```bash
esri-cli query --service service_name --id 0 \
  --where "STATE_NAME='California'" \
  --outFields "OBJECTID,STATE_NAME,POP2000" \
  --geometry "-118,34,-117,35" \
  --geometryType esriGeometryEnvelope \
  --spatialRel esriSpatialRelIntersects \
  --returnGeometry true \
  --url https://your-server.com
```

## Python API

```python
from src.esri_client import EsriClient

# Initialize client
client = EsriClient("https://your-server.com")

# Get services
services = client.get_services()
print([folder.name for folder in services.folders])

# Get service
service = client.get_service("service_name/MapServer")
print([layer.name for layer in service.layers])

# Query layer
layer = client.get_layer("service_name/MapServer", 0)
results = layer.query(where="OBJECTID < 10", format="geojson")
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd esri-services-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
pip install pytest pytest-cov pyinstaller
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run tests with coverage:**
```bash
pytest --cov=src --cov=cli --cov-report=html --cov-report=term
```

**View coverage report:**
```bash
open htmlcov/index.html  # On macOS
# Or navigate to htmlcov/index.html in your browser
```

### Building Executable

**Create standalone executable with PyInstaller:**
```bash
# Basic executable
pyinstaller --onefile cli.py

# With custom name and icon
pyinstaller --onefile --name esri-cli cli.py

# The executable will be in dist/
./dist/esri-cli --help
```

**PyInstaller options:**
- `--onefile`: Create single executable file
- `--name`: Custom executable name
- `--add-data`: Include additional files
- `--hidden-import`: Include modules not detected automatically

### Project Structure

```
esri-services-api/
├── src/
│   └── esri_client/
│       ├── __init__.py
│       ├── client.py
│       ├── services.py
│       ├── folder.py
│       ├── service.py
│       └── layer.py
├── tests/
│   ├── test_cli.py
│   └── test_client.py
├── cli.py
├── setup.py
├── requirements.txt
└── README.md
```

### Code Quality

**Run tests before committing:**
```bash
pytest --cov=src --cov=cli
```

**Check coverage threshold:**
- Aim for >90% test coverage
- All new features should include tests
- CLI commands should have integration tests