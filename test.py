import unittest
import boto3
from connector import *
from main import get_credentials

def test_get_aws_session():
	cred = get_credentials()
	session = get_aws_session(cred)
	
	return session
	

class TestConsumer(unittest.TestCase):
	def test_get_aws_session(self):
		cred = get_credentials()
		self.session = get_aws_session(cred)
		self.assertEqual(self.session.get('region_name'), 'us-east-1')


print(test_get_aws_session())