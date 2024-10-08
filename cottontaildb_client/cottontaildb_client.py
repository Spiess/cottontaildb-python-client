from datetime import datetime, timezone
from typing import List

import grpc
from google.protobuf.empty_pb2 import Empty

from .cottontail_pb2 import SchemaName, CreateSchemaMessage, DropSchemaMessage, EntityName, ColumnDefinition, \
    CreateEntityMessage, InsertMessage, ColumnName, Scan, From, Type, ListSchemaMessage, ListEntityMessage, \
    EntityDetailsMessage, DropEntityMessage, TruncateEntityMessage, IndexName, IndexType, CreateIndexMessage, \
    DropIndexMessage, RebuildIndexMessage, UpdateMessage, DeleteMessage, Literal, Vector, FloatVector, \
    BatchInsertMessage, RequestMetadata, QueryMessage, Query, AnalyzeEntityMessage, Expression, FunctionName, Function, \
    Projection, Order
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
            self.start_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self._transaction:
            self.commit_transaction()
        self._channel.close()

    # Transactions

    def start_transaction(self):
        """Starts a transaction that all further changes will be associated with."""
        if self._transaction:
            raise Exception('Transaction already running!')
        self._transaction = True
        metadata = self._txn.Begin(Empty())
        self._tid = metadata.transactionId

    def commit_transaction(self):
        """Commits the current transaction."""
        if not self._transaction:
            raise Exception('No transaction running!')
        self._txn.Commit(RequestMetadata(transactionId=self._tid))
        self._tid = None
        self._transaction = False

    def abort_transaction(self):
        """Aborts the current transaction and rolls back work. Blocks if a query is ongoing."""
        if not self._transaction:
            raise Exception('No transaction running!')
        self._txn.Rollback(RequestMetadata(transactionId=self._tid))
        self._tid = None
        self._transaction = False

    def kill_transaction(self):
        """Kills the current transaction and rolls back work."""
        if not self._transaction:
            raise Exception('No transaction running!')
        self._txn.Kill(RequestMetadata(transactionId=self._tid))
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
        response = self._ddl.CreateSchema(
            CreateSchemaMessage(metadata=RequestMetadata(transactionId=self._tid), schema=schema_name))
        return self._parse_query_response(response)

    def drop_schema(self, schema):
        """Drops the schema with the given name."""
        schema_name = SchemaName(name=schema)
        response = self._ddl.DropSchema(
            DropSchemaMessage(metadata=RequestMetadata(transactionId=self._tid), schema=schema_name))
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
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.CreateEntity(
            CreateEntityMessage(metadata=RequestMetadata(transactionId=self._tid), entity=entity_name, columns=columns,
                                mayExist=exist_ok))
        return self._parse_query_response(response)

    def drop_entity(self, schema, entity, not_exist_ok=True):
        """Drops the given entity from the given schema."""
        if not_exist_ok and entity not in [s.split('.')[-1] for s in self.list_entities(schema)]:
            return
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.DropEntity(
            DropEntityMessage(metadata=RequestMetadata(transactionId=self._tid), entity=entity_name))
        return self._parse_query_response(response)

    def truncate_entity(self, schema, entity, not_exist_ok=True):
        """Truncates the specified entity."""
        if not_exist_ok and entity not in [s.split('.')[-1] for s in self.list_entities(schema)]:
            return
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.TruncateEntity(
            TruncateEntityMessage(metadata=RequestMetadata(transactionId=self._tid), entity=entity_name))
        return self._parse_query_response(response)

    def analyze_entity(self, schema, entity, async_=False):
        """Optimizes the specified entity."""
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        kwargs = {
            'async': async_
        }
        response = self._ddl.AnalyzeEntity(
            AnalyzeEntityMessage(metadata=RequestMetadata(transactionId=self._tid), entity=entity_name, **kwargs))
        return self._parse_query_response(response)

    def create_index(self, schema, entity, index, index_type: IndexType, columns: List[str], params=None):
        """
        Creates an index on a column.

        @param schema: name of the index's schema
        @param entity: name of the index's entity
        @param index: index name
        @param index_type: type of index
        @param columns: columns to build index for
        @param params: additional parameters for the index
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        response = self._ddl.CreateIndex(
            CreateIndexMessage(metadata=RequestMetadata(transactionId=self._tid), entity=entity_name, type=index_type,
                               indexName=index, columns=columns, params=params))
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
        response = self._ddl.DropIndex(
            DropIndexMessage(metadata=RequestMetadata(transactionId=self._tid), index=index_name))
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
        response = self._ddl.RebuildIndex(
            RebuildIndexMessage(metadata=RequestMetadata(transactionId=self._tid), index=index_name))
        return self._parse_query_response(response)

    def list_schemas(self):
        """Lists all schemas in the database."""
        responses = [response for response in
                     self._ddl.ListSchemas(ListSchemaMessage(metadata=RequestMetadata(transactionId=self._tid)))]
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
                     self._ddl.ListEntities(
                         ListEntityMessage(metadata=RequestMetadata(transactionId=self._tid), schema=schema_name))]
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
        response = self._ddl.EntityDetails(
            EntityDetailsMessage(metadata=RequestMetadata(transactionId=self._tid), entity=entity_name))
        entity_data = response.tuples[0]
        data_names = [c.name.name for c in response.columns]
        name_index = data_names.index('dbo')
        class_index = data_names.index('class')
        type_index = data_names.index('type')
        rows_index = data_names.index('rows')
        size_index = data_names.index('l_size')
        nullable_index = data_names.index('nullable')
        entity_details = {
            'name': entity_data.data[name_index].stringData,
            'rows': entity_data.data[rows_index].longData,
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

    def sample_entity(self, schema, entity, limit=10, skip=0):
        """
        Retrieves a preview of the specified entity.

        @param schema: the entity's schema
        @param entity: entity name
        @param limit: number of rows to return
        @param skip: number of rows to skip from the beginning
        @return: query response message
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        op = Projection.ProjectionOperation.SELECT
        column = ColumnName(entity=entity_name, name="*")
        elements = [Projection.ProjectionElement(expression=Expression(column=column))]
        projection = Projection(op=op, elements=elements)
        return self.query(schema, entity, projection, None, limit=limit, skip=skip)

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

        message = BatchInsertMessage(metadata=RequestMetadata(transactionId=self._tid), **kwargs)

        self._dml.InsertBatch(message)

    def update(self, schema, entity, where, updates):
        """
        Updates the rows in schema.entity selected through the where clause with the values from updates.

        @param schema: the schema containing the entity to update
        @param entity: the entity containing rows to update
        @param where: where clause selecting rows to update
        @param updates: dictionary of (column name, Literal value expression) key-value pairs to update selected rows
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_kwarg = {'from': From(scan=Scan(entity=entity_name))}
        updates_list = [UpdateMessage.UpdateElement(column=ColumnName(name=column), value=value)
                        for column, value in updates.items()]
        # TODO: Simplify where specification
        return self._dml.Update(
            UpdateMessage(metadata=RequestMetadata(transactionId=self._tid), **from_kwarg, where=where,
                          updates=updates_list))

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
        return self._dml.Delete(
            DeleteMessage(metadata=RequestMetadata(transactionId=self._tid), **from_kwarg, where=where))

    # Data query

    def ping(self):
        """Sends a ping message to the endpoint. If method returns without exception endpoint is connected."""
        self._dql.Ping(Empty())

    def nns(self, schema, entity, query_vector, distance='manhattan', limit=None, vector_col='feature', id_col='id'):
        """
        Queries the specified entity with the given vector.

        @param schema: the schema containing the queried entity
        @param entity: the entity being queried
        @param query_vector: the query vector. Simple float array.
        @param distance: the distance to be used
        @param limit: maximum number of rows to return
        @param vector_col: column name where the vector is stored
        @param id_col: column name where the id is stored
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        nns_col = Expression(column=ColumnName(entity=entity_name, name=vector_col))

        distance_col = ColumnName(name='distance')
        id_expression = Expression(column=ColumnName(name=id_col))

        nns_expression = Expression(literal=float_vector(*query_vector))
        fn = FunctionName(name=distance)
        fun = Function(name=fn, arguments=[nns_col, nns_expression])

        expression = Expression(function=fun)

        projection_element = Projection.ProjectionElement(alias=distance_col,
                                                          expression=expression)
        projection = Projection(op=Projection.ProjectionOperation.SELECT,
                                elements=[projection_element, Projection.ProjectionElement(expression=id_expression)])

        order_component = Order.Component(column=distance_col, direction=Order.Direction.ASCENDING)

        order = Order(components=[order_component])

        return self.query(schema, entity, projection, None, limit=limit, order=order)

    def query(self, schema, entity, projection, where, order=None, limit=None, skip=None, from_=None):
        """
        Queries the specified entity where the provided conditions are met and applies the given projection.

        @param schema: the schema containing the queried entity
        @param entity: the entity being queried
        @param projection: the projection to be applied to the result
        @param where: where clause specifying the rows to return
        @param order: order by clause specifying the order of the result
        @param limit: maximum number of rows to return
        @param skip: number of rows to skip
        @param from_: from clause, defaults to scan of the entity
        """
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_kwarg = {'from': from_ if from_ else From(scan=Scan(entity=entity_name))}
        query = Query(**from_kwarg, projection=projection, where=where, order=order, limit=limit, skip=skip)
        responses = self._dql.Query(QueryMessage(metadata=RequestMetadata(transactionId=self._tid), query=query))
        return [r for response in responses for r in self._parse_query_response(response)]

    @staticmethod
    def _parse_query_response(response):
        data_names = [c.name.name for c in response.columns]
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

        if literal.HasField('vectorData'):
            vector = literal.vectorData
            vector_types = [
                'float',
                'double',
                'int',
                'long',
                'bool',
                'complex32',
                'complex64'
            ]
            for vector_type in vector_types:
                if vector.HasField(vector_type):
                    return list(getattr(vector, vector_type).vector)

        # TODO: Object types
        # complex32Data
        # complex64Data
        return literal

    def _insert_helper(self, schema, entity, values):
        schema_name = SchemaName(name=schema)
        entity_name = EntityName(schema=schema_name, name=entity)
        from_kwarg = {'from': From(scan=Scan(entity=entity_name))}
        elements = [InsertMessage.InsertElement(column=ColumnName(name=column), value=value)
                    for column, value in values.items()]
        return InsertMessage(metadata=RequestMetadata(transactionId=self._tid), **from_kwarg, elements=elements)


def column_def(name: str, type_: Type, length: int = None, primary: bool = None, nullable: bool = None):
    """
    Creates a column definition.

    @param name: column name
    @param type_: column type
    @param length: data length for vector types
    @param primary: if this is a primary column of the entity
    @param nullable: if this column may be null
    @return: column definition
    """
    kwargs = {
        'name': ColumnName(name=name),
        'type': type_
    }
    if length is not None:
        kwargs['length'] = length
    if primary is not None:
        kwargs['primary'] = primary
    if nullable is not None:
        kwargs['nullable'] = nullable

    return ColumnDefinition(**kwargs)


def float_vector(*elements):
    return Literal(vectorData=Vector(float=FloatVector(vector=elements)))
