# Cottontail DB gRPC Python Client

[![pypi](https://img.shields.io/pypi/v/cottontaildb-client.svg)](https://pypi.org/project/cottontaildb-client/)
[![Python package workflow](https://github.com/Spiess/cottontaildb-python-client/actions/workflows/python-package.yml/badge.svg)](https://github.com/Spiess/cottontaildb-python-client/actions/workflows/python-package.yml)

A Cottontail DB gRPC client for Python. Built with [Cottontail DB Proto](https://github.com/vitrivr/cottontaildb-proto)
version `0.13.0`. Comes with an interactive CLI for remote DB access.

## Installation

Clone and install locally, or with `pip install cottontaildb-client`.

## Usage

Running the interactive CLI is as easy as `cottontaildb-client [--port PORT] host`.

Example usage in scripts:

```python
from cottontaildb_client import CottontailDBClient, Type, Literal, Null, column_def

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
        [Literal(stringData='test_null'), Literal(nullData=Null())]
    ]
    client.insert_batch('example_schema', 'example_entity', columns, values)
```
