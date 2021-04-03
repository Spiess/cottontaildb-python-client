from unittest import TestCase

from cottontaildb_client import CottontailDBClient

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

    def tearDown(self):
        for s in self.client.list_schemas():
            self.client.drop_schema(s.split('.')[-1])
        self.client.close()

    def test_create_drop_schema(self):
        self.client.create_schema(TEST_SCHEMA)
        schemas = self.client.list_schemas()
        self.assertEqual(schemas[0].split('.')[-1], TEST_SCHEMA, 'schema was not created')
        self.client.drop_schema(TEST_SCHEMA)
        schemas = self.client.list_schemas()
        self.assertEqual(len(schemas), 0, 'schema was not dropped')
