from Triplets import Triplets

class Review:
    def __init__(self, review: str, triplets: list[Triplets]):
        self.review = review
        self.triplets = triplets

    def __str__(self):
        return f'{self.review}: {str(self.triplets)}'