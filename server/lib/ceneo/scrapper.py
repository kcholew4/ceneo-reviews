from bs4 import BeautifulSoup
import requests

from .helpers.extract_review import ExtractReview


class Scrapper:
    def __init__(self, url):
        self.res = requests.get(url)
        self.soup = BeautifulSoup(self.res.text, features="html.parser")

    def status_code(self):
        return self.res.status_code

    def get_reviews(self):
        if self.res.status_code != requests.codes.ok:
            return None

        reviews_container = self.soup.select(
            "div.user-post.user-post__card.js_product-review")

        # No reviews :(
        if len(reviews_container) == 0:
            return []

        reviews = []

        for single_review in reviews_container:
            extract = ExtractReview(single_review)

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

    def get_product_name(self):
        if self.res.status_code != requests.codes.ok:
            return None

        title = self.soup.find(class_="product-top__product-info__name")
        return title.string.strip()
