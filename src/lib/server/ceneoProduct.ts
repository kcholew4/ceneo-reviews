import type { Review } from "./ceneo/review.js";
import { ProductPageScrapper } from "./ceneo/scrapper.js";

export class CeneoProduct {
  private static ID_PATTERN = /^\d+$/
  private static URL = "https://www.ceneo.pl";

  private baseUrl: string;

  id: string;
  name = "";
  partialExtraction = false;
  reviews: Review[] = [];

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

  async get() {
    const scrapper = new ProductPageScrapper();

    console.log(this.baseUrl);

    await scrapper.query(this.baseUrl);

    this.name = scrapper.extractProductName() ?? "";
    this.reviews.push(...scrapper.extractReviews());

    if (!scrapper.hasNextReviewsPage()) {
      return;
    }

    do {
      const nextPageUrl = `${this.baseUrl}/opinie-${scrapper.extractReviewsPageNumber() + 1}`;

      await scrapper.query(nextPageUrl);

      console.log(nextPageUrl);

      if (scrapper.extractProductName() === null) {
        this.partialExtraction = true;
        break;
      }

      this.reviews.push(...scrapper.extractReviews());
    } while(scrapper.hasNextReviewsPage())
  }
}