import type { Cheerio, AnyNode } from "cheerio";

export class Review {
  private static SELECTORS = {
    author: ".user-post__author-name",
    recommendation: ".user-post__author-recomendation > em",
    score_count: ".user-post__score-count",
    verified: ".user-post__info > .review-pz",
    time_tag: ".user-post__published > time",
    votes_yes: ".vote-yes > span",
    votes_no: ".vote-no > span",
    text: ".user-post__text",
    review_feature: ".review-feature",
    review_feature_col: ".review-feature__col",
    review_feature_item: ".review-feature__item"
  }

  private $review: Cheerio<AnyNode>;

  constructor($review: Cheerio<AnyNode>) {
    this.$review = $review
  }

  private timeTags() {
    return this.$review.find(Review.SELECTORS.time_tag)
  }

  private reviewFeatureCols() {
    const reviewFeature = this.$review.find(Review.SELECTORS.review_feature);

    if (reviewFeature.length === 0) {
      return null;
    }

    return reviewFeature.find(Review.SELECTORS.review_feature_col);
  }

  id() {
    return this.$review.attr("data-entry-id") ?? null;
  }

  author() {
    return this.$review.find(Review.SELECTORS.author).text().trim();
  }

  recommendation() {
    return this.$review.find(Review.SELECTORS.recommendation).text().trim();
  }

  score() {
    const raw = this.$review.find(Review.SELECTORS.score_count).text();
    const score = raw.match(/(?<score>.+)(?=\/\d)/)?.groups?.score;

    if (!score) {
      return null;
    }

    return parseFloat(score.replaceAll(",", "."));
  }

  verified() {
    return this.$review.is(Review.SELECTORS.verified)
  }

  published() {
    const timeTags = this.timeTags();
    return new Date(timeTags.first().attr("datetime") ?? 0)
  }

  bought() {
    const timeTags = this.timeTags();

    if (timeTags.length < 2) {
      return null;
    }

    return new Date(timeTags.last().attr("datetime") ?? 0)
  }

  votesYes() {
    return parseInt(this.$review.find(Review.SELECTORS.votes_yes).text())
  }

  votesNo() {
    return parseInt(this.$review.find(Review.SELECTORS.votes_no).text())
  }

  text() {
    return this.$review.find(Review.SELECTORS.text).text().trim();
  }

  pros() {
    const featureCols = this.reviewFeatureCols();

    if (!featureCols) {
      return null;
    }

    const prosCol = featureCols.first();

    //Maybe not the best solution...
    return prosCol.text().trim().split("\n").slice(1).map((item) => item.trim());
  }

  cons() {
    const featureCols = this.reviewFeatureCols();

    if (!featureCols) {
      return null;
    }

    if (featureCols.length < 2) {
      return null;
    }

    const consCol = featureCols.last();

    return consCol.text().trim().split("\n").slice(1).map((item) => item.trim())
  }
}