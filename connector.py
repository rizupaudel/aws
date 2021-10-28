from boto3.session import Session
import json


def get_aws_session(credentials):
    return Session(**credentials)

def get_bucket(s3, name):
    # get bucket object from s3
    for bucket in s3.buckets.all():
        if bucket.name == name:
            return bucket

def get_db(session):
    return session.resource('dynamodb', 'us-east-1')

def get_db_data(db, table, id):
    return db.Table(table).get_item(Key={'id': id})

# def get_one_requests(bucket, limit=1):
#     requests = []
#     # get request from bucket and parse it to dict
#     for r in bucket.objects.limit(limit):
#         requests.append([r.key, json.loads(r.get()['Body'].read().decode('utf-8'))])
#     return requests

def get_requests(bucket):
    requests = []
    # get request from bucket and parse it to dict
    for r in bucket.objects.all():
        requests.append([r.key, json.loads(r.get()['Body'].read().decode('utf-8'))])
    return requests

def delete_request(s3, bucket_name, key):
    delete_object = s3.Object(bucket_name, key)
    return delete_object.delete()