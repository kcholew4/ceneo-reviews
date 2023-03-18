from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

from .helpers.extract_review import ExtractReview


class Scrapper:
    def __init__(self):
        self.s = requests.Session()
        ua = UserAgent()
        self.s.headers.update({"User-Agent": ua.chrome})

    def _query(self, url):
        print(f"querying url: {url}")

        self.res = self.s.get(url)
        self.soup = BeautifulSoup(self.res.text, features="html.parser")

        return self.res.status_code

    def _extract_single_review(self, review):
        extract = ExtractReview(review)

        return {
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

    def _extract_reviews(self):
        review_elements = self.soup.select(
            "div.user-post.user-post__card.js_product-review")

        reviews = []

        for single_review in review_elements:
            reviews.append(self._extract_single_review(single_review))

        return reviews

    def _extract_reviews_page(self):
        page = self.soup.select_one(".pagination__item.active > span")

        return int(page.string) if page else 1

    def _reviews_has_next_page(self):
        return True if self.soup.select_one(".pagination__item.pagination__next") else False

    def _extract_product_name(self):
        name = self.soup.select_one(".product-top__product-info__name")

        return name.string.strip() if name else None

    def get_product_data(self, product_id):
        status_code = self._query(f"https://www.ceneo.pl/{product_id}")

        if status_code == 404:
            return None

        if status_code != 200:
            return None  # TODO: Handle it

        result = {
            "name": self._extract_product_name(),
            "partial_data": False,
            "reviews": [
                {
                    "page": self._extract_reviews_page(),
                    "has_next_page": self._reviews_has_next_page(),
                    "data": [self._extract_reviews()]
                }
            ]
        }

        while self._reviews_has_next_page():
            status_code = self._query(
                f"https://www.ceneo.pl/{product_id}/opinie-{self._extract_reviews_page() + 1}")

            if status_code != 200 or (not self._extract_product_name()):
                result["partial_data"] = True  # Happens when limit is exceeded
                break

            result["reviews"].append({
                "page": self._extract_reviews_page(),
                "has_next_page": self._reviews_has_next_page(),
                "data": self._extract_reviews()
            })

        return result
