from unittest import TestCase

from grpc import RpcError

from cottontaildb_client import CottontailDBClient, column_def, Type, Literal, float_vector
from cottontaildb_client.cottontail_pb2 import Where, ColumnName, Expression, Projection, IndexType, EntityName, \
    SchemaName, Predicate

DB_HOST = 'localhost'
DB_PORT = 1865

TEST_SCHEMA_STR = 'schema_test'
TEST_ENTITY_STR = 'entity_test'
TEST_VECTOR_ENTITY_STR = 'entity_test_vector'
TEST_SCHEMA_NAME = SchemaName(name=TEST_SCHEMA_STR)
TEST_ENTITY_NAME = EntityName(schema=TEST_SCHEMA_NAME, name=TEST_ENTITY_STR)
TEST_VECTOR_ENTITY_NAME = EntityName(schema=TEST_SCHEMA_NAME, name=TEST_VECTOR_ENTITY_STR)
TEST_INDEX = 'index_test'
TEST_COLUMN_ID = 'id'
TEST_COLUMN_VALUE = 'value'


class TestCottontailDBClient(TestCase):
    """
    Cottontail DB Client integration test.
    Requires empty default instance of Cottontail DB to be running on localhost:1865.
    """

    def setUp(self):
        self.client = CottontailDBClient(DB_HOST, DB_PORT)
        self.client.__enter__()
        try:
            self.client.ping()
        except RpcError:
            self.skipTest(f'error connecting to Cottontail DB at {DB_HOST}:{DB_PORT}')

    def tearDown(self):
        if TEST_SCHEMA_STR in [s.split('.')[-1] for s in self.client.list_schemas()]:
            self.client.drop_schema(TEST_SCHEMA_STR)
        self.client.close()

    def test_create_drop_schema(self):
        self._create_schema()
        self.assert_in(TEST_SCHEMA_STR, self.client.list_schemas(), 'schema was not created')
        self.client.create_schema(TEST_SCHEMA_STR, exist_ok=True)
        self.client.drop_schema(TEST_SCHEMA_STR)
        self.assert_not_in(TEST_SCHEMA_STR, self.client.list_schemas(), 'schema was not dropped')

    def test_create_drop_entity(self):
        self._create_schema()
        self._create_entity()
        self._create_vector_entity()
        self.assert_in(TEST_ENTITY_STR, self.client.list_entities(TEST_SCHEMA_STR), 'entity was not created')
        self.assert_in(TEST_VECTOR_ENTITY_STR, self.client.list_entities(TEST_SCHEMA_STR),
                       'vector entity was not created')
        self.client.create_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR, [], exist_ok=True)
        self.client.create_entity(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR, [], exist_ok=True)
        self.client.drop_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.client.drop_entity(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR)
        self.assert_not_in(TEST_ENTITY_STR, self.client.list_entities(TEST_SCHEMA_STR), 'entity was not dropped')
        self.assert_not_in(TEST_VECTOR_ENTITY_STR, self.client.list_entities(TEST_SCHEMA_STR),
                           'vector entity was not dropped')

    def test_drop_not_exists_entity(self):
        self._create_schema()
        result = self.client.drop_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR, not_exist_ok=True)
        self.assertIsNone(result, 'response received after dropping nonexistent entity')

    def test_truncate_not_exists_entity(self):
        self._create_schema()
        result = self.client.truncate_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR, not_exist_ok=True)
        self.assertIsNone(result, 'response received after truncating nonexistent entity')

    def test_create_truncate_entity(self):
        self._create_schema()
        self._create_entity()
        self.assert_in(TEST_ENTITY_STR, self.client.list_entities(TEST_SCHEMA_STR), 'entity was not created')
        self.client.truncate_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assert_in(TEST_ENTITY_STR, self.client.list_entities(TEST_SCHEMA_STR), 'entity was dropped')

    def test_insert(self):
        self._create_schema()
        self._create_entity()
        self._insert()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(1, details['rows'], 'unexpected number of rows in entity after insert')

    def test_vector_insert(self):
        self._create_schema()
        self._create_vector_entity()
        self._insert_vector()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR)
        self.assertEqual(details['rows'], 1, 'unexpected number of rows in vector entity after insert')

    def test_batch_insert(self):
        self._create_schema()
        self._create_entity()
        self._batch_insert()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(3, details['rows'], 'unexpected number of rows in entity after batch insert')

    def test_batch_insert_vectors(self):
        self._create_schema()
        self._create_vector_entity()
        self._batch_insert_vectors()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR)
        self.assertEqual(3, details['rows'], 'unexpected number of rows in entity after batch insert')

    def test_query(self):
        self._create_schema()
        self._create_entity()
        self._batch_insert()
        query_key = 'test_1'
        query_result = self._query_value_with_key(query_key)
        self.assertEqual(len(query_result), 1, 'unexpected number of rows returned from query')

    def test_sample_entity(self):
        self._create_schema()
        self._create_entity()
        self._batch_insert()
        sample = self.client.sample_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR, limit=2)
        should = [{'id': 'test_1', 'value': 1}, {'id': 'test_2', 'value': 2}]
        self.assertEqual(sample, should, 'unexpected preview result')

    def test_query_vectors(self):
        self._create_schema()
        self._create_vector_entity()
        self._batch_insert_vectors()
        query = [0.1, 0.2, 0.4]

        results = self.client.nns(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR, query, vector_col='value')
        self.assertEqual(len(results), 3, 'unexpected number of rows returned from query')
        # test with limit
        results = self.client.nns(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR, query, vector_col='value', limit=1)
        self.assertEqual(len(results), 1, 'unexpected number of rows returned from query')

    def test_update(self):
        self._create_schema()
        self._create_entity()
        self._insert()
        update_key = 'test_0'
        update_value = 5
        self._update_value_with_key(update_key, update_value)
        query_results = self._query_value_with_key(update_key)
        self.assertEqual(query_results[0][TEST_COLUMN_VALUE], update_value, 'value not correctly updated')

    def test_analyze(self):
        self._create_schema()
        self._create_entity()
        self._batch_insert()
        self.client.analyze_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR)

    def test_create_rebuild_drop_index(self):
        self._create_schema()
        self._create_entity()
        self._batch_insert()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(len(details['indexes']), 0, 'unexpected number of indexes in entity before index creation')
        self.client.create_index(TEST_SCHEMA_STR, TEST_ENTITY_STR, TEST_INDEX, IndexType.BTREE, [TEST_COLUMN_VALUE])
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(len(details['indexes']), 1, 'index was not created')
        self.client.rebuild_index(TEST_SCHEMA_STR, TEST_ENTITY_STR, TEST_INDEX)
        self.client.drop_index(TEST_SCHEMA_STR, TEST_ENTITY_STR, TEST_INDEX)
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(len(details['indexes']), 0, 'index was not dropped')

    def test_transaction_commit(self):
        self._create_schema()
        self._create_entity()
        self.client.start_transaction()
        self._insert()
        self.client.commit_transaction()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(details['rows'], 1, 'unexpected number of rows in entity after committed insert')

    def test_transaction_abort(self):
        self._create_schema()
        self._create_entity()
        self.client.start_transaction()
        self._insert()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(details['rows'], 1, 'unexpected number of rows in entity after transaction insert')
        self.client.abort_transaction()
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(details['rows'], 0, 'unexpected number of rows in entity after aborted insert')

    def test_delete(self):
        self._create_schema()
        self._create_entity()
        self._insert()
        where = Where(predicate=Predicate(
            comparison=Predicate.Comparison(lexp=Expression(column=ColumnName(name=TEST_COLUMN_VALUE)),
                                            operator=Predicate.Comparison.Operator.EQUAL,
                                            rexp=Expression(literal=Literal(intData=0)))))
        self.client.delete(TEST_SCHEMA_STR, TEST_ENTITY_STR, where)
        details = self.client.get_entity_details(TEST_SCHEMA_STR, TEST_ENTITY_STR)
        self.assertEqual(details['rows'], 0, 'unexpected number of rows in entity after delete')

    def assert_in(self, name, names, message):
        """Shortcut to test if the name of a database object is contained in a list of fully qualified names."""
        self.assertIn(name, [n.split('.')[-1] for n in names], message)

    def assert_not_in(self, name, names, message):
        """Shortcut to test if the name of a database object is not contained in a list of fully qualified names."""
        self.assertNotIn(name, [n.split('.')[-1] for n in names], message)

    def _create_schema(self):
        self.client.create_schema(TEST_SCHEMA_STR)

    def _create_entity(self):
        columns = [
            column_def(TEST_COLUMN_ID, Type.STRING, nullable=False),
            column_def(TEST_COLUMN_VALUE, Type.INTEGER, nullable=False)
        ]
        self.client.create_entity(TEST_SCHEMA_STR, TEST_ENTITY_STR, columns)

    def _create_vector_entity(self):
        columns = [
            column_def(TEST_COLUMN_ID, Type.STRING, nullable=False),
            column_def(TEST_COLUMN_VALUE, Type.FLOAT_VECTOR, length=3, nullable=False)
        ]
        self.client.create_entity(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR, columns)

    def _insert(self):
        values = {'id': Literal(stringData='test_0'), TEST_COLUMN_VALUE: Literal(intData=0)}
        self.client.insert(TEST_SCHEMA_STR, TEST_ENTITY_STR, values)

    def _insert_vector(self):
        value_list = [0.2, 0.3, 0.5]
        values = {'id': Literal(stringData='test_0'), TEST_COLUMN_VALUE: float_vector(*value_list)}
        self.client.insert(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR, values)

    def _batch_insert(self):
        columns = ['id', TEST_COLUMN_VALUE]
        values = [
            [Literal(stringData='test_1'), Literal(intData=1)],
            [Literal(stringData='test_2'), Literal(intData=2)],
            [Literal(stringData='test_3'), Literal(intData=3)]
        ]

        self.client.insert_batch(TEST_SCHEMA_STR, TEST_ENTITY_STR, columns, values)

    def _batch_insert_vectors(self):
        columns = ['id', TEST_COLUMN_VALUE]
        one = [0.1, 0.2, 0.3]
        two = [0.01, 0.02, 0.3]
        three = [0.9, 0.9, 0.9]
        values = [
            [Literal(stringData='test_1'), float_vector(*one)],
            [Literal(stringData='test_2'), float_vector(*two)],
            [Literal(stringData='test_3'), float_vector(*three)]
        ]
        self.client.insert_batch(TEST_SCHEMA_STR, TEST_VECTOR_ENTITY_STR, columns, values)

    def _update_value_with_key(self, key, value):
        where = Where(predicate=Predicate(
            comparison=Predicate.Comparison(lexp=Expression(column=ColumnName(name=TEST_COLUMN_ID)),
                                            operator=Predicate.Comparison.Operator.EQUAL,
                                            rexp=Expression(literal=Literal(stringData=key)))))
        updates = {TEST_COLUMN_VALUE: Expression(literal=Literal(intData=value))}
        self.client.update(TEST_SCHEMA_STR, TEST_ENTITY_STR, where, updates)

    def _query_value_with_key(self, key):
        expression = Expression(column=ColumnName(entity=TEST_ENTITY_NAME, name=TEST_COLUMN_VALUE))
        projection_element = Projection.ProjectionElement(expression=expression)
        projection = Projection(op=Projection.ProjectionOperation.SELECT, elements=[projection_element])
        where = Where(predicate=Predicate(
            comparison=Predicate.Comparison(lexp=Expression(column=ColumnName(name=TEST_COLUMN_ID)),
                                            operator=Predicate.Comparison.Operator.EQUAL,
                                            rexp=Expression(literal=Literal(stringData=key)))))
        return self.client.query(TEST_SCHEMA_STR, TEST_ENTITY_STR, projection, where)
