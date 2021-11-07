from consumer.connector import *

class Worker:
    def __init__(self, session, bucket, storage_strategy, requests_resource) -> None:
        self.session = session
        self.s3_resource = session.resource('s3')
        self.s3_client = session.client('s3')
        self.bucket = bucket
        self.storage_strategy = storage_strategy
        self.requests_resource = requests_resource
        self.request_queue = []
    
    def set_ddb_info(self, ddb, table_name):
        self.ddb = ddb
        self.table_name = table_name
    
    def set_s3_storage_info(self, bucket_name):
        self.storage_bucket_name = bucket_name

    def set_s3_resource_info(self, bucket_name):
        self.storage_bucket_name = bucket_name
    
    def set_sqs_resource_info(self, queue_url):
        self.queue_url = queue_url
        self.sqs_client = self.session.client('sqs')

    def prepare_db_data(self, r):
        owner = ""
        widget_id = ""
        db_data = {}
        for k, v in r.items():
            if k not in ['type', 'requestId']:
                if k != 'otherAttributes':
                    if k == 'owner':
                        owner = v.lower().strip().replace(' ', '-')
                    if k == 'widgetId':
                        widget_id = v
                        k = 'id'
                    db_data[k] = v
                else:
                    for each_attr in v:
                        db_data[each_attr.get('name')] = each_attr.get('value')
        
        widget_key = f'widgets/{owner}/{widget_id}.json'

        return widget_key, db_data

    def process_request(self, r):
        key = None
        request = r[1]
        response = False

        widget_key, data = self.prepare_db_data(request)

        if request.get('type') == 'create':
            if self.storage_strategy=='ddb':
                response = add_to_ddb(self.ddb, self.table_name, data)
            elif self.storage_strategy=='s3':
                response = add_to_bucket(self.s3_client, self.storage_bucket_name, data, widget_key)
            key = r[0] if response.get('ResponseMetadata').get('HTTPStatusCode') == 200 else None
            
        elif request.get('type') == 'update':
            if self.storage_strategy=='ddb':
                response = add_to_ddb(self.ddb, self.table_name, data)
            elif self.storage_strategy=='s3':
                response = add_to_bucket(self.s3_client, self.storage_bucket_name, data, widget_key)
            key = r[0] if response.get('ResponseMetadata').get('HTTPStatusCode') == 200 else None
        
        elif request.get('type') == 'delete':
            if self.storage_strategy=='ddb':
                response = remove_from_ddb(self.ddb, self.table_name, {'id': data.get('id')})
            elif self.storage_strategy=='s3':
                response = remove_from_bucket(self.s3_resource, self.storage_bucket_name, widget_key)
            key = r[0]
        else:
            return "Invalid Request Type"
        
        if key:
            if self.requests_resource == 's3':
                remove_from_bucket(self.s3_resource, self.bucket.name, key)
            else:
                remove_from_queue(self.sqs_client, self.queue_url, key)
        
        return response
        
    def handle_requests(self):
        status = []
        for request in self.request_queue:
            status.append(self.process_request(request))
        return status
        
    def add_to_queue(self, r):
        self.request_queue.append(r)
    