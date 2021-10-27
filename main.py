import logging as log
import argparse
import time
from connector import *
from configparser import ConfigParser
from consumer import Consumer

config = ConfigParser()

LOG_FILE = 'consumer.log'
LOG_FORMAT = '%(asctime)s %(filename)s: %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

log.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, datefmt=DATE_FORMAT, level=log.INFO)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description='Consumer: Process Widget Requests')

    parser.add_argument('-ss', '--storage-strategy', help='Storage strategy', type=str, required=True)
    parser.add_argument('-r', '--resource', help='Resources to use', type=str, required=True)

    args = parser.parse_args()
    return vars(args)


def main():
    # print(get_args())
    # log.warning("information is read")
    # print("information is read")

    config.read('.config')
    aws_credentials = dict(config['aws_credentials'])

    session = get_aws_session(aws_credentials)
    
    s3 = session.resource('s3')
    request_bucket_name = 'usu-cs5260-rp-requests'

    request_bucket = get_bucket(s3, request_bucket_name)

    # get dynamodb session
    ddb = get_db(session)

    while(True):
        # kasari tanne
        widget_requests = get_requests(request_bucket, 1)

        # process widget requests 
        if widget_requests:
            for wr in widget_requests:
                cO = Consumer(s3, request_bucket, ddb)
                cO.add_request_to_queue(wr)
                cO.handle_requests()
                log.info(f'Processed: request_type: {wr[1].get("type").upper()}; widget_id: {wr[1].get("widgetId")};')
        exit()
        time.sleep(5)

    print("-----------------------")
    # read data from dynamodb
    # print(get_db_data(ddb, 'widgets', 'f2568720-583c-44da-ad63-4d8f13bfe04b')['Item'])


if __name__=='__main__':
    main()