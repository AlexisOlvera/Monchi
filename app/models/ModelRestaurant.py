from .entities.Restaurant import Restaurant

class ModelRestaurant():
    @classmethod
    def find(self, db, restaurant_name):
        try:
            result = db['restaurants'].find_one({'name': {"$regex": restaurant_name, "$options": "i"}})
            print(result)
            if result != None:
                return Restaurant(**result)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
