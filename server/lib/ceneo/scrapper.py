from bs4 import BeautifulSoup
import requests

from lib.ceneo.extract_review import ExtractReview
from lib.reviews_page import ReviewsPage


class Scrapper:
    def get_reviews_page(self, product_id, page=1) -> ReviewsPage | None:
        url = f"https://www.ceneo.pl/{product_id}"

        r = requests.get(url)

        soup = BeautifulSoup(r.text, features="html.parser")

        user_posts = soup.select(
            "div.user-post.user-post__card.js_product-review")

        if len(user_posts) == 0:
            return None

        reviews_page = ReviewsPage(page)

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

            reviews_page.add_review(review)

        return reviews_page
