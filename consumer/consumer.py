from consumer.connector import *
from consumer.worker import Worker
import time
from consumer.log import log

def consumer(args, aws_credentials):
    # arg parse
    request_bucket_name = args.get('request_bucket_name') if args.get('request_bucket_name') else 'usu-cs5260-rp-requests'
    storage_bucket_name = args.get('storage_bucket_name') if args.get('storage_bucket_name') else 'usu-cs5260-rp-web'
    table_name = args.get('table_name') if args.get('table_name') else 'widgets'
    queue_url = args.get('query_url') if args.get('query_url') else 'https://sqs.us-east-1.amazonaws.com/699670510392/cs5260-requests'
    storage_strategy = args.get('storage_strategy')
    requests_resource = args.get('resource')

    session = get_aws_session(aws_credentials)
    s3_resource = session.resource('s3')
    request_bucket = get_bucket(s3_resource, request_bucket_name)

    sqs_client = session.client('sqs')

    widget_requests = []
    
    while (True):
        if requests_resource == 's3':
            widget_requests = get_requests(request_bucket, 10)
        else:
            widget_requests = get_requests_from_queue(sqs_client, queue_url)
        
        if widget_requests:
            log.info(f'Fetched: {len(widget_requests)} requests from {requests_resource};')
        else:
            log.info(f'Fetching: requests from {requests_resource};')

        
        # process widget requests 
        if widget_requests:
            for wr in widget_requests:
                cO = Worker(session, request_bucket, storage_strategy, requests_resource)
                if requests_resource == 'sqs':
                    cO.set_sqs_resource_info(queue_url)
                else:
                    cO.set_s3_resource_info(request_bucket_name)
                
                if storage_strategy == 'ddb':
                    ddb = get_ddb(session)
                    cO.set_ddb_info(ddb, table_name)
                else:
                    cO.set_s3_storage_info(storage_bucket_name)

                cO.add_to_queue(wr)
                cO.handle_requests()
                log.info(f'Processed: {wr[1].get("type").upper()}; {wr[1].get("widgetId")};')
        
        time.sleep(5)
        log.info('Sleeping for next 5 seconds;')

    print("-----------------------")
