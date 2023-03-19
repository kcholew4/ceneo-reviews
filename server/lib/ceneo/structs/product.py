from .review import Review


class Product:
    def __init__(self, id, name, partial_data):
        self.id = id
        self.name = name
        self.partial_data = partial_data
        self.reviews: list[Review] = []

        self.overview = {
            "reviews_count": 0,
            "pros_count": 0,
            "cons_count": 0,
            "average_score": 0
        }

    def _reviews_to_dict(self, reviews):
        reviews_dict = []

        for review in reviews:
            reviews_dict.append(vars(review))

        return reviews_dict

    def calculate_overview(self):
        if (len(self.reviews) == 0):
            return

        self.overview["reviews_count"] = len(self.reviews)

        total_score = 0

        for review in self.reviews:
            self.overview["pros_count"] += review.pros_count()
            self.overview["cons_count"] += review.cons_count()
            total_score += review.score_count

        self.overview["average_score"] = total_score / \
            self.overview["reviews_count"]

    def add_reviews(self, reviews: list[Review]):
        self.reviews += reviews

    def get(self):
        return {
            "product_id": self.id,
            "name": self.name,
            "partial_data": self.partial_data,
            "overview": self.overview,
            "reviews": self._reviews_to_dict(self.reviews)
        }
