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
  pros: string[];
  cons: string[];

  constructor($review: Cheerio<AnyNode>) {
    this.$review = $review

    this.id = this.extractId();
    this.author = this.extractAuthor();
    this.recommendation = this.extractRecommendation();
    this.score = this.extractScore();
    this.verified = this.extractVerified();
    this.published = this.extractPublished();
    this.bought = this.extractBought();
    this.votesYes = this.extractVotesYes();
    this.votesNo = this.extractVotesNo();
    this.text = this.extractText();
    this.pros = this.extractPros();
    this.cons = this.extractCons();
  }

  private getTimeTags() {
    return this.$review.find(Review.SELECTORS.time_tag)
  }

  private getReviewFeatureCols() {
    const reviewFeature = this.$review.find(Review.SELECTORS.review_feature);

    if (reviewFeature.length === 0) {
      return null;
    }

    return reviewFeature.find(Review.SELECTORS.review_feature_col);
  }

  private extractId() {
    return this.$review.attr("data-entry-id") ?? "";
  }

  private extractAuthor() {
    return this.$review.find(Review.SELECTORS.author).text().trim();
  }

  private extractRecommendation() {
    return this.$review.find(Review.SELECTORS.recommendation).text().trim();
  }

  private extractScore() {
    const raw = this.$review.find(Review.SELECTORS.score_count).text();
    const score = raw.match(/(?<score>.+)(?=\/\d)/)?.groups?.score;

    if (!score) {
      return 0;
    }

    return parseFloat(score.replaceAll(",", "."));
  }

  private extractVerified() {
    return this.$review.is(Review.SELECTORS.verified);
  }

  private extractPublished() {
    const timeTags = this.getTimeTags();
    return new Date(timeTags.first().attr("datetime") ?? 0)
  }

  private extractBought() {
    const timeTags = this.getTimeTags();

    if (timeTags.length < 2) {
      return null;
    }

    return new Date(timeTags.last().attr("datetime") ?? 0)
  }

  private extractVotesYes() {
    return parseInt(this.$review.find(Review.SELECTORS.votes_yes).text()) 
  }

  private extractVotesNo() {
    return parseInt(this.$review.find(Review.SELECTORS.votes_no).text());
  }

  private extractText() {
    // TODO: More advanced text extraction
    return this.$review.find(Review.SELECTORS.text).text().trim();
  }

  // TODO: Don't use string manipulation to extract pros and cons
  private extractPros() {
    const featureCols = this.getReviewFeatureCols();

    if (!featureCols) {
      return [];
    }

    const prosCol = featureCols.first();

    //Maybe not the best solution...
    return prosCol.text().trim().split("\n").slice(1).map((item) => item.trim());
  }

  private extractCons() {
    const featureCols = this.getReviewFeatureCols();

    if (!featureCols) {
      return [];
    }

    if (featureCols.length < 2) {
      return [];
    }

    const consCol = featureCols.last();

    return consCol.text().trim().split("\n").slice(1).map((item) => item.trim())
  }
}