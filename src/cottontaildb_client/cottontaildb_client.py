import grpc
from google.protobuf.empty_pb2 import Empty

from .cottontail_pb2 import SchemaName, CreateSchemaMessage, DropSchemaMessage, EntityName, ColumnDefinition, \
    EntityDefinition, CreateEntityMessage, Engine, InsertMessage, ColumnName, Scan, From
from .cottontail_pb2_grpc import DDLStub, DMLStub, TXNStub


class CottontailDBClient:
    def __init__(self, host, port, with_transaction=False):
        self.host = host
        self.port = port
        self.transaction = with_transaction
        self.tid = None

    def __enter__(self):
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.ddl = DDLStub(self.channel)
        self.dml = DMLStub(self.channel)
        self.txn = TXNStub(self.channel)
        if self.transaction:
            self.tid = self.txn.Begin(Empty())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.transaction:
            self.txn.Commit(self.tid)
        self.channel.close()

    # Transactions

    def start_transaction(self):
        if self.transaction:
            raise Exception('Transaction already running!')
        self.transaction = True
        self.tid = self.txn.Begin(Empty())

    def commit_transaction(self):
        if not self.transaction:
            raise Exception('No transaction running!')
        self.txn.Commit(self.tid)
        self.tid = None
        self.transaction = False

    def abort_transaction(self):
        if not self.transaction:
            raise Exception('No transaction running!')
        self.txn.Rollback(self.tid)
        self.tid = None
        self.transaction = False

    # Data definition

    def create_schema(self, name):
        schema_name = SchemaName(name=name)
        self.ddl.CreateSchema(CreateSchemaMessage(txId=self.tid, schema=schema_name))

    def drop_schema(self, name):
        schema_name = SchemaName(name=name)
        self.ddl.DropSchema(DropSchemaMessage(schema=schema_name))

    def create_entity(self, schema, name, columns):
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=name)
        columns_definitions = [ColumnDefinition(engine=Engine.MAPDB, **column) for column in columns]
        entity = EntityDefinition(entity=entity_name, columns=columns_definitions)
        self.ddl.CreateEntity(CreateEntityMessage(txId=self.tid, definition=entity))

    # Data management

    def insert_entry(self, schema, entity, values):
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        elements = [
            InsertMessage.InsertElement(column=ColumnName(name=column_name), value=value) for
            column_name, value in values
        ]
        return self.dml.Insert(
            InsertMessage(txId=self.tid, **{'from': From(scan=Scan(entity=entity_name))}, inserts=elements))
