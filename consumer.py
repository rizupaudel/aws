from connector import *
from consumer_worker import Worker
import time
from log import log

def consumer(args, aws_credentials, request_bucket_name, table_name):
    session = get_aws_session(aws_credentials)
    
    s3 = session.resource(args.get('resource'))

    request_bucket = get_bucket(s3, request_bucket_name)

    if args.get('storage_strategy') == 'ddb':
        # get dynamodb session
        ddb = get_db(session)
    else:
        print(f"TODO: {args.get('storage_strategy')} storage strategy. :)")

    while(True):

        # widget_requests = get_one_requests(request_bucket, 1)
        widget_requests = get_requests(request_bucket)

        # process widget requests 
        if widget_requests:
            for wr in widget_requests:
                cO = Worker(s3, request_bucket, ddb, table_name)
                cO.add_to_queue(wr)
                cO.handle_requests()
                log.info(f'Processed: {wr[1].get("type").upper()}; {wr[1].get("widgetId")};')
        
        time.sleep(5)
        log.info('Sleeping for next 5 seconds.')

    print("-----------------------")
    # read data from dynamodb
    # print(get_db_data(ddb, 'widgets', 'f2568720-583c-44da-ad63-4d8f13bfe04b')['Item'])
