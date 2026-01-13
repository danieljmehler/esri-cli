from unittest.mock import Mock, patch
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
        # Mock both count query and actual query
        mock_client._get_json.side_effect = [
            {'count': 0},  # Count query response
            {'features': []}  # Actual query response
        ]
        
        layer = Layer({}, mock_client, 'service/path', 0)
        with patch('builtins.print'):
            result = layer.query(where="test=1")
        
        # Should be called twice: once for count, once for data
        assert mock_client._get_json.call_count == 2
        
        # Check count query call
        count_call = mock_client._get_json.call_args_list[0]
        expected_url = 'https://example.com/rest/services/service/path/0/query'
        expected_count_params = {'where': 'test=1', 'f': 'pjson', 'resultRecordCount': 100, 'returnCountOnly': 'true'}
        assert count_call[0][0] == expected_url
        assert count_call[0][1] == expected_count_params
        
        # Check data query call
        data_call = mock_client._get_json.call_args_list[1]
        expected_data_params = {'where': 'test=1', 'f': 'pjson', 'resultRecordCount': 100, 'resultOffset': 0}
        assert data_call[0][0] == expected_url
        assert data_call[0][1] == expected_data_params