from datetime import datetime, timezone

import grpc
from google.protobuf.empty_pb2 import Empty
from typing import List

from .cottontail_pb2 import SchemaName, CreateSchemaMessage, DropSchemaMessage, EntityName, ColumnDefinition, \
    EntityDefinition, CreateEntityMessage, Engine, InsertMessage, ColumnName, Scan, From, Type, ListSchemaMessage, \
    ListEntityMessage, EntityDetailsMessage, DropEntityMessage, TruncateEntityMessage, OptimizeEntityMessage, \
    IndexName, IndexDefinition, IndexType, CreateIndexMessage, DropIndexMessage, RebuildIndexMessage, UpdateMessage, \
    DeleteMessage, Literal, Vector, FloatVector, BatchInsertMessage
from .cottontail_pb2_grpc import DDLStub, DMLStub, TXNStub, DQLStub


class CottontailDBClient:
    def __init__(self, host, port, with_transaction=False):
        self._host = host
        self._port = port
        self._transaction = with_transaction
        self._tid = None

    def __enter__(self):
        self._channel = grpc.insecure_channel(f'{self._host}:{self._port}')
        self._ddl = DDLStub(self._channel)
        self._dml = DMLStub(self._channel)
        self._txn = TXNStub(self._channel)
        self._dql = DQLStub(self._channel)
        if self._transaction:
            self._tid = self._txn.Begin(Empty())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._transaction:
            self._txn.Commit(self._tid)
        self._channel.close()

    # Transactions

    def start_transaction(self):
        """Starts a transaction that all further changes will be associated with."""
        if self._transaction:
            raise Exception('Transaction already running!')
        self._transaction = True
        self._tid = self._txn.Begin(Empty())

    def commit_transaction(self):
        """Commits the current transaction."""
        if not self._transaction:
            raise Exception('No transaction running!')
        self._txn.Commit(self._tid)
        self._tid = None
        self._transaction = False

    def abort_transaction(self):
        """Aborts the current transaction."""
        if not self._transaction:
            raise Exception('No transaction running!')
        self._txn.Rollback(self._tid)
        self._tid = None
        self._transaction = False

    def list_transactions(self):
        """Lists all active transactions."""
        responses = [response for response in self._txn.ListTransactions(Empty())]
        # TODO: Parse into Python data structure
        return [r for response in responses for r in self._parse_query_response(response)]

    def list_locks(self):
        """Lists all active locks on database objects."""
        responses = [response for response in self._txn.ListLocks(Empty())]
        # TODO: Parse into Python data structure
        return [r for response in responses for r in self._parse_query_response(response)]

    # Data definition

    def create_schema(self, schema, exist_ok=False):
        """
        Creates a new schema with the given name.

        @param schema: name of the entity's schema
        @param exist_ok: if the client should first check if the schema already exists
        @return: query response if there was a schema create attempt or None if exist_ok and schema already exists
        """
        if exist_ok and schema in [s.split('.')[-1] for s in self.list_schemas()]:
            return
        schema_name = SchemaName(name=schema)
        response = self._ddl.CreateSchema(CreateSchemaMessage(txId=self._tid, schema=schema_name))
        return self._parse_query_response(response)

    def drop_schema(self, schema):
        """Drops the schema with the given name."""
        schema_name = SchemaName(name=schema)
        response = self._ddl.DropSchema(DropSchemaMessage(txId=self._tid, schema=schema_name))
        return self._parse_query_response(response)

    def create_entity(self, schema, entity, columns, exist_ok=False):
        """
        Creates an entity in the given schema with the defined columns.

        Columns are defined by a list of column definitions, e.g.:
        columns = [column_def('id', Type.STRING, nullable=False)]

        @param schema: name of the entity's schema
        @param entity: entity name
        @param columns: list of ColumnDefinition objects defining the entity's columns
        @param exist_ok: if the client should first check if the entity already exists
        @return: query response if there was an entity create attempt or None if exist_ok and entity already exists
        """
        if exist_ok and entity in [s.split('.')[-1] for s in self.list_entities(schema)]:
            return
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        entity_def = EntityDefinition(entity=entity_name, columns=columns)
        response = self._ddl.CreateEntity(CreateEntityMessage(txId=self._tid, definition=entity_def))
        return self._parse_query_response(response)

    def drop_entity(self, schema, entity):
        """Drops the given entity from the given schema."""
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.DropEntity(DropEntityMessage(txId=self._tid, entity=entity_name))
        return self._parse_query_response(response)

    def truncate_entity(self, schema, entity):
        """Truncates the specified entity."""
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.DropEntity(TruncateEntityMessage(txId=self._tid, entity=entity_name))
        return self._parse_query_response(response)

    def optimize_entity(self, schema, entity):
        """Optimizes the specified entity."""
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.DropEntity(OptimizeEntityMessage(txId=self._tid, entity=entity_name))
        return self._parse_query_response(response)

    def create_index(self, schema, entity, index, index_type: IndexType, columns: List[str], rebuild: bool = False):
        """
        Creates an index on a column.

        @param schema: name of the index's schema
        @param entity: name of the index's entity
        @param index: index name
        @param index_type: type of index
        @param columns: columns to build index for
        @param rebuild: TODO
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        index_name = IndexName(entity=entity_name, name=index)
        # TODO: map<string,string> params
        column_names = [ColumnName(entity=entity_name, name=c) for c in columns]
        index_def = IndexDefinition(name=index_name, type=index_type, columns=column_names)
        response = self._ddl.CreateIndex(CreateIndexMessage(txId=self._tid, definition=index_def, rebuild=rebuild))
        return self._parse_query_response(response)

    def drop_index(self, schema, entity, index):
        """
        Drops the specified index.

        @param schema: name of the index's schema
        @param entity: name of the index's entity
        @param index: index name
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        index_name = IndexName(entity=entity_name, name=index)
        response = self._ddl.DropIndex(DropIndexMessage(txId=self._tid, index=index_name))
        return self._parse_query_response(response)

    def rebuild_index(self, schema, entity, index):
        """
        Rebuilds the specified index.

        @param schema: name of the index's schema
        @param entity: name of the index's entity
        @param index: index name
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        index_name = IndexName(entity=entity_name, name=index)
        response = self._ddl.RebuildIndex(RebuildIndexMessage(txId=self._tid, index=index_name))
        return self._parse_query_response(response)

    def list_schemas(self):
        """Lists all schemas in the database."""
        responses = [response for response in self._ddl.ListSchemas(ListSchemaMessage(txId=self._tid))]
        tuples = [t.data[0].stringData for response in responses for t in response.tuples]
        return tuples

    def list_entities(self, schema):
        """
        Lists all entities of the specified schema

        @param schema: schema of which to list entities
        @return: list of entity names
        """
        schema_name = SchemaName(name=schema)
        responses = [response for response in
                     self._ddl.ListEntities(ListEntityMessage(txId=self._tid, schema=schema_name))]
        tuples = [t.data[0].stringData for response in responses for t in response.tuples]
        return tuples

    def get_entity_details(self, schema, entity):
        """
        Retrieves details about an entity.

        @param schema: the entity's schema
        @param entity: entity name
        @return: dictionary containing entity details
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.EntityDetails(EntityDetailsMessage(txId=self._tid, entity=entity_name))
        entity_data = response.tuples[0]
        data_names = [c.name for c in response.columns]
        name_index = data_names.index('dbo')
        class_index = data_names.index('class')
        type_index = data_names.index('type')
        size_index = data_names.index('l_size')
        nullable_index = data_names.index('nullable')
        entity_details = {
            'name': entity_data.data[name_index].stringData,
            'rows': entity_data.data[data_names.index('rows')].intData,
            'columns': [
                {
                    'name': c.data[name_index].stringData,
                    'type': c.data[type_index].stringData,
                    'size': c.data[size_index].intData,
                    'nullable': c.data[nullable_index].booleanData
                } for c in response.tuples if c.data[class_index].stringData == 'COLUMN'
            ],
            'indexes': [
                {
                    'name': c.data[name_index].stringData,
                    'type': c.data[type_index].stringData
                } for c in response.tuples if c.data[class_index].stringData == 'INDEX'
            ]
        }

        return entity_details

    # Data management

    def insert(self, schema, entity, values):
        """
        Inserts column values into an entity.

        @param schema: name of the entity's schema
        @param entity: entity name
        @param values: dictionary of (column name, Literal value) key-value pairs
        @return: query response message
        """
        message = self._insert_helper(schema, entity, values)
        return self._dml.Insert(message)

    def insert_batch(self, schema, entity, columns, values):
        """
        Inserts column values into an entity in a batch.

        @param schema: name of the entity's schema
        @param entity: entity name
        @param columns: The names of the columns to insert values for (same length as values sub-lists)
        @param values: list of Literal value lists, where each sub-list contains for a value for each column
        @return: query response message
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        column_names = [ColumnName(name=column) for column in columns]
        inserts = [BatchInsertMessage.Insert(values=row) for row in values]

        kwargs = {
            'from': From(scan=Scan(entity=entity_name)),
            'columns': column_names,
            'inserts': inserts
        }

        message = BatchInsertMessage(txId=self._tid, **kwargs)

        self._dml.InsertBatch(message)

    def update(self, schema, entity, where, updates):
        """
        Updates the rows in schema.entity selected through the where clause with the values from updates.

        @param schema: the schema containing the entity to update
        @param entity: the entity containing rows to update
        @param where: where clause selecting rows to update
        @param updates: dictionary of (column name, Literal value) key-value pairs to update selected rows with
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_kwarg = {'from': From(scan=Scan(entity=entity_name))}
        updates_list = [UpdateMessage.UpdateElement(column=ColumnName(name=column), value=value)
                        for column, value in updates.items()]
        # TODO: Simplify where specification
        return self._dml.Update(UpdateMessage(txId=self._tid, **from_kwarg, where=where, updates=updates_list))

    def delete(self, schema, entity, where):
        """
        Deletes the rows in schema.entity selected through the where clause.

        @param schema: the schema containing the entity to delete
        @param entity: the entity containing rows to delete
        @param where: where clause selecting rows to delete
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_kwarg = {'from': From(scan=Scan(entity=entity_name))}
        # TODO: Simplify where specification
        return self._dml.Delete(DeleteMessage(txId=self._tid, **from_kwarg, where=where))

    # Data query

    def ping(self):
        """Sends a ping message to the endpoint. If method returns without exception endpoint is connected."""
        self._dql.Ping(Empty())

    # TODO: Query

    @staticmethod
    def _parse_query_response(response):
        data_names = [c.name for c in response.columns]
        return [
            {
                key: CottontailDBClient._parse_literal(value) for key, value in zip(data_names, item.data)
            } for item in response.tuples
        ]

    @staticmethod
    def _parse_literal(literal):
        data_types = [
            'booleanData',
            'intData',
            'longData',
            'floatData',
            'doubleData',
            'stringData'
        ]
        for data_type in data_types:
            if literal.HasField(data_type):
                return getattr(literal, data_type)

        if literal.HasField('dateData'):
            return datetime.fromtimestamp(literal.dateData.utc_timestamp / 1000.0, timezone.utc)
        if literal.HasField('nullData'):
            return None

        # TODO: Object types
        # complex32Data
        # complex64Data
        # vectorData
        return literal

    def _insert_helper(self, schema, entity, values):
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_kwarg = {'from': From(scan=Scan(entity=entity_name))}
        elements = [InsertMessage.InsertElement(column=ColumnName(name=column), value=value)
                    for column, value in values.items()]
        return InsertMessage(txId=self._tid, **from_kwarg, elements=elements)


def column_def(name: str, type_: Type, length: int = None, primary: bool = None, nullable: bool = None,
               engine: Engine = Engine.MAPDB):
    """
    Creates a column definition.

    @param name: column name
    @param type_: column type
    @param length: data length for vector types
    @param primary: if this is a primary column of the entity
    @param nullable: if this column may be null
    @param engine: storage engine to use (currently only MapDB)
    @return: column definition
    """
    kwargs = {
        'name': name,
        'type': type_,
        'engine': engine
    }
    if length is not None:
        kwargs['length'] = length
    if primary is not None:
        kwargs['primary'] = primary
    if nullable is not None:
        kwargs['nullable'] = nullable

    return ColumnDefinition(**kwargs)


def float_vector(*elements):
    return Literal(vectorData=Vector(floatVector=FloatVector(vector=elements)))
