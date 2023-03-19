import { env } from '$env/dynamic/public';
import { error } from '@sveltejs/kit';

export async function load({ fetch }) {
	const res = await fetch(`http://${env.PUBLIC_API_URL}/api/products`);

	if (!res.ok) {
		if (res.status === 404) {
			throw error(404, 'Nie znaleziono produktu');
		}
		throw error(500, 'Wystąpił błąd');
	}

	return {
		list: await res.json()
	};
}
