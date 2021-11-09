#To run the progam
# python main.py -ss ddb -r s3

import os
import argparse
from consumer.consumer import consumer
from configparser import ConfigParser

# Command line argument implementation
def get_args() -> dict:
    parser = argparse.ArgumentParser(description='Consumer: Process Widget Requests')
    parser.add_argument('-ss','--storage-strategy', help='Storage strategy', type=str, choices=['ddb', 's3'], required=True)
    parser.add_argument('-r','--resource', help='Resources to use', type=str, choices=['sqs', 's3'], required=True)
    parser.add_argument('-rbn','--request-bucket-name', help='Request Bucket Name', type=str)
    parser.add_argument('-sbn','--storage-bucket-name', help='Storage Bucket Name', type=str)
    parser.add_argument('-tn','--table-name', help='DynamoDB Table Name', type=str)
    parser.add_argument('-qu','--query-url', help='SQS Queue URL', type=str)

    args = parser.parse_args()
    return vars(args)

def get_credentials():
    credentials = {}
    aki = os.environ.get('aws_access_key_id')
    sak = os.environ.get('aws_secret_access_key')
    st = os.environ.get('aws_session_token')
    if aki and sak and st:
        credentials = {'aws_access_key_id': aki, 'aws_secret_access_key': sak, 'aws_session_token': st}
    else:
        config = ConfigParser()
        config.read('.config')
        credentials = dict(config['default'])
    
    return credentials


def main():
    args = get_args()
    aws_credentials = get_credentials()
    consumer(args, aws_credentials)


if __name__=='__main__':
    main()