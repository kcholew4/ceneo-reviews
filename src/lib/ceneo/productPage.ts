import type { CheerioAPI } from "cheerio";
import { Review } from "./review.js"

export class ProductPage {
  private static SELECTORS = {
    review: "div.user-post.user-post__card.js_product-review",
    product_name: ".product-top__product-info__name",
    next_page: ".pagination__item.pagination__next",
    page_number: ".pagination__item.active > span"
  }

  private $: CheerioAPI;

  captchaProtected = false;
  name = "";
  reviews: Review[] = [];
  reviewsPage: number | null = null;
  hasNextReviewsPage = false;
  nextReviewsPage: number | null = null;

  constructor($: CheerioAPI) {
    this.$ = $;

    this.name = this.extractProductName();

    if (!this.name) {
      this.captchaProtected = true;
      return;
    }

    this.reviews = this.extractReviews();
    this.reviewsPage = this.extractReviewsPage();
    this.hasNextReviewsPage = this.extractHasNextReviewsPage();
    this.nextReviewsPage = this.getNextReviewsPage();
  }

  private extractProductName() { 
    const $name = this.$(ProductPage.SELECTORS.product_name);
    return $name.text();
  }

  private extractReviews() {
    const $reviews = this.$(ProductPage.SELECTORS.review)

    const reviews: Review[] = [];

    $reviews.each((index, element) => {
      const $review = this.$(element);

      if (!$review) {
        return;
      }

      reviews.push(new Review($review));
    })

    return reviews;
  }

  private extractReviewsPage() {
    const $page = this.$(ProductPage.SELECTORS.page_number);

    if ($page.length === 0) {
      return 1;
    }

    return parseInt($page.text());
  }

  private extractHasNextReviewsPage() {
    const $next_page = this.$(ProductPage.SELECTORS.next_page);

    if ($next_page.length === 0) {
      return false;
    }

    return true;
  }

  private getNextReviewsPage() {
    if (!this.extractHasNextReviewsPage()) {
      return null;
    }

    return this.extractReviewsPage() + 1;
  }
}