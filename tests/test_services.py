from unittest.mock import Mock
from src.esri_client import Services


class TestServices:
    def test_init(self):
        mock_client = Mock()
        data = {
            'folders': ['folder1', 'folder2'],
            'services': [{'name': 'service1'}, {'name': 'service2'}]
        }
        
        services = Services(data, mock_client)
        
        assert len(services.folders) == 2
        assert len(services.services) == 2
        assert services.data == data