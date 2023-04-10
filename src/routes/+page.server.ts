import { fail } from '@sveltejs/kit';
import { CeneoProduct } from '$lib/server/ceneoProduct.js';

export const actions = {
  search: async ({ request }) => {
    const data = await request.formData();

    const productId = data.get('productId')?.toString() ?? '';

    if (!CeneoProduct.validateId(productId)) {
      return fail(400, { ok: false, productId, invalidId: true });
    }

    const ceneoProduct = new CeneoProduct(productId);
    const product = await ceneoProduct.getProduct();

    if (!product) {
      return fail(400, { ok: false, productId, doesNotExist: true });
    }

    return { ok: true, productId, product };
  }
};
