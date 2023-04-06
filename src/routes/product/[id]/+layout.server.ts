import { error } from '@sveltejs/kit';
import { CeneoProduct } from '$lib/server/ceneoProduct.js';

export const load = async ({ params }) => {
  const productId = params.id;

  if (!await CeneoProduct.exists(productId)) {
    throw error(404, "Product o podanym id nie istnieje.")
  }

  return { ok: true }
}