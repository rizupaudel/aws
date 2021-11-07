import unittest
import boto3
from connector import *
from main import *
import json

class TestConsumer(unittest.TestCase):
    # tests aws session

    def setUp(self) -> None:
        self.cred = get_credentials()
        self.session = get_aws_session(self.cred)
        self.s3 = self.session.resource(('s3'))
        self.db = get_db(self.session)
        self.bucket = get_bucket(self.s3, 'usu-cs5260-rp-dist')
        # return super().setUp()

    def load_json(self, filename):
        with open(filename) as json_file:
            return json.load(json_file)

    def test_get_aws_session(self):
        self.session = get_aws_session(self.cred)
        self.assertEqual(self.session.region_name, 'us-east-1')

    def test_get_bucket(self):
        self.s3 = self.session.resource(('s3'))
        self.bucket = get_bucket(self.s3, 'usu-cs5260-rp-dist')
        self.assertEqual(self.bucket.name, 'usu-cs5260-rp-dist')

    def test_get_db(self):
        self.db = get_db(self.session)
        self.assertTrue(self.db.Table)

    def test_get_requests(self):
        actual = get_requests(self.bucket)
        data = actual[0][1]
        self.assertTrue(data['requestId'])
        # expected = self.load_json('tests/test1.json')
        # self.assertEqual(actual[0][1], expected)

    # def test_delete_request(self):
    #     temp_actual = delete_request('usu-cs5260-rp-dist')
    #     self.assertEqual(type(temp_actual.get('ResponseMetaData').get('HttpStatusCode')), int)


    # def test_get_db_data(self, table, id):
    #         actual = get_db_data(self.db, table, id)
    #         expected = {}
    #         self.assertEqual(actual, expected)