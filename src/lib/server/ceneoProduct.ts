import * as cheerio from "cheerio";
import type { Review } from "./ceneo/review.js";
import { ProductPage } from "./ceneo/productPage.js";

export class CeneoProduct {
  private static ID_PATTERN = /^\d+$/
  private static URL = "https://www.ceneo.pl";

  private baseUrl: string;

  id: string;
  name = "";
  reviews: Review[] = [];
  partialExtraction = false;

  constructor(id: string) {
    if (!CeneoProduct.validateId(id)) {
      throw new Error(`Invalid product id: ${id}`)
    }

    this.id = id;
    this.baseUrl = `${CeneoProduct.URL}/${id}`;
  }

  static validateId(id: string) {
    return id.match(CeneoProduct.ID_PATTERN) ? true : false;
  }

  static async exists(id: string) {
    if (!CeneoProduct.validateId(id)) {
      throw new Error(`Invalid product id: ${id}`)
    }

    const url = `${CeneoProduct.URL}/${id}`;

    const response = await fetch(url);

    if (response.status !== 200 && response.status !== 404) {
      throw new Error(`Unknown response: ${url} (${response.status})`)
    }

    if (response.status === 404) {
      return false;
    }

    return true;
  }

  private async getPageContent({ reviewsPage }: { reviewsPage: number }) {
    const queryUrl = reviewsPage > 0 ? `${this.baseUrl}/opinie-${reviewsPage}` : this.baseUrl;

    const response = await fetch(queryUrl);

    if (!response.ok) {
      throw new Error(`Error fetching the page: ${queryUrl} (${response.status})`);
    }

    return await response.text();
  }

  async get() {
    let content = await this.getPageContent({ reviewsPage: 0 });
    let productPage = new ProductPage(cheerio.load(content));

    this.name = productPage.name
    this.reviews.push(...productPage.reviews);

    for(;;) {
      if (productPage.nextReviewsPage === null) {
        return;
      }

      content = await this.getPageContent({ reviewsPage: productPage.nextReviewsPage })
      productPage = new ProductPage(cheerio.load(content));

      if (productPage.captchaProtected) {
        this.partialExtraction = true;
        return;
      }

      this.reviews.push(...productPage.reviews);
    }
  }
}