import grpc

from .cottontail_pb2 import SchemaName, CreateSchemaMessage
from .cottontail_pb2_grpc import DDLStub


class CottontailDBClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.ddl = DDLStub(self.channel)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()

    def create_schema(self, name):
        schema_name = SchemaName(name=name)
        self.ddl.CreateSchema(CreateSchemaMessage(schema=schema_name))
