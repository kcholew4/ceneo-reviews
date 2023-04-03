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

  id: string;
  author: string;
  recommendation: string;
  score: number;
  verified: boolean;
  published: Date;
  bought: Date | null;
  votesYes: number;
  votesNo: number;
  text: string;
  pros: string[] | null;
  cons: string[] | null;

  constructor($review: Cheerio<AnyNode>) {
    this.$review = $review

    this.id = $review.attr("data-entry-id") ?? "";
    this.author = $review.find(Review.SELECTORS.author).text().trim();
    this.recommendation = $review.find(Review.SELECTORS.recommendation).text().trim();
    this.score = this.extractScore();
    this.verified = $review.is(Review.SELECTORS.verified);
    this.published = this.extractPublished();
    this.bought = this.extractBought();
    this.votesYes = parseInt(this.$review.find(Review.SELECTORS.votes_yes).text());
    this.votesNo = parseInt(this.$review.find(Review.SELECTORS.votes_no).text());
    this.text = $review.find(Review.SELECTORS.text).text().trim(); // TODO: More advanced text extraction
    this.pros = this.extractPros();
    this.cons = this.extractCons();
  }

  private extractTimeTags() {
    return this.$review.find(Review.SELECTORS.time_tag)
  }

  private extractReviewFeatureCols() {
    const reviewFeature = this.$review.find(Review.SELECTORS.review_feature);

    if (reviewFeature.length === 0) {
      return null;
    }

    return reviewFeature.find(Review.SELECTORS.review_feature_col);
  }

  private extractScore() {
    const raw = this.$review.find(Review.SELECTORS.score_count).text();
    const score = raw.match(/(?<score>.+)(?=\/\d)/)?.groups?.score;

    if (!score) {
      return 0;
    }

    return parseFloat(score.replaceAll(",", "."));
  }

  private extractPublished() {
    const timeTags = this.extractTimeTags();
    return new Date(timeTags.first().attr("datetime") ?? 0)
  }

  private extractBought() {
    const timeTags = this.extractTimeTags();

    if (timeTags.length < 2) {
      return null;
    }

    return new Date(timeTags.last().attr("datetime") ?? 0)
  }

  // TODO: Don't use string manipulation to extract pros and cons
  private extractPros() {
    const featureCols = this.extractReviewFeatureCols();

    if (!featureCols) {
      return null;
    }

    const prosCol = featureCols.first();

    //Maybe not the best solution...
    return prosCol.text().trim().split("\n").slice(1).map((item) => item.trim());
  }

  private extractCons() {
    const featureCols = this.extractReviewFeatureCols();

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