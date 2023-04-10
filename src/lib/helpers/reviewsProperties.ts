import type { Review } from '@prisma/client';

export class ReviewsProperties {
	private reviews: Review[];

	constructor(reviews: Review[]) {
		this.reviews = reviews;
	}

	private getPropertyLiteralValues<T extends keyof Review>(property: T) {
		return Array.from(
			this.reviews.reduce((acc, review) => {
				return new Set([...acc, review[property]]);
			}, new Set<Review[T]>())
		);
	}

	recommendations() {
		return this.getPropertyLiteralValues('recommendation');
	}

	scores() {
		return this.getPropertyLiteralValues('score');
	}

	verifiedOptions() {
		return this.getPropertyLiteralValues('verified');
	}

	pros() {
		return Array.from(
			this.reviews.reduce(
				(acc, review) => new Set<string>([...acc, ...review.pros]),
				new Set<string>()
			)
		);
	}

	cons() {
		return Array.from(
			this.reviews.reduce(
				(acc, review) => new Set<string>([...acc, ...review.cons]),
				new Set<string>()
			)
		);
	}
}
