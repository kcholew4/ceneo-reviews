import { error } from '@sveltejs/kit';
import { CeneoProduct } from '$lib/server/ceneoProduct.js';

export const load = async ({ params }) => {
  const productId = params.id;

  if (!CeneoProduct.validateId(productId)) {
    throw error(400, 'Id produktu jest nieprawidłowe');
  }

  const ceneoProduct = new CeneoProduct(productId);
  const product = await ceneoProduct.getProduct();

  if (!product) {
    throw error(404, 'Product o podanym id nie istnieje.');
  }

  return { ok: true, product };
};
