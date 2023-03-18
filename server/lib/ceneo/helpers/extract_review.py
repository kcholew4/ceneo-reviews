from bs4.element import NavigableString


class ExtractReview:
    ELEMENT_SELECTORS = {
        "author": ".user-post__author-name",
        "recommendation": ".user-post__author-recomendation > em",
        "score_count": ".user-post__score-count",
        "verified": ".user-post__info > .review-pz",
        "time_tag": ".user-post__published > time",
        "votes_yes": ".vote-yes > span",
        "votes_no": ".vote-no > span",
        "text": ".user-post__text",
        "review_feature": ".review-feature",
        "review_feature_col": ".review-feature__col",
        "review_feature_item": ".review-feature__item"
    }

    def __init__(self, review):
        self.review = review

    def _get_time_tags(self):
        return self.review.select(self.ELEMENT_SELECTORS["time_tag"])

    def _get_review_feature_cols(self):
        review_feature = self.review.select_one(
            self.ELEMENT_SELECTORS["review_feature"])

        if not review_feature:
            return []

        return review_feature.select(self.ELEMENT_SELECTORS["review_feature_col"])

    def _extract_text(self, tag):
        text = []

        if (type(tag) == NavigableString):
            return [str(tag).strip()]

        for child in tag.children:
            text += self._extract_text(child)

        return text

    def id(self):
        return self.review["data-entry-id"]

    def author(self):
        author = self.review.select_one(self.ELEMENT_SELECTORS["author"])
        return author.string.strip()

    def recommendation(self):
        recomendation = self.review.select_one(
            self.ELEMENT_SELECTORS["recommendation"])

        if not recomendation:
            return None

        return recomendation.string.strip()

    def score_count(self):
        score_count = self.review.select_one(
            self.ELEMENT_SELECTORS["score_count"])
        return int(score_count.string[0])

    def verified(self):
        return True if self.review.select_one(self.ELEMENT_SELECTORS["verified"]) else False

    def published_date(self):
        time_tags = self._get_time_tags()
        return time_tags[0]["datetime"]

    def bought_date(self):
        time_tags = self._get_time_tags()

        if len(time_tags) < 2:
            return None

        return time_tags[1]["datetime"]

    def votes_yes(self):
        votes_yes = self.review.select_one(self.ELEMENT_SELECTORS["votes_yes"])
        return int(votes_yes.string)

    def votes_no(self):
        votes_no = self.review.select_one(self.ELEMENT_SELECTORS["votes_no"])
        return int(votes_no.string)

    def text(self):
        text = self.review.select_one(self.ELEMENT_SELECTORS["text"])

        return self._extract_text(text)

    def pros(self):
        review_feature_cols = self._get_review_feature_cols()

        if len(review_feature_cols) == 0:
            return []

        pros_col = review_feature_cols[0]

        return [item.string.strip() for item in pros_col.select(self.ELEMENT_SELECTORS["review_feature_item"])]

    def cons(self):
        review_feature_cols = self._get_review_feature_cols()

        if len(review_feature_cols) != 2:
            return []

        cons_col = review_feature_cols[1]

        return [item.string.strip() for item in cons_col.select(self.ELEMENT_SELECTORS["review_feature_item"])]
