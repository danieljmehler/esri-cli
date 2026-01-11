from unittest.mock import Mock
from src.esri_client import Layer


class TestLayer:
    def test_init(self):
        mock_client = Mock()
        data = {'name': 'test_layer'}
        
        layer = Layer(data, mock_client, 'service/path', 0)
        
        assert layer.name == 'test_layer'
        assert layer.id == 0
        assert layer.service_path == 'service/path'

    def test_query(self):
        mock_client = Mock()
        mock_client.base_url = 'https://example.com'
        mock_client._get_json.return_value = {'features': []}
        
        layer = Layer({}, mock_client, 'service/path', 0)
        result = layer.query(where="test=1")
        
        expected_url = 'https://example.com/rest/services/service/path/0/query'
        expected_params = {'where': 'test=1', 'f': 'pjson', 'resultRecordCount': 100, 'resultOffset': 0}
        mock_client._get_json.assert_called_once_with(expected_url, expected_params)