import * as db from '$lib/server/db';

export const load = async () => {
	return {
		products: db.getProductsOverview()
	};
};
