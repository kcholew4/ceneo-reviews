from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

from .helpers.product_info import ProductInfoHelper
from .helpers.reviews import ReviewsHelper

from .structs.review import Review
from .structs.product import Product


class Scrapper:
    def __init__(self):
        self.s = requests.Session()
        ua = UserAgent()
        self.s.headers.update({"User-Agent": ua.chrome})

    def _query(self, url):
        print(f"querying url: {url}")

        res = self.s.get(url)

        if res.status_code == 404:
            return None

        if res.status_code != 200:
            return None  # TODO: Raise exception

        return BeautifulSoup(res.text, features="html.parser")

    def get_product(self, product_id):
        page = self._query(f"https://www.ceneo.pl/{product_id}")

        if not page:
            print("product not found")
            return None

        product_info_helper = ProductInfoHelper(page)
        reviews_helper = ReviewsHelper(page)

        product = Product(
            id=product_id,
            name=product_info_helper.name(),
            partial_data=False,
        )

        product.add_reviews(reviews_helper.reviews())

        while reviews_helper.has_next_page():
            page = self._query(
                f"https://www.ceneo.pl/{product_id}/opinie-{reviews_helper.page_number() + 1}")

            product_info_helper = ProductInfoHelper(page)
            reviews_helper = ReviewsHelper(page)

            if not product_info_helper.name():
                print("limit exceeded")
                product.partial_data = True
                break

            product.add_reviews(reviews_helper.reviews())

        product.calculate_overview()

        return product
