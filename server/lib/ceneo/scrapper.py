from bs4 import BeautifulSoup
import requests

from lib.ceneo.extract_review import ExtractReview


class Scrapper:
    def __init__(self, url):
        self.res = requests.get(url)
        self.soup = BeautifulSoup(self.res.text, features="html.parser")

    def status_code(self):
        return self.res.status_code

    def get_reviews(self):
        if self.res.status_code != requests.codes.ok:
            return None

        user_posts = self.soup.select(
            "div.user-post.user-post__card.js_product-review")

        if len(user_posts) == 0:
            return None

        reviews = []

        for user_post in user_posts:
            extract = ExtractReview(user_post)

            review = {
                "id": extract.id(),
                "author": extract.author(),
                "recommendation": extract.recommendation(),
                "score_count": extract.score_count(),
                "verified": extract.verified(),
                "published_date": extract.published_date(),
                "bought_date": extract.bought_date(),
                "votes_yes": extract.votes_yes(),
                "votes_no": extract.votes_no(),
                "text": extract.text(),
                "pros": extract.pros(),
                "cons": extract.cons()
            }

            reviews.append(review)

        return reviews
