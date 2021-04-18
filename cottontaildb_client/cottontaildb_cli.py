import argparse

from . import CottontailDBClient


def cli():
    parser = argparse.ArgumentParser()

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
            arguments = command_parser.parse_args(parts)
            running = process_command(client, arguments)

        print('Goodbye!')


def get_command_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # Schema
    parser_schema = subparsers.add_parser('schema', help='Schema related commands.')
    subparsers_schema = parser_schema.add_subparsers(dest='subcommand')

    subparsers_schema.add_parser('all', help='List all schemas stored in Cottontail DB.')

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

    return True


def schema(client, args):
    command = args.subcommand
    if command == 'all':
        schemas = client.list_schemas()
        print(schemas)
