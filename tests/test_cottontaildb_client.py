from unittest import TestCase

from grpc import RpcError

from cottontaildb_client import CottontailDBClient, column_def, Type, Literal
from cottontaildb_client.cottontail_pb2 import Where, AtomicBooleanPredicate, ColumnName, AtomicBooleanOperand, \
    Literals, ComparisonOperator

DB_HOST = 'localhost'
DB_PORT = 1865

TEST_SCHEMA = 'schema_test'
TEST_ENTITY = 'entity_test'
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
        if TEST_SCHEMA in [s.split('.')[-1] for s in self.client.list_schemas()]:
            self.client.drop_schema(TEST_SCHEMA)
        self.client.close()

    def test_create_drop_schema(self):
        self._create_schema()
        self.assert_in(TEST_SCHEMA, self.client.list_schemas(), 'schema was not created')
        self.client.create_schema(TEST_SCHEMA, exist_ok=True)
        self.client.drop_schema(TEST_SCHEMA)
        self.assert_not_in(TEST_SCHEMA, self.client.list_schemas(), 'schema was not dropped')

    def test_create_drop_entity(self):
        self._create_schema()
        self._create_entity()
        self.assert_in(TEST_ENTITY, self.client.list_entities(TEST_SCHEMA), 'entity was not created')
        self.client.create_entity(TEST_SCHEMA, TEST_ENTITY, [], exist_ok=True)
        self.client.drop_entity(TEST_SCHEMA, TEST_ENTITY)
        self.assert_not_in(TEST_ENTITY, self.client.list_entities(TEST_SCHEMA), 'entity was not dropped')

    def test_insert(self):
        self._create_schema()
        self._create_entity()
        self._insert()
        details = self.client.get_entity_details(TEST_SCHEMA, TEST_ENTITY)
        self.assertEqual(details['rows'], 1, 'unexpected number of rows in entity after insert')

    def test_batch_insert(self):
        self._create_schema()
        self._create_entity()
        self._batch_insert()
        details = self.client.get_entity_details(TEST_SCHEMA, TEST_ENTITY)
        self.assertEqual(details['rows'], 3, 'unexpected number of rows in entity after batch insert')

    def test_transaction_commit(self):
        self._create_schema()
        self._create_entity()
        self.client.start_transaction()
        self._insert()
        self.client.commit_transaction()
        details = self.client.get_entity_details(TEST_SCHEMA, TEST_ENTITY)
        self.assertEqual(details['rows'], 1, 'unexpected number of rows in entity after committed insert')

    def test_transaction_abort(self):
        self._create_schema()
        self._create_entity()
        self.client.start_transaction()
        self._insert()
        details = self.client.get_entity_details(TEST_SCHEMA, TEST_ENTITY)
        self.assertEqual(details['rows'], 1, 'unexpected number of rows in entity after transaction insert')
        self.client.abort_transaction()
        details = self.client.get_entity_details(TEST_SCHEMA, TEST_ENTITY)
        self.assertEqual(details['rows'], 0, 'unexpected number of rows in entity after aborted insert')

    def test_delete(self):
        self._create_schema()
        self._create_entity()
        self._insert()
        where = Where(atomic=AtomicBooleanPredicate(left=ColumnName(name=TEST_COLUMN_VALUE), right=AtomicBooleanOperand(
            literals=Literals(literal=[Literal(intData=0)])), op=ComparisonOperator.EQUAL))
        self.client.delete(TEST_SCHEMA, TEST_ENTITY, where)
        details = self.client.get_entity_details(TEST_SCHEMA, TEST_ENTITY)
        self.assertEqual(details['rows'], 0, 'unexpected number of rows in entity after delete')

    def assert_in(self, name, names, message):
        """Shortcut to test if the name of a database object is contained in a list of fully qualified names."""
        self.assertIn(name, [n.split('.')[-1] for n in names], message)

    def assert_not_in(self, name, names, message):
        """Shortcut to test if the name of a database object is not contained in a list of fully qualified names."""
        self.assertNotIn(name, [n.split('.')[-1] for n in names], message)

    def _create_schema(self):
        self.client.create_schema(TEST_SCHEMA)

    def _create_entity(self):
        columns = [
            column_def(TEST_COLUMN_ID, Type.STRING, nullable=False),
            column_def(TEST_COLUMN_VALUE, Type.INTEGER, nullable=False)
        ]
        self.client.create_entity(TEST_SCHEMA, TEST_ENTITY, columns)

    def _insert(self):
        values = {'id': Literal(stringData='test_0'), 'value': Literal(intData=0)}
        self.client.insert(TEST_SCHEMA, TEST_ENTITY, values)

    def _batch_insert(self):
        columns = ['id', 'value']
        values = [
            [Literal(stringData='test_1'), Literal(intData=1)],
            [Literal(stringData='test_2'), Literal(intData=2)],
            [Literal(stringData='test_3'), Literal(intData=3)]
        ]
        self.client.insert_batch(TEST_SCHEMA, TEST_ENTITY, columns, values)
