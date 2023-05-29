from .entities.User import User

class ModelUser:
    @classmethod
    def authenticate(self, db, username, password):
        if username == 'admin' and password == 'admin':
            return True
        else:
            return False
        try:
            result = db['users'].find_one({'username': username})
            if result != None:
                return User(**result)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)