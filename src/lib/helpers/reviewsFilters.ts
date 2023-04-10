import type { Review } from '@prisma/client';

export type FilterFunction = (reviews: Review[]) => Review[];

export class ReviewsFilters {
	static createRecommendationFilter(recommendation: string): FilterFunction {
		return (reviews: Review[]) => {
			return reviews.filter((review) => review.recommendation === recommendation);
		};
	}

	static createVerifiedFilter(verified: boolean): FilterFunction {
		return (reviews: Review[]) => {
			return reviews.filter((review) => review.verified === verified);
		};
	}

	static createScoresFilter(scores: number[]): FilterFunction {
		return (reviews: Review[]) => {
			return reviews.filter((review) => scores.includes(review.score));
		};
	}

	static createProsFilter(pros: string[]): FilterFunction {
		return (reviews: Review[]) => {
			return reviews.filter((review) => pros.every((pro) => review.pros.includes(pro)));
		};
	}

	static createConsFilter(cons: string[]): FilterFunction {
		return (reviews: Review[]) => {
			return reviews.filter((review) => cons.every((con) => review.cons.includes(con)));
		};
	}

	private reviews: Review[];

	constructor(reviews: Review[]) {
		this.reviews = reviews;
	}

	apply(filters: FilterFunction[]) {
		let filtered = this.reviews;

		filters.forEach((filter) => {
			filtered = filter(filtered);
		});

		return filtered;
	}
}
