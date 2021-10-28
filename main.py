#To run the progam
# python main.py -ss ddb -r s3

import argparse
from configparser import ConfigParser
from consumer import consumer

config = ConfigParser()



# Command line argument implementation
def get_args() -> dict:
    parser = argparse.ArgumentParser(description='Consumer: Process Widget Requests')

    parser.add_argument('-ss','--storage-strategy', help='Storage strategy', type=str, required=True)
    parser.add_argument('-r','--resource', help='Resources to use', type=str, required=True)

    args = parser.parse_args()
    return vars(args)


def get_credentials():
    config.read('.config')
    return dict(config['aws_credentials'])


def main():
    args = get_args()
    request_bucket_name = 'usu-cs5260-rp-requests'
    table_name = 'widgets'
    aws_credentials = get_credentials()
    consumer(args, aws_credentials, request_bucket_name, table_name)


if __name__=='__main__':
    main()