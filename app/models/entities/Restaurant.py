class Restaurant:
    def __init__(self, name, review, data, id_google, id_yelp, id_tripadvisor, _id, last_updated, relevant_pairs):
        self.name = name
        self.review = review
        self.data = data
        self.id_google = id_google
        self.id_yelp = id_yelp
        self.id_tripadvisor = id_tripadvisor
        self._id = _id
        self.last_updated = last_updated
        self.relevant_pairs = relevant_pairs
    def __str__(self):
        return f"{self.name}: {self.review}"
