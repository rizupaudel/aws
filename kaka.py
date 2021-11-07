import unittest
import boto3
from connector import *
from main import *
import json

cred = get_credentials()
session = get_aws_session(cred)
s3 = session.resource(('s3'))
# db = get_db(self.session)
# bucket = get_bucket(self.s3, 'usu-cs5260-rp-dist')
# usu-cs5260-rp-web
# return super().setUp()
