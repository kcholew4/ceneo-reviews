from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

from .helpers.extract_review import ExtractReview


class Scrapper:
    def __init__(self):
        self.s = requests.Session()

        ua = UserAgent()
        self.s.headers.update({"User-Agent": ua.chrome})

    def query(self, url):
        print(url)

        self.res = self.s.get(url)
        self.soup = BeautifulSoup(self.res.text, features="html.parser")

        return self.res.status_code

    def not_found(self):
        return self.res.status_code == 404

    def ok(self):
        return self.res.status_code == requests.codes.ok

    def reviews(self):
        review_elements = self.soup.select(
            "div.user-post.user-post__card.js_product-review")

        # No reviews :(
        if len(review_elements) == 0:
            return []

        reviews = []

        for single_review in review_elements:
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

    def product_name(self):
        title = self.soup.find(class_="product-top__product-info__name")

        if not title:
            return None

        return title.string.strip()

    def reviews_page(self):
        pagination = self.soup.find(class_="pagination__item active")

        if not pagination:
            return 1

        return int(pagination.find("span").string)

    def reviews_has_next_page(self):
        return True if self.soup.find(
            class_="pagination__item pagination__next") else False
