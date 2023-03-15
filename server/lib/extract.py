class Extract:
    def __init__(self, tag):
        self.tag = tag

    def id(self) -> str:
        return self.tag["data-entry-id"]

    def author(self) -> str:
        return self.tag.find(class_="user-post__author-name").string

    def recommendation(self) -> str:
        return self.tag.find(
            class_="user-post__author-recomendation").string

    def scoreCount(self) -> int:
        score = self.tag.find(class_="user-post__score-count").string
        return int(score[0])

    def verified(self) -> bool:
        return True if self.tag.find(class_="review-pz") else False

    def dates(self) -> tuple:
        time = self.tag.find(
            class_="user-post__published").find_all("time")

        datetimes = [time["datetime"] for time in time]

        if (len(datetimes) == 1):
            return datetimes[0], None

        return datetimes[0], datetimes[1]

    def votes(self) -> tuple:
        votesYes = self.tag.find(class_="vote-yes").find("span").string
        votesNo = self.tag.find(class_="vote-no").find("span").string
        return int(votesYes), int(votesNo)

    def text(self) -> str:
        return self.tag.find(class_="user-post__text").string

    def features(self) -> tuple:
        feature = self.tag.find(class_="review-feature")

        if not feature:
            return None, None

        featureCols = feature.find_all(class_="review-feature__col")

        pros = [item.string for item in featureCols[0].find_all(
            class_="review-feature__item")]

        if len(featureCols) == 1:
            return pros, None

        cons = [item.string for item in featureCols[1].find_all(
            class_="review-feature__item")]

        return pros, cons
