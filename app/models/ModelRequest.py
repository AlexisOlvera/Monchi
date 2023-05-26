from .entities.Rest_request import Rest_request
import datetime
class ModelRequest:
    @classmethod
    def find_requests(self, db):
        try:
            result = db['request'].find()
            requests = []
            for request in result:
                requests.append(Rest_request(**request))
            return requests
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def new_request(self, db, restaurant_name):
        try:
            db['request'].insert_one({'name': restaurant_name, 'date': datetime.datetime.now()})
        except Exception as ex:
            raise Exception(ex)