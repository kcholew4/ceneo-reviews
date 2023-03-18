from .single_review import SingleReviewHelper


class ReviewsHelper:
    ELEMENT_SELECTORS = {
        "page_number": ".pagination__item.active > span",
        "next_page": ".pagination__item.pagination__next",
        "review": "div.user-post.user-post__card.js_product-review"
    }

    def __init__(self, page):
        self.page = page

    def _single_review(self, review_element):
        helper = SingleReviewHelper(review_element)

        return {
            "id": helper.id(),
            "author": helper.author(),
            "recommendation": helper.recommendation(),
            "score_count": helper.score_count(),
            "verified": helper.verified(),
            "published_date": helper.published_date(),
            "bought_date": helper.bought_date(),
            "votes_yes": helper.votes_yes(),
            "votes_no": helper.votes_no(),
            "text": helper.text(),
            "pros": helper.pros(),
            "cons": helper.cons()
        }

    def page_number(self):
        page_number = self.page.select_one(
            self.ELEMENT_SELECTORS["page_number"])
        return int(page_number.string) if page_number else 1

    def has_next_page(self):
        return True if self.page.select_one(self.ELEMENT_SELECTORS["next_page"]) else False

    def reviews(self):
        review_elements = self.page.select(
            self.ELEMENT_SELECTORS["review"])

        reviews = []

        for review_element in review_elements:
            reviews.append(self._single_review(review_element))

        return reviews
