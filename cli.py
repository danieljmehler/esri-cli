#!/usr/bin/env python3
import sys
import json
import argparse
from src.esri_client import EsriClient
from requests.exceptions import RequestException, ConnectionError, Timeout, HTTPError

# Constants
DEFAULT_WHERE = '1=1'
DEFAULT_GEOMETRY_TYPE = 'esriGeometryEnvelope'
DEFAULT_SPATIAL_REL = 'esriSpatialRelIntersects'
DEFAULT_UNITS = 'esriSRUnit_Foot'
DEFAULT_ENCODING = 'esriDefault'
DEFAULT_FORMAT = 'pjson'

def add_common_args(parser):
    """Add common arguments to a parser.
    
    Args:
        parser: ArgumentParser to add arguments to
    """
    parser.add_argument('--url', required=True, help='Base URL of the ArcGIS server')
    parser.add_argument('--output', help='Output file path')

def add_service_args(parser):
    """Add service-related arguments to a parser.
    
    Args:
        parser: ArgumentParser to add arguments to
    """
    parser.add_argument('--folder', help='Folder name')
    parser.add_argument('--service', required=True, help='Service name')

def add_layer_args(parser):
    """Add layer identification arguments to a parser.
    
    Args:
        parser: ArgumentParser to add arguments to
    """
    parser.add_argument('--id', type=int, help='Layer ID')
    parser.add_argument('--name', help='Layer name')

def main():
    """Main entry point for the CLI application.
    
    Sets up argument parsing and dispatches to command handlers.
    """
    parser = argparse.ArgumentParser(description='ESRI ArcGIS REST API CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands', required=True)
    
    # folders command
    folders_parser = subparsers.add_parser('folders', help='List all folders')
    add_common_args(folders_parser)

    # folder command
    folder_parser = subparsers.add_parser('folder', help='Get folder details')
    folder_parser.add_argument('folder_name', help='Folder name')
    add_common_args(folder_parser)
    
    # services command
    services_parser = subparsers.add_parser('services', help='List services')
    add_common_args(services_parser)
    services_parser.add_argument('--folder', help='Folder name')

    # service command
    service_parser = subparsers.add_parser('service', help='Get service details')
    service_parser.add_argument('service_name', help='Service name')
    add_common_args(service_parser)
    service_parser.add_argument('--folder', help='Folder name')
    
    # layers command
    layers_parser = subparsers.add_parser('layers', help='List layers in a service')
    add_common_args(layers_parser)
    add_service_args(layers_parser)
    
    # layer command
    layer_parser = subparsers.add_parser('layer', help='Get layer details')
    add_common_args(layer_parser)
    add_service_args(layer_parser)
    add_layer_args(layer_parser)
    
    # query command
    query_parser = subparsers.add_parser('query', help='Query a layer')
    add_common_args(query_parser)
    add_service_args(query_parser)
    add_layer_args(query_parser)
    query_parser.add_argument('--where', default=DEFAULT_WHERE, help='Where clause')
    query_parser.add_argument('--text', help='Text search')
    query_parser.add_argument('--objectIds', help='Object IDs')
    query_parser.add_argument('--time', help='Time')
    query_parser.add_argument('--timeRelation', help='Time relation')
    query_parser.add_argument('--geometry', help='Geometry')
    query_parser.add_argument('--geometryType', default=DEFAULT_GEOMETRY_TYPE, help='Geometry type')
    query_parser.add_argument('--inSR', help='Input spatial reference')
    query_parser.add_argument('--spatialRel', default=DEFAULT_SPATIAL_REL, help='Spatial relationship')
    query_parser.add_argument('--distance', help='Distance')
    query_parser.add_argument('--units', default=DEFAULT_UNITS, help='Units')
    query_parser.add_argument('--relationParam', help='Relation parameter')
    query_parser.add_argument('--outFields', default='', help='Output fields')
    query_parser.add_argument('--returnGeometry', default='true', help='Return geometry')
    query_parser.add_argument('--returnTrueCurves', default='false', help='Return true curves')
    query_parser.add_argument('--maxAllowableOffset', help='Max allowable offset')
    query_parser.add_argument('--geometryPrecision', help='Geometry precision')
    query_parser.add_argument('--outSR', help='Output spatial reference')
    query_parser.add_argument('--havingClause', help='Having clause')
    query_parser.add_argument('--returnIdsOnly', default='false', help='Return IDs only')
    query_parser.add_argument('--returnCountOnly', default='false', help='Return count only')
    query_parser.add_argument('--orderByFields', help='Order by fields')
    query_parser.add_argument('--groupByFieldsForStatistics', help='Group by fields for statistics')
    query_parser.add_argument('--outStatistics', help='Output statistics')
    query_parser.add_argument('--returnZ', default='false', help='Return Z values')
    query_parser.add_argument('--returnM', default='false', help='Return M values')
    query_parser.add_argument('--gdbVersion', help='Geodatabase version')
    query_parser.add_argument('--historicMoment', help='Historic moment')
    query_parser.add_argument('--returnDistinctValues', default='false', help='Return distinct values')
    query_parser.add_argument('--resultOffset', help='Result offset')
    query_parser.add_argument('--resultRecordCount', help='Records per page')
    query_parser.add_argument('--returnExtentOnly', default='false', help='Return extent only')
    query_parser.add_argument('--sqlFormat', help='SQL format')
    query_parser.add_argument('--datumTransformation', help='Datum transformation')
    query_parser.add_argument('--parameterValues', help='Parameter values')
    query_parser.add_argument('--rangeValues', help='Range values')
    query_parser.add_argument('--quantizationParameters', help='Quantization parameters')
    query_parser.add_argument('--featureEncoding', default=DEFAULT_ENCODING, help='Feature encoding')
    query_parser.add_argument('--format', default=DEFAULT_FORMAT, help='Output format (pjson, geojson, or kml)')
    
    args = parser.parse_args()
    
    client = EsriClient(args.url)
    
    try:
        command_handlers = {
            'folders': handle_folders_command,
            'services': handle_services_command,
            'layers': handle_layers_command,
            'folder': handle_folder_command,
            'service': handle_service_command,
            'layer': handle_layer_command,
            'query': handle_query_command,
        }
        handler = command_handlers.get(args.command)
        if handler:
            handler(args, client)
    except ConnectionError as e:
        print(f"Connection Error: {e}")
        sys.exit(1)
    except Timeout as e:
        print(f"Timeout Error: {e}")
        sys.exit(1)
    except HTTPError as e:
        print(f"HTTP Error: {e}")
        sys.exit(1)
    except RequestException as e:
        print(f"Request Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)
        
def get_service_path(client, folder_name, service_name):
    """Get full service path from folder and service names.
    
    Args:
        client: EsriClient instance
        folder_name: Name of the folder (None for root)
        service_name: Name of the service
        
    Returns:
        str: Full service path string
        
    Raises:
        ValueError: If service is not found
    """
    if folder_name:
        folder = client.get_folder(folder_name)
        service_info = next((s for s in folder.data.get('services', []) 
                           if s['name'].replace(f"{folder_name}/", "") == service_name), None)
        if service_info:
            return f"{folder_name}/{service_name}/{service_info['type']}"
        raise ValueError(f"Service {service_name} not found in folder {folder_name}")
    else:
        services = client.get_services()
        service_info = next((s for s in services.data.get('services', []) 
                           if s['name'] == service_name), None)
        if service_info:
            return f"{service_name}/{service_info['type']}"
        raise ValueError(f"Service {service_name} not found")

def handle_folders_command(args, client):
    """Handle the folders command to list all folders.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    services = client.get_services()
    folders = [folder.name for folder in services.folders]
    output_result(folders, args)

def handle_services_command(args, client):
    """Handle the services command to list services in root or folder.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    if args.folder:
        folder = client.get_folder(args.folder)
        service_list = [service.name.replace(f"{args.folder}/", "") for service in folder.services]
    else:
        services = client.get_services()
        service_list = [service.name for service in services.services]
    output_result(service_list, args)

def handle_layers_command(args, client):
    """Handle the layers command to list layers in a service.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    if args.folder:
        folder = client.get_folder(args.folder)
        service_info = next((s for s in folder.data.get('services', []) if s['name'].replace(f"{args.folder}/", "") == args.service), None)
        if service_info:
            full_path = f"{args.folder}/{args.service}/{service_info['type']}"
            service = client.get_service(full_path)
            layer_list = sorted([{'id': layer.id, 'name': layer.name} for layer in service.layers], key=lambda x: x['id'])
            output_result(layer_list, args)
        else:
            print(f"Service {args.service} not found in folder {args.folder}")
    else:
        services = client.get_services()
        service_info = next((s for s in services.data.get('services', []) if s['name'] == args.service), None)
        if service_info:
            full_path = f"{args.service}/{service_info['type']}"
            service = client.get_service(full_path)
            layer_list = sorted([{'id': layer.id, 'name': layer.name} for layer in service.layers], key=lambda x: x['id'])
            output_result(layer_list, args)
        else:
            print(f"Service {args.service} not found")

def handle_folder_command(args, client):
    """Handle the folder command to get folder details.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    folder = client.get_folder(args.folder_name)
    output_result(folder.data, args)

def handle_service_command(args, client):
    """Handle the service command to get service details.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    if args.folder:
        folder = client.get_folder(args.folder)
        service_info = next((s for s in folder.data.get('services', []) if s['name'].replace(f"{args.folder}/", "") == args.service_name), None)
        if service_info:
            full_path = f"{args.folder}/{args.service_name}/{service_info['type']}"
            service = client.get_service(full_path)
            output_result(service.data, args)
        else:
            print(f"Service {args.service_name} not found in folder {args.folder}")
    else:
        services = client.get_services()
        service_info = next((s for s in services.data.get('services', []) if s['name'] == args.service_name), None)
        if service_info:
            full_path = f"{args.service_name}/{service_info['type']}"
            service = client.get_service(full_path)
            output_result(service.data, args)
        else:
            print(f"Service {args.service_name} not found")

def handle_layer_command(args, client):
    """Handle the layer command to get layer details.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    if args.id is None and not args.name:
        print("Error: either --id or --name is required for layer command")
        sys.exit(1)
    if args.folder:
        folder = client.get_folder(args.folder)
        service_info = next((s for s in folder.data.get('services', []) if s['name'].replace(f"{args.folder}/", "") == args.service), None)
        if service_info:
            full_path = f"{args.folder}/{args.service}/{service_info['type']}"
            service = client.get_service(full_path)
            if args.id is not None:
                layer = next((l for l in service.layers if l.id == args.id), None)
            else:
                layer = next((l for l in service.layers if l.name == args.name), None)
            if layer:
                layer_data = client.get_layer(full_path, layer.id)
                output_result(layer_data.data, args)
            else:
                identifier = args.id if args.id is not None else args.name
                print(f"Layer {identifier} not found in service {args.service}")
        else:
            print(f"Service {args.service} not found in folder {args.folder}")
    else:
        services = client.get_services()
        service_info = next((s for s in services.data.get('services', []) if s['name'] == args.service), None)
        if service_info:
            full_path = f"{args.service}/{service_info['type']}"
            service = client.get_service(full_path)
            if args.id is not None:
                layer = next((l for l in service.layers if l.id == args.id), None)
            else:
                layer = next((l for l in service.layers if l.name == args.name), None)
            if layer:
                layer_data = client.get_layer(full_path, layer.id)
                output_result(layer_data.data, args)
            else:
                identifier = args.id if args.id is not None else args.name
                print(f"Layer {identifier} not found in service {args.service}")
        else:
            print(f"Service {args.service} not found")

def handle_query_command(args, client):
    """Handle the query command to query a layer.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
    """
    if args.id is None and not args.name:
        print("Error: either --id or --name is required for query command")
        sys.exit(1)
    
    if args.folder:
        layer_obj = get_layer_from_folder(args, client)
    else:
        layer_obj = get_layer_from_root(args, client)
    
    if layer_obj:
        query_params = {k: v for k, v in vars(args).items() if k not in ['command', 'url', 'folder', 'service', 'id', 'name', 'output'] and v is not None}
        results = layer_obj.query(**query_params)
        output_result(results, args)

def get_layer_from_folder(args, client):
    """Get layer object from a folder service.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
        
    Returns:
        Layer object or None
    """
    folder = client.get_folder(args.folder)
    service_info = next((s for s in folder.data.get('services', []) if s['name'].replace(f"{args.folder}/", "") == args.service), None)
    if service_info:
        full_path = f"{args.folder}/{args.service}/{service_info['type']}"
        service = client.get_service(full_path)
        layer = find_layer_in_service(service, args)
        if layer:
            return client.get_layer(full_path, layer.id)
        else:
            identifier = args.id if args.id is not None else args.name
            print(f"Layer {identifier} not found in service {args.service}")
    else:
        print(f"Service {args.service} not found in folder {args.folder}")
    return None

def get_layer_from_root(args, client):
    """Get layer object from a root service.
    
    Args:
        args: Parsed command line arguments
        client: EsriClient instance
        
    Returns:
        Layer object or None
    """
    services = client.get_services()
    service_info = next((s for s in services.data.get('services', []) if s['name'] == args.service), None)
    if service_info:
        full_path = f"{args.service}/{service_info['type']}"
        service = client.get_service(full_path)
        layer = find_layer_in_service(service, args)
        if layer:
            return client.get_layer(full_path, layer.id)
        else:
            identifier = args.id if args.id is not None else args.name
            print(f"Layer {identifier} not found in service {args.service}")
    else:
        print(f"Service {args.service} not found")
    return None

def find_layer_in_service(service, args):
    """Find a layer in a service by ID or name.
    
    Args:
        service: Service object
        args: Parsed command line arguments
        
    Returns:
        Layer object or None
    """
    if args.id is not None:
        return next((l for l in service.layers if l.id == args.id), None)
    else:
        return next((l for l in service.layers if l.name == args.name), None)

def output_result(data, args):
    """Output result data to console or file.
    
    Args:
        data: Data to output
        args: Parsed command line arguments
    """
    if hasattr(args, 'format') and args.format == 'kml' and isinstance(data, dict) and 'features' in data:
        kml_content = convert_json_to_kml(data)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(kml_content)
        else:
            print(kml_content)
        return
    
    json_str = json.dumps(data, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_str)
    else:
        print(json_str)

def convert_json_to_kml(json_data):
    features = json_data.get('features', [])
    
    kml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>'
    ]
    
    for feature in features:
        placemark = create_kml_placemark(feature)
        if placemark:
            kml_parts.extend(placemark)
    
    kml_parts.extend(['</Document>', '</kml>'])
    return '\n'.join(kml_parts)

def create_kml_placemark(feature):
    geom = feature.get('geometry', {})
    props = feature.get('properties', {})
    
    name = get_feature_name(props)
    description = create_feature_description(props)
    
    if geom.get('type') == 'Point':
        return create_point_placemark(name, description, geom)
    elif geom.get('type') == 'Polygon':
        return create_polygon_placemark(name, description, geom)
    
    return None

def get_feature_name(props):
    for key, value in props.items():
        if key.lower() == 'name':
            return value
    return ''

def create_feature_description(props):
    table_rows = []
    for key, value in props.items():
        if key.lower() != 'name':
            table_rows.append(f'<tr><td>{key}</td><td>{value}</td></tr>')
    
    return f'<![CDATA[<table border="1"><tr><th>Attribute</th><th>Value</th></tr>{"".join(table_rows)}</table>]]>'

def create_point_placemark(name, description, geom):
    coords = geom.get('coordinates', [])
    if len(coords) >= 2:
        return [
            '<Placemark>',
            f'<name>{name}</name>',
            f'<description>{description}</description>',
            '<Point>',
            f'<coordinates>{coords[0]},{coords[1]}</coordinates>',
            '</Point>',
            '</Placemark>'
        ]
    return None

def create_polygon_placemark(name, description, geom):
    coords = geom.get('coordinates', [])
    if coords and len(coords) > 0:
        coord_str = ' '.join([f'{coord[0]},{coord[1]},0' for coord in coords[0]])
        return [
            '<Placemark>',
            f'<name>{name}</name>',
            f'<description>{description}</description>',
            '<Polygon>',
            '<outerBoundaryIs>',
            '<LinearRing>',
            f'<coordinates>{coord_str}</coordinates>',
            '</LinearRing>',
            '</outerBoundaryIs>',
            '</Polygon>',
            '</Placemark>'
        ]
    return None
if __name__ == '__main__':
    main()