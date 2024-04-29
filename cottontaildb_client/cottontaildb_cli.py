import argparse
from typing import Dict, List

from grpc import RpcError

from . import CottontailDBClient


def cli():
    parser = argparse.ArgumentParser(prog='cottontaildb-client')

    parser.add_argument('host', help='Cottontail DB host.')
    parser.add_argument('--port', help='Cottontail DB host port.', type=int, default=1865)

    args = parser.parse_args()

    with CottontailDBClient(args.host, args.port) as client:
        client.ping()

        command_parser = get_command_parser()

        running = True
        while running:
            try:
                command = input('> ')
            except EOFError:
                print()
                break
            parts = command.split()
            try:
                arguments = command_parser.parse_args(parts)
            except SystemExit:
                continue
            try:
                running = process_command(client, arguments)
            except RpcError as error:
                print(error)
                continue

        print('Goodbye!')


def get_command_parser():
    parser = argparse.ArgumentParser(prog='cottontaildb-client')
    subparsers = parser.add_subparsers(dest='command')

    # Schema
    parser_schema = subparsers.add_parser('schema', help='Schema related commands.')
    subparsers_schema = parser_schema.add_subparsers(dest='subcommand')
    # Schema all
    subparsers_schema.add_parser('all', help='List all schemas stored in Cottontail DB.')
    # Schema create
    parser_schema_create = subparsers_schema.add_parser('create', help='Create the schema with the given name.')
    parser_schema_create.add_argument('schema_name', help='Name of schema to create.')
    # Schema drop
    parser_schema_drop = subparsers_schema.add_parser('drop', help='Drops the schema with the given name.')
    parser_schema_drop.add_argument('schema_name', help='Name of schema to drop.')
    # Schema list entities
    parser_schema_list = subparsers_schema.add_parser('list', help='Lists all entities for a given schema.')
    parser_schema_list.add_argument('schema_name', help='Name of schema to list entities of.')

    # Entity
    parser_entity = subparsers.add_parser('entity', help='Entity related commands.')
    subparsers_entity = parser_entity.add_subparsers(dest='subcommand')
    # Entity create
    # parser_entity_create = subparsers_schema.add_parser('create', help='Creates a new entity in the database.')
    # parser_entity_create.add_argument('schema_name', help='Name of schema to create entity in.')
    # parser_entity_create.add_argument('entity_name', help='Name of entity to create.')
    # Entity drop
    parser_entity_drop = subparsers_entity.add_parser('drop', help='Drops the given entity from the database.')
    parser_entity_drop.add_argument('schema_name', help='Name of schema to drop entity from.')
    parser_entity_drop.add_argument('entity_name', help='Name of entity to drop.')
    # Entity about
    parser_entity_about = subparsers_entity.add_parser('about', help='Gives an overview of the entity and its columns.')
    parser_entity_about.add_argument('schema_name', help='Name of schema containing entity.')
    parser_entity_about.add_argument('entity_name', help='Name of entity to show details of.')
    # Entity Preview
    parser_entity_preview = subparsers_entity.add_parser('preview', help='Shows a preview of the entity\'s contents.')
    parser_entity_preview.add_argument('schema_name', help='Name of schema containing entity.')
    parser_entity_preview.add_argument('entity_name', help='Name of entity to show preview of.')
    parser_entity_preview.add_argument('--limit', help='Number of rows to show.', type=int, default=10)

    # System
    parser_system = subparsers.add_parser('system', help='System related commands.')
    subparsers_system = parser_system.add_subparsers(dest='subcommand')
    # Transactions
    subparsers_system.add_parser('transactions',
                                 help='Lists all ongoing transaction in the current Cottontail DB instance.')
    # Locks
    subparsers_system.add_parser('locks', help='Lists all locks in the current Cottontail DB instance.')

    # Stop / quit
    subparsers.add_parser('stop', help='Stop client and exit.')
    subparsers.add_parser('quit', help='Stop client and exit.')
    subparsers.add_parser('exit', help='Stop client and exit.')

    return parser


def process_command(client, args):
    command = args.command
    if command == 'stop' or command == 'quit' or command == 'exit':
        return False
    elif command == 'schema':
        schema(client, args)
    elif command == 'entity':
        entity(client, args)
    elif command == 'system':
        system(client, args)

    return True


def schema(client, args):
    command = args.subcommand
    if command == 'all':
        schemas = client.list_schemas()
        print('\n'.join(schemas))
    elif command == 'create':
        response = client.create_schema(args.schema_name)
        print(response)
    elif command == 'drop':
        response = client.drop_schema(args.schema_name)
        print(response)
    elif command == 'list':
        response = client.list_entities(args.schema_name)
        print(response)


def entity(client, args):
    command = args.subcommand
    response = None
    if command == 'drop':
        response = client.drop_entity(args.schema_name, args.entity_name)
    elif command == 'about':
        response = client.get_entity_details(args.schema_name, args.entity_name)
    elif command == 'preview':
        response = client.sample_entity(args.schema_name, args.entity_name, limit=args.limit)
    if response is not None:
        print(format_response(response))


def format_response(response) -> str:
    """Formats the response object as a string.

    @param response: The object to format.
    @return: The formatted response as a string.
    """
    if type(response) is list and all([type(item) is dict for item in response]) and len(response) > 0:
        return format_as_table(response)
    else:
        return response.__repr__()


def format_as_table(dict_list: List[Dict]) -> str:
    """Formats a list of dictionaries as a table.

    @param dict_list: The list of dictionaries to format.
    @return: The formatted table as a string.
    """
    # Determine the maximum length for each column
    column_widths = {}
    headers = dict_list[0].keys()
    for header in headers:
        max_length = max(len(str(item[header])) for item in dict_list)
        column_widths[header] = max(max_length, len(header))

    # Prepare the table rows
    table_rows = []
    header_row = ' | '.join([f"{header:<{column_widths[header]}}" for header in headers])
    table_rows.append(header_row)
    table_rows.append('-' * len(header_row))
    for item in dict_list:
        row = ' | '.join([f"{str(item[header]):<{column_widths[header]}}" for header in headers])
        table_rows.append(row)

    # Join the table rows and return as a string
    table = '\n'.join(table_rows)
    return table


def system(client, args):
    command = args.subcommand
    if command == 'transactions':
        response = client.list_transactions()
        print(response)
    elif command == 'locks':
        response = client.list_locks()
        print(response)
