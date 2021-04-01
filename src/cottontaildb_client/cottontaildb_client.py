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
        """Starts a transaction that all further changes will be associated with."""
        if self.transaction:
            raise Exception('Transaction already running!')
        self.transaction = True
        self.tid = self.txn.Begin(Empty())

    def commit_transaction(self):
        """Commits the current transaction."""
        if not self.transaction:
            raise Exception('No transaction running!')
        self.txn.Commit(self.tid)
        self.tid = None
        self.transaction = False

    def abort_transaction(self):
        """Aborts the current transaction."""
        if not self.transaction:
            raise Exception('No transaction running!')
        self.txn.Rollback(self.tid)
        self.tid = None
        self.transaction = False

    # Data definition

    def create_schema(self, name):
        """Creates a new schema with the given name."""
        schema_name = SchemaName(name=name)
        self.ddl.CreateSchema(CreateSchemaMessage(txId=self.tid, schema=schema_name))

    def drop_schema(self, name):
        """Drops the schema with the given name."""
        schema_name = SchemaName(name=name)
        self.ddl.DropSchema(DropSchemaMessage(schema=schema_name))

    def create_entity(self, schema, name, columns):
        """
        Creates an entity in the given schema with the defined columns.

        Columns are defined by a list of dictionaries containing all necessary parameters, e.g.:
        columns = [{'name': 'id', 'type': Type.STRING, 'nullable': False}]

        @param schema:
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=name)
        columns_definitions = [ColumnDefinition(engine=Engine.MAPDB, **column) for column in columns]
        entity = EntityDefinition(entity=entity_name, columns=columns_definitions)
        self.ddl.CreateEntity(CreateEntityMessage(txId=self.tid, definition=entity))

    # Data management

    def insert(self, schema, entity, values):
        """
        Inserts column values into an entity.

        @param schema: name of the entity's schema
        @param entity: entity name
        @param values: list of (column name, Literal value) tuples
        @return: query response message
        """
        message = self._insert_helper(schema, entity, values)
        return self.dml.Insert(message)

    def insert_batch(self, insert_iterator):
        """
        Inserts column values into entities in a batch.

        @param insert_iterator: iterator providing (schema, entity, values) triples containing the same information as
         required by non-batch insert
        """

        def insert_stream():
            for schema, entity, values in insert_iterator:
                yield self._insert_helper(schema, entity, values)

        for _ in self.dml.InsertBatch(insert_stream()):
            continue

    def _insert_helper(self, schema, entity, values):
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_arg = {'from': From(scan=Scan(entity=entity_name))}
        elements = [InsertMessage.InsertElement(column=ColumnName(name=column_name), value=value)
                    for column_name, value in values]
        return InsertMessage(txId=self.tid, **from_arg, inserts=elements)
