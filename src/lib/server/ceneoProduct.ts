import * as cheerio from 'cheerio';
import type { Review } from '../ceneo/review.js';
import { ProductPage } from '../ceneo/productPage.js';
import * as db from './db';

export class CeneoProduct {
	private static ID_PATTERN = /^\d+$/;
	private static URL = 'https://www.ceneo.pl';

	private baseUrl: string;

	id: string;
	name = '';
	reviews: Review[] = [];

	reviewsCount = 0;
	prosCount = 0;
	consCount = 0;
	averageScore = 0;

	partialExtraction = false;
	blockedWithCaptcha = false;
	notFound = false;

	constructor(id: string) {
		if (!CeneoProduct.validateId(id)) {
			throw new Error(`Invalid product id: ${id}`);
		}

		this.id = id;
		this.baseUrl = `${CeneoProduct.URL}/${id}`;
	}

	static validateId(id: string) {
		return id.match(CeneoProduct.ID_PATTERN) ? true : false;
	}

	static async exists(id: string) {
		if (!CeneoProduct.validateId(id)) {
			throw new Error(`Invalid product id: ${id}`);
		}

		const url = `${CeneoProduct.URL}/${id}`;

		const response = await fetch(url);

		if (response.status !== 200 && response.status !== 404) {
			throw new Error(`Unknown response: ${url} (${response.status})`);
		}

		if (response.status === 404) {
			return false;
		}

		return true;
	}

	private async getPageContent({ reviewsPage }: { reviewsPage: number }) {
		const queryUrl = reviewsPage > 0 ? `${this.baseUrl}/opinie-${reviewsPage}` : this.baseUrl;

		const response = await fetch(queryUrl);

		if (response.status === 404) {
			return null;
		}

		if (!response.ok) {
			throw new Error(`Error fetching the page: ${queryUrl} (${response.status})`);
		}

		return await response.text();
	}

	private async fetch() {
		let content = await this.getPageContent({ reviewsPage: 0 });

		if (!content) {
			this.notFound = true;
			return;
		}

		let productPage = new ProductPage(cheerio.load(content));

		if (productPage.captchaProtected) {
			this.blockedWithCaptcha = true;
			return;
		}

		this.name = productPage.name;
		this.reviews.push(...productPage.reviews);

		for (;;) {
			if (productPage.nextReviewsPage === null) {
				return;
			}

			content = await this.getPageContent({ reviewsPage: productPage.nextReviewsPage });
			// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
			productPage = new ProductPage(cheerio.load(content!));

			if (productPage.captchaProtected) {
				this.partialExtraction = true;
				return;
			}

			this.reviews.push(...productPage.reviews);
		}
	}

	private calculateOverview() {
		this.reviewsCount = this.reviews.length;
		this.prosCount = this.reviews.reduce((count, review) => count + review.pros.length, 0);
		this.consCount = this.reviews.reduce((count, review) => count + review.cons.length, 0);

		if (this.reviewsCount === 0) {
			this.averageScore = 0;
		} else {
			this.averageScore =
				this.reviews.reduce((count, review) => count + review.score, 0) / this.reviewsCount;
		}
	}

	async getProduct() {
		let product = await db.getProductById(this.id);

		//TODO: Deal with partial extraction
		if (!product) {
			await this.fetch();

			if (this.notFound) {
				return null;
			}

			if (this.blockedWithCaptcha) {
				throw new Error('Product page is blocked with captcha');
			}

			this.calculateOverview();
			product = await db.insertProduct(this);
		}

		return product;
	}
}
