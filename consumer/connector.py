from boto3.session import Session
import json


def get_aws_session(credentials):
    return Session(**credentials, region_name='us-east-1')

def get_bucket(s3, bucket_name):
    # get bucket object from s3
    for bucket in s3.buckets.all():
        if bucket.name == bucket_name:
            return bucket

def get_ddb(session):
    return session.resource('dynamodb', 'us-east-1')

def get_requests(bucket, limit=10):
    requests = []
    # get request from bucket and parse it to dict
    # get only 10
    for i, r in enumerate(bucket.objects.all()):
        if i == limit:
            return requests
        requests.append([r.key, json.loads(r.get()['Body'].read().decode('utf-8'))])

def get_requests_from_queue(sqs_client, queue_url, limit=10, wait_time=10):
    requests = []
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=limit,
        WaitTimeSeconds=wait_time,
    )
    for message in response.get("Messages", []):
        message_body = json.loads(message["Body"])
        requests.append([message['ReceiptHandle'], message_body])
    return requests

def add_to_bucket(s3_client, bucket_name, data, key):
    json_data = json.dumps(data)
    response = s3_client.put_object(Body=json_data, Bucket=bucket_name, Key=key)
    return response

def add_to_ddb(ddb, table_name, data):
    response = ddb.Table(table_name).put_item(Item=data)
    return response

def remove_from_ddb(ddb, table_name, key):
    response = ddb.Table(table_name).delete_item(Key=key)
    return response

def remove_from_bucket(s3_resource, bucket_name, key):
    delete_object = s3_resource.Object(bucket_name, key)
    return delete_object.delete()

def remove_from_queue(sqs_client, queue_url, key):
    response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=key)
    return response
