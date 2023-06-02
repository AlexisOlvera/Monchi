class Triplet:
    def __init__(self, aspect: str, opinion: str, sentiment: str, positions: dict):
        self.aspect = aspect
        self.opinion = opinion
        self.sentiment = sentiment
        self.positions = positions