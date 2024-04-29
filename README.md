# Cottontail DB gRPC Python Client

[![pypi](https://img.shields.io/pypi/v/cottontaildb-client.svg)](https://pypi.org/project/cottontaildb-client/)
[![Python package workflow](https://github.com/Spiess/cottontaildb-python-client/actions/workflows/python-package.yml/badge.svg)](https://github.com/Spiess/cottontaildb-python-client/actions/workflows/python-package.yml)

A Cottontail DB gRPC client for Python. Built with [Cottontail DB Proto](https://github.com/vitrivr/cottontaildb-proto)
version `0.14.3`. Comes with an interactive CLI for remote DB access.

Versions are numbered such that the first two numbers correspond with those of the compatible Cottontail DB Proto.

## Installation

Clone and install locally, or with `pip install cottontaildb-client`.

## Usage

Running the interactive CLI is as easy as `cottontaildb-client [--port PORT] HOST`.

Example usage in scripts:

```python
from cottontaildb_client import CottontailDBClient, Type, Literal, column_def

with CottontailDBClient('localhost', 1865) as client:
    # Create schema
    client.create_schema('example_schema')
    # Define entity columns
    columns = [
        column_def('id', Type.STRING, nullable=False),
        column_def('value', Type.INTEGER, nullable=True)
    ]
    # Create entity
    client.create_entity('example_schema', 'example_entity', columns)
    # Insert entry
    entry = {'id': Literal(stringData='test_1'), 'value': Literal(intData=1)}
    client.insert('example_schema', 'example_entity', entry)
    # Insert batch
    columns = ['id', 'value']
    values = [
        [Literal(stringData='test_10'), Literal(intData=10)],
        [Literal(stringData='test_20'), Literal(intData=20)],
        [Literal(stringData='test_null'), Literal()]
    ]
    client.insert_batch('example_schema', 'example_entity', columns, values)
```

## Developing

To update the gRPC client, regenerate `cottontaildb_pb2.py`, `cottontail_pb2.pyi`, and `cottontaildb_pb2_grpc.py` from the proto definitions
file in the [Cottontail DB](https://github.com/vitrivr/cottontaildb) repository.

The following is an approximate guide on how to do so from a terminal:

```bash
# Get the latest version of the Cottontail DB proto (and download to cottontaildb_client directory)
wget https://github.com/vitrivr/cottontaildb/raw/master/cottontaildb-client/src/main/protobuf/cottontail.proto -P ./cottontaildb_client/
# Install necessary python packages
pip install grpcio grpcio-tools
# Generate the gRPC client
python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./cottontaildb_client/cottontail.proto
```

It is important that the path to the `cottontail.proto` file reflects the location of the gRPC Python files, such that
the imports can be generated correctly.
