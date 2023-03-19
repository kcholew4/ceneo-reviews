import { env } from '$env/dynamic/public';
import { error } from '@sveltejs/kit';

const apiUrl = env.PUBLIC_API_URL;

export async function load({ fetch, params }) {
	const id = params.id;

	const res = await fetch(`http://${apiUrl}/api/products/${id}`);

	if (!res.ok) {
		if (res.status === 404) {
			throw error(404, 'Nie znaleziono produktu');
		}
		throw error(500, 'Wystąpił błąd');
	}

	return await res.json();
}
