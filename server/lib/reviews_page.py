class ReviewsPage:
    def __init__(self, page):
        self.page = page
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)
