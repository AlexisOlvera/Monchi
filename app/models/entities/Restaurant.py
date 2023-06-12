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

    def formated_review(self):
        lines = self.review.split("\n")
        review_formated = ""
        review_formated += "<h4>"+lines[0]+"</h4>"
        for line in lines[1:]:
            review_formated += "<p>"+line+"</p>"
        return review_formated
