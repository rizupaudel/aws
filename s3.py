import json
import logging as log
import argparse

LOG_FILE = 'consumer.log'
LOG_FORMAT = '%(asctime)s %(filename)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

log.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def get_args() -> dict:
    parser = argparse.ArgumentParser(description='Consumer: Process Widget Requests')

    parser.add_argument('-ss', '--storage-strategy', help='Storage strategy', type=str, required=True)
    parser.add_argument('-r', '--resource', help='Resources to use', type=str, required=True)

    args = parser.parse_args()
    return vars(args)


json_content = '''{
"$schema": "http://json-schema.org/draft-04/schema#", "type": "object",
"properties": {
"type": {
"type": "string",
"pattern": "create|delete|update"
}, "requestId": {
"type": "string" },
"widgetId": { "type": "string"
}, "owner": {
"type": "string",
"pattern": "[A-Za-z ]+" },
"label": { "type": "string"
}, "description": {
"type": "string" },
"otherAttributes": { "type": "array", "items": [
{
"type": "object", "properties": {
"name": {
"type": "string"
}, "value": {
"type": "string" }
}, "required": [
"name",
"value" ]
} ]
} },
"required": [ "type",
"requestId", "widgetId", "owner"
]
}'''


def read_string_json(string_json:str) -> dict:
    return dict(json.loads(string_json))


def main():
    print(get_args())
    read_string_json(json_content)
    log.warning("information is read")


if __name__=='__main__':
    main()