class ReviewsPage:
    def __init__(self, page):
        self.page = page
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def get_reviews(self):
        reviews = []
        for review in self.reviews:
            reviews.append({
                "id": review.id,
                "author": review.author,
                "recommendation": review.recommendation,
                "score_count": review.score_count,
                "verified": review.verified,
                "published_date": review.published_date,
                "bought_date": review.bought_date,
                "votes_yes": review.votes_yes,
                "votes_no": review.votes_no,
                "text": review.text,
                "pros": review.pros,
                "cons": review.cons
            })

        return reviews
