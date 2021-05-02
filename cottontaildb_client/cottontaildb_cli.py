import argparse

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
        print(schemas)
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
    if command == 'drop':
        response = client.drop_entity(args.schema_name, args.entity_name)
        print(response)
    elif command == 'about':
        response = client.get_entity_details(args.schema_name, args.entity_name)
        print(response)


def system(client, args):
    command = args.subcommand
    if command == 'transactions':
        response = client.list_transactions()
        print(response)
    elif command == 'locks':
        response = client.list_locks()
        print(response)
