from connector import delete_request

class Worker:
    def __init__(self, s3, bucket, db, table_name) -> None:
        self.s3 = s3
        self.bucket = bucket
        self.db = db
        self.table_name = table_name
        self.request_queue = []
    
    def get_db_data(self, r) -> dict:
        db_data = {}
        for k, v in r.items():
            if k not in ['type', 'requestId']:
                if k != 'otherAttributes':
                    if k == 'widgetId':
                        k = 'id'
                    db_data[k] = v
                else:
                    for each_attr in v:
                        db_data[each_attr.get('name')] = each_attr.get('value')
        return db_data

    def process_request(self, r):
        key = None
        request = r[1]
        response = False
        if request.get('type') == 'create':
            response = self.db.Table(self.table_name).put_item(Item=self.get_db_data(request))
            key = r[0] if response.get('ResponseMetadata').get('HTTPStatusCode') == 200 else None
        elif request.get('type') == 'update':
            # TODO
            key = r[0]
        elif request.get('type') == 'delete':
            # TODO
            key = r[0]
        else:
            return "Invalid Request Type"
        
        if key:
            resp = delete_request(self.s3, self.bucket.name, key)
            # print("Delete: {}".format(resp))
        
        return response
        
    def handle_requests(self):
        status = []
        for request in self.request_queue:
            status.append(self.process_request(request))
        return status
        
    def add_to_queue(self, r):
        self.request_queue.append(r)
    