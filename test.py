import unittest
import boto3
from consumer.connector import *
from consumer.worker import Worker
from main import *
import json

class TestConsumer(unittest.TestCase):
    # tests aws session

    def setUp(self) -> None:
        self.cred = get_credentials()
        self.session = get_aws_session(self.cred)
        self.s3 = self.session.resource(('s3'))
        self.s3_client = self.session.client('s3')
        self.ddb = get_ddb(self.session)
        self.bucket = get_bucket(self.s3, 'usu-cs5260-rp-dist')
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/699670510392/cs5260-requests'
        self.sqs_client = self.session.client('sqs')
        # return super().setUp()

    def load_json(self, filename):
        with open(filename) as json_file:
            return json.load(json_file)

    def test_get_aws_session(self):
        self.session = get_aws_session(self.cred)
        self.assertEqual(self.session.region_name, 'us-east-1')

    def test_get_bucket(self):
        self.bucket = get_bucket(self.s3, 'usu-cs5260-rp-dist')
        self.assertEqual(self.bucket.name, 'usu-cs5260-rp-dist')

    def test_get_ddb(self):
        self.db = get_ddb(self.session)
        self.assertTrue(self.ddb.Table)

    def test_get_requests(self):
        actual = get_requests(self.bucket)
        data = actual[0][1]
        self.assertTrue(data['requestId'])

    def test_get_requests_from_queue(self):
        expected_owner = 'john-jones'
        actual_owner = ''
        for k, r in get_requests_from_queue(self.sqs_client, self.queue_url):
            if r['widgetId'] == 'f2568720-583c-44da-ad63-4d8f13bfe04b':
                actual_owner = r['owner']
        self.assertEqual(actual_owner, expected_owner)

    # storage_strategy = s3 and request type = update
    def test_process_request(self):
        widget_id_to_process = 'f2568720-583c-44da-ad63-4d8f13bfe04b'
        expected_key = f'widgets/john-jones/{widget_id_to_process}.json'
        bucket_name = 'usu-cs5260-rp-web'
        request_to_process = ''
        for k, r in get_requests(self.bucket):
            if r['widgetId'] == widget_id_to_process:
                request_to_process = r
        
        wO = Worker(self.session, self.bucket, 's3', 's3')
        wO.process_request(request_to_process)
        self.assertTrue(self.s3_client.get_object(Bucket=bucket_name, Key=expected_key))
     
    def test_remove_from_bucket(self):
        widget_id_to_process = 'f2568720-583c-44da-ad63-4d8f13bfe04b'
        key_to_remove = f'widgets/john-jones/{widget_id_to_process}.json'
        remove_from_bucket(self.s3, self.bucket.name, key_to_remove)
        self.assertFalse(self.s3_client.get_object(Bucket=self.bucket.name, Key=key_to_remove))

    def test_remove_from_queue(self):
        widget_id_to_process = 'f2568720-583c-44da-ad63-4d8f13bfe04b'
        key_to_remove = f'widgets/john-jones/{widget_id_to_process}.json'
        remove_from_queue(self.sqs_client, self.queue_url, key_to_remove)
        
        result = True
        for k, v in get_requests_from_queue(self.sqs_client, self.queue_url):
            if v['widgetId'] == widget_id_to_process:
                result=False
        self.assertTrue(result)
        
        