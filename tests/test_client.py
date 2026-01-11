import pytest
from unittest.mock import Mock, patch
from src.esri_client import EsriClient


class TestEsriClient:
    def test_init(self):
        client = EsriClient("https://example.com/")
        assert client.base_url == "https://example.com"

    @patch('src.esri_client.client.requests.Session')
    def test_get_json(self, mock_session):
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_session.return_value.get.return_value = mock_response
        
        client = EsriClient("https://example.com")
        result = client._get_json("test_url")
        
        assert result == {"test": "data"}
        mock_session.return_value.get.assert_called_once_with("test_url", params={'f': 'pjson'}, timeout=30)