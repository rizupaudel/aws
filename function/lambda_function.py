import json
import logging
import boto3
from botocore.exceptions import ClientError

'''
    module: that takes restful request, 
    extract widget request, and send it to sqs
    
'''

# checks the validity widget request that comes from the http request body
def valid_widget_request(widget_request):
    if widget_request.get('widgetId'):
        return True
    return False

# check if the restful request is valid for our application or not
# def validate_event(event):
#     try:
#         widget_request = event['body']
#         if valid_widget_request(widget_request):
#             return True
#     except:
#         return False
#     return False

def get_valid_widget_request(widget_request):
    if isinstance(widget_request, str):
        widget_request = json.loads(widget_request)
    return widget_request

def make_message_body(widget_request):
    return json.dumps(widget_request)

# send the message to sqs
def send_sqs_message(queue_name, msg_body):
    sqs_client = boto3.client('sqs')
    sqs_queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    msg_body = make_message_body(msg_body)
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body)
    except ClientError as e:
        return (400, e)
    return (200, msg)

# main lambda handler
def lambda_handler(event, context):
    response = (400, 'Unknown Error!')
    queue_name = 'cs5260-requests'
    
    widget_request = event['body']
    
    widget_request = json.loads(widget_request) if isinstance(widget_request, str) else widget_request
    
    if valid_widget_request(widget_request):
        # response = send_sqs_message(queue_name, widget_request)
        pass
    else:
        response = (400, 'Invalid Widget Request!')
    
    return {
        'statusCode': response[0],
        'body': response[1]
    }
