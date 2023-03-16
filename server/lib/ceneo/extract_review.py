import bs4


class ExtractReview:
    def __init__(self, user_post):
        self.user_post = user_post

    def _get_time_tags(self):
        return self.user_post.find(
            class_="user-post__published").find_all("time")

    def _get_review_feature_cols(self):
        review_feature = self.user_post.find(class_="review-feature")

        if not review_feature:
            return []

        return review_feature.find_all(class_="review-feature__col")

    def _extract_text(self, tag):
        text = []

        if (type(tag) == bs4.element.NavigableString):
            return [str(tag).strip()]

        for child in tag.children:
            text += self._extract_text(child)

        return text

    def id(self) -> str:
        return self.user_post["data-entry-id"]

    def author(self) -> str:
        author = self.user_post.find(class_="user-post__author-name")
        return author.string.strip()

    def recommendation(self) -> str:
        recomendation = self.user_post.find(
            class_="user-post__author-recomendation")
        return recomendation.find("em").string.strip()

    def score_count(self) -> int:
        score_count = self.user_post.find(class_="user-post__score-count")
        return int(score_count.string[0])

    def verified(self) -> bool:
        return True if self.user_post.find(class_="review-pz") else False

    def published_date(self) -> str:
        time_tags = self._get_time_tags()
        return time_tags[0]["datetime"]

    def bought_date(self) -> str:
        time_tags = self._get_time_tags()

        if len(time_tags) < 2:
            return ""

        return time_tags[1]["datetime"]

    def votes_yes(self) -> int:
        votes_yes = self.user_post.find(class_="vote-yes").find("span")
        return int(votes_yes.string)

    def votes_no(self) -> int:
        votes_no = self.user_post.find(class_="vote-no").find("span")
        return int(votes_no.string)

    def text(self) -> str:
        text = self.user_post.find(class_="user-post__text")

        return self._extract_text(text)

    def pros(self) -> list:
        review_feature_cols = self._get_review_feature_cols()

        if len(review_feature_cols) == 0:
            return []

        pros_col = review_feature_cols[0]

        return [item.string.strip() for item in pros_col.find_all(class_="review-feature__item")]

    def cons(self) -> list:
        review_feature_cols = self._get_review_feature_cols()

        if len(review_feature_cols) != 2:
            return []

        cons_col = review_feature_cols[1]

        return [item.string.stip() for item in cons_col.find_all(class_="review-feature__item")]
