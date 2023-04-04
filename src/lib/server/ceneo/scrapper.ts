import * as cheerio from "cheerio"

import { Review } from "./review.js"

export class ProductPageScrapper {
  private static SELECTORS = {
    review: "div.user-post.user-post__card.js_product-review",
    product_name: ".product-top__product-info__name",
    next_page: ".pagination__item.pagination__next",
    page_number: ".pagination__item.active > span"
  }

  private $: cheerio.CheerioAPI;

  constructor() {
    //Load empty string so this.$ is always defined
    this.$ = cheerio.load("");
  }

  async query(url: string): Promise<void> {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Error fetching the page: ${url} (${response.status})`);
    }
  
    const content = await response.text();
    this.$ = cheerio.load(content)
  }

  extractReviews() {
    const $reviews = this.$(ProductPageScrapper.SELECTORS.review)

    const reviews: Review[] = [];

    $reviews.each((index, element) => {
      const $review = this.$?.(element);

      if (!$review) {
        return;
      }

      reviews.push(new Review($review));
    })

    return reviews;
  }

  extractProductName() { 
    const $name = this.$(ProductPageScrapper.SELECTORS.product_name);
    return $name.text();
  }

  hasNextReviewsPage() {
    const $next_page = this.$(ProductPageScrapper.SELECTORS.next_page);

    if ($next_page.length === 0) {
      return false;
    }

    return true;
  }

  extractReviewsPageNumber() {
    const $page = this.$(ProductPageScrapper.SELECTORS.page_number);

    if ($page.length === 0) {
      return 1;
    }

    return parseInt($page.text());
  }
}