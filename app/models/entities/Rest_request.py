class Rest_request:
    def __init__(self, _id, name, date):
        self._id = _id
        self.name = name
        self.date = date
    
    def __str__(self):
        return f"{self.name}: {self.date}"