from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

from .helpers.product_info import ProductInfoHelper
from .helpers.reviews import ReviewsHelper


class Scrapper:
    def __init__(self):
        self.s = requests.Session()
        ua = UserAgent()
        self.s.headers.update({"User-Agent": ua.chrome})

    def _query(self, url):
        print(f"querying url: {url}")

        res = self.s.get(url)
        self.page = BeautifulSoup(res.text, features="html.parser")

        return res.status_code

    def get_product_data(self, product_id):
        status_code = self._query(f"https://www.ceneo.pl/{product_id}")

        if status_code == 404:
            return None

        if status_code != 200:
            return None  # TODO: Handle it

        product_info_helper = ProductInfoHelper(self.page)
        reviews_helper = ReviewsHelper(self.page)

        result = {
            "product_id": product_id,
            "name": product_info_helper.name(),
            "partial_reviews_data": False,
            "reviews": [
                {
                    "page": reviews_helper.page_number(),
                    "has_next_page": reviews_helper.has_next_page(),
                    "data": reviews_helper.reviews()
                }
            ]
        }

        while reviews_helper.has_next_page():
            status_code = self._query(
                f"https://www.ceneo.pl/{product_id}/opinie-{reviews_helper.page_number() + 1}")

            product_info_helper = ProductInfoHelper(self.page)
            reviews_helper = ReviewsHelper(self.page)

            # Product name is not available when exceeded limit
            if status_code != 200 or (not product_info_helper.name()):
                print("limit exceeded")
                result["partial_reviews_data"] = True
                break

            result["reviews"].append({
                "page": reviews_helper.page_number(),
                "has_next_page": reviews_helper.has_next_page(),
                "data": reviews_helper.reviews()
            })

        return result
