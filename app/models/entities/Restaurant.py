class Restaurant:
    def __init__(self, name, review, data, id_google, id_yelp, _id, last_updated):
        self.name = name
        self.review = review
        self.data = data
        self.id_google = id_google
        self.id_yelp = id_yelp
        self._id = _id
        self.last_updated = last_updated
    def __str__(self):
        return f"{self.name}: {self.review}"
