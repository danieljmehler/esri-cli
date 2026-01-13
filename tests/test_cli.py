import pytest
from unittest.mock import Mock, patch, mock_open
import sys
import json
from io import StringIO
from cli import main


class TestCLI:
    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'folders', '--url', 'https://example.com'])
    def test_folders_command(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_folder1 = Mock()
        mock_folder1.name = 'folder1'
        mock_folder2 = Mock()
        mock_folder2.name = 'folder2'
        mock_services.folders = [mock_folder1, mock_folder2]
        mock_client.get_services.return_value = mock_services
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == ['folder1', 'folder2']

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'services', '--url', 'https://example.com'])
    def test_services_command_root(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.services = [Mock(name='service1'), Mock(name='service2')]
        # Fix: Mock objects need to return strings for .name attribute
        mock_services.services[0].name = 'service1'
        mock_services.services[1].name = 'service2'
        mock_client.get_services.return_value = mock_services
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == ['service1', 'service2']

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'services', '--folder', 'test_folder', '--url', 'https://example.com'])
    def test_services_command_folder(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_service1 = Mock()
        mock_service1.name = 'test_folder/service1'
        mock_service2 = Mock()
        mock_service2.name = 'test_folder/service2'
        mock_folder.services = [mock_service1, mock_service2]
        mock_client.get_folder.return_value = mock_folder
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == ['service1', 'service2']

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'folder', 'test_folder', '--url', 'https://example.com'])
    def test_folder_command(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'name': 'test_folder'}
        mock_client.get_folder.return_value = mock_folder
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'name': 'test_folder'}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'query', '--service', 'test_service', '--id', '0', '--url', 'https://example.com'])
    def test_query_command_root(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_service.data = {'displayField': 'NAME'}
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'displayField': 'NAME'}
        mock_layer.query.side_effect = lambda **kwargs: {'features': []}
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
        
        # The print statement should be in stderr, not captured
        output = json.loads(mock_stdout.getvalue())
        assert output == {'features': []}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'query', '--service', 'test_service', '--id', '0', '--format', 'pjson', '--output', 'test.json', '--url', 'https://example.com'])
    def test_query_with_output_file(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_service.data = {'displayField': 'NAME'}
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'displayField': 'NAME'}
        mock_layer.query.side_effect = lambda **kwargs: {'features': []}
        mock_client.get_layer.return_value = mock_layer
        
        with patch('builtins.open', mock_open()) as mock_file:
            main()
            
        mock_file.assert_called_once_with('test.json', 'w')

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'query', '--service', 'test_service', '--id', '0', '--format', 'kml', '--where', 'OBJECTID=1', '--url', 'https://example.com'])
    def test_convert_json_to_kml_polygon(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_service.data = {'displayField': 'NAME'}
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'displayField': 'NAME'}
        mock_layer.query.side_effect = lambda **kwargs: {
            'features': [{
                'geometry': {'type': 'Polygon', 'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
                'properties': {'NAME': 'Test Polygon', 'attr1': 'value1'}
            }]
        }
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert '<Polygon>' in output
        assert '<name>Test Polygon</name>' in output
        assert '<coordinates>0,0,0 1,0,0 1,1,0 0,1,0 0,0,0</coordinates>' in output

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'query', '--service', 'test_service', '--id', '0', '--format', 'geojson', '--url', 'https://example.com'])
    def test_query_geojson_format(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_service.data = {'displayField': 'NAME'}
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'displayField': 'NAME'}
        mock_layer.query.side_effect = lambda **kwargs: {'type': 'FeatureCollection', 'features': []}
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'type': 'FeatureCollection', 'features': []}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'query', '--service', 'test_service', '--id', '0', '--format', 'kml', '--url', 'https://example.com'])
    def test_query_command_kml_format(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_service.data = {'displayField': 'Name'}
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'displayField': 'Name'}
        mock_layer.query.side_effect = lambda **kwargs: {
            'features': [{
                'geometry': {'type': 'Point', 'coordinates': [-74.0, 40.0]},
                'properties': {'Name': 'Test Point', 'attr1': 'value1'}
            }]
        }
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in output
        assert '<kml xmlns="http://www.opengis.net/kml/2.2">' in output
        assert '<name>Test Point</name>' in output
        assert '<coordinates>-74.0,40.0</coordinates>' in output
        assert '<table border="1">' in output
        assert '<td>attr1</td><td>value1</td>' in output

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'query', '--service', 'test_service', '--id', '0', '--format', 'kml', '--where', 'OBJECTID=999', '--url', 'https://example.com'])
    def test_convert_json_to_kml_empty_features(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_service.data = {'displayField': 'NAME'}
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'displayField': 'NAME'}
        mock_layer.query.side_effect = lambda **kwargs: {'features': []}
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in output
        assert '<Document>' in output
        assert '</Document>' in output

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layer', '--service', 'test_service', '--url', 'https://example.com'])
    def test_layer_command_missing_id_and_name(self, mock_client_class):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('sys.exit') as mock_exit:
                main()
                mock_exit.assert_called_once_with(1)
        
        output = mock_stdout.getvalue()
        assert 'Error: either --id or --name is required for layer command' in output

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layer', '--service', 'test_service', '--id', '0', '--url', 'https://example.com'])
    def test_layer_command_by_id_root(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'id': 0, 'name': 'layer0'}
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'id': 0, 'name': 'layer0'}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layer', '--service', 'test_service', '--name', 'layer0', '--url', 'https://example.com'])
    def test_layer_command_by_name_root(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_layer = Mock()
        mock_layer.id = 0
        mock_layer.name = 'layer0'
        mock_service.layers = [mock_layer]
        mock_client.get_service.return_value = mock_service
        
        mock_layer_data = Mock()
        mock_layer_data.data = {'id': 0, 'name': 'layer0'}
        mock_client.get_layer.return_value = mock_layer_data
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'id': 0, 'name': 'layer0'}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layer', '--folder', 'test_folder', '--service', 'test_service', '--id', '0', '--url', 'https://example.com'])
    def test_layer_command_by_id_folder(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'services': [{'name': 'test_folder/test_service', 'type': 'MapServer'}]}
        mock_client.get_folder.return_value = mock_folder
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_client.get_service.return_value = mock_service
        
        mock_layer = Mock()
        mock_layer.data = {'id': 0, 'name': 'layer0'}
        mock_client.get_layer.return_value = mock_layer
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'id': 0, 'name': 'layer0'}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layer', '--service', 'nonexistent', '--id', '0', '--url', 'https://example.com'])
    def test_layer_command_service_not_found(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': []}
        mock_client.get_services.return_value = mock_services
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert 'Service nonexistent not found' in output

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layer', '--service', 'test_service', '--id', '999', '--url', 'https://example.com'])
    def test_layer_command_layer_not_found(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.layers = [Mock(id=0, name='layer0')]
        mock_client.get_service.return_value = mock_service
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert 'Layer 999 not found in service test_service' in output

    @patch('cli.EsriClient')
    def test_get_layer_from_folder_success(self, mock_client_class):
        from cli import get_layer_from_folder
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'services': [{'name': 'test_folder/test_service', 'type': 'MapServer'}]}
        mock_client.get_folder.return_value = mock_folder
        
        mock_service = Mock()
        mock_layer = Mock()
        mock_layer.id = 0
        mock_layer.name = 'layer0'
        mock_service.layers = [mock_layer]
        mock_client.get_service.return_value = mock_service
        
        mock_layer_obj = Mock()
        mock_client.get_layer.return_value = mock_layer_obj
        
        args = Mock()
        args.folder = 'test_folder'
        args.service = 'test_service'
        args.id = 0
        args.name = None
        
        result = get_layer_from_folder(args, mock_client)
        assert result == (mock_layer_obj, mock_service)

    @patch('cli.EsriClient')
    def test_get_layer_from_folder_service_not_found(self, mock_client_class):
        from cli import get_layer_from_folder
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'services': []}
        mock_client.get_folder.return_value = mock_folder
        
        args = Mock()
        args.folder = 'test_folder'
        args.service = 'nonexistent'
        args.id = 0
        args.name = None
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = get_layer_from_folder(args, mock_client)
            
        assert result == (None, None)
        assert 'Service nonexistent not found in folder test_folder' in mock_stdout.getvalue()

    @patch('cli.EsriClient')
    def test_get_service_path_root_success(self, mock_client_class):
        from cli import get_service_path
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        result = get_service_path(mock_client, None, 'test_service')
        assert result == 'test_service/MapServer'

    @patch('cli.EsriClient')
    def test_get_service_path_folder_success(self, mock_client_class):
        from cli import get_service_path
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'services': [{'name': 'test_folder/test_service', 'type': 'MapServer'}]}
        mock_client.get_folder.return_value = mock_folder
        
        result = get_service_path(mock_client, 'test_folder', 'test_service')
        assert result == 'test_folder/test_service/MapServer'

    @patch('cli.EsriClient')
    def test_get_service_path_not_found(self, mock_client_class):
        from cli import get_service_path
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': []}
        mock_client.get_services.return_value = mock_services
        
        with pytest.raises(ValueError, match="Service nonexistent not found"):
            get_service_path(mock_client, None, 'nonexistent')

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layers', '--service', 'test_service', '--url', 'https://example.com'])
    def test_handle_layers_command_root(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_layer1 = Mock()
        mock_layer1.id = 0
        mock_layer1.name = 'layer0'
        mock_layer2 = Mock()
        mock_layer2.id = 1
        mock_layer2.name = 'layer1'
        mock_service.layers = [mock_layer2, mock_layer1]  # Unsorted order
        mock_client.get_service.return_value = mock_service
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == [{'id': 0, 'name': 'layer0'}, {'id': 1, 'name': 'layer1'}]

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layers', '--folder', 'test_folder', '--service', 'test_service', '--url', 'https://example.com'])
    def test_handle_layers_command_folder(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'services': [{'name': 'test_folder/test_service', 'type': 'MapServer'}]}
        mock_client.get_folder.return_value = mock_folder
        
        mock_service = Mock()
        mock_layer = Mock()
        mock_layer.id = 0
        mock_layer.name = 'layer0'
        mock_service.layers = [mock_layer]
        mock_client.get_service.return_value = mock_service
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == [{'id': 0, 'name': 'layer0'}]

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'layers', '--service', 'nonexistent', '--url', 'https://example.com'])
    def test_handle_layers_command_service_not_found(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': []}
        mock_client.get_services.return_value = mock_services
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert 'Service nonexistent not found' in output

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'service', 'test_service', '--url', 'https://example.com'])
    def test_handle_service_command_root(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': [{'name': 'test_service', 'type': 'MapServer'}]}
        mock_client.get_services.return_value = mock_services
        
        mock_service = Mock()
        mock_service.data = {'name': 'test_service', 'type': 'MapServer'}
        mock_client.get_service.return_value = mock_service
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'name': 'test_service', 'type': 'MapServer'}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'service', 'test_service', '--folder', 'test_folder', '--url', 'https://example.com'])
    def test_handle_service_command_folder(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_folder = Mock()
        mock_folder.data = {'services': [{'name': 'test_folder/test_service', 'type': 'MapServer'}]}
        mock_client.get_folder.return_value = mock_folder
        
        mock_service = Mock()
        mock_service.data = {'name': 'test_service', 'type': 'MapServer'}
        mock_client.get_service.return_value = mock_service
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = json.loads(mock_stdout.getvalue())
        assert output == {'name': 'test_service', 'type': 'MapServer'}

    @patch('cli.EsriClient')
    @patch('sys.argv', ['cli.py', 'service', 'nonexistent', '--url', 'https://example.com'])
    def test_handle_service_command_not_found(self, mock_client_class):
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_services = Mock()
        mock_services.data = {'services': []}
        mock_client.get_services.return_value = mock_services
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            main()
            
        output = mock_stdout.getvalue()
        assert 'Service nonexistent not found' in output