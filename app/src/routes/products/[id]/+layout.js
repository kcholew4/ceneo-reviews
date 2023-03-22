import { env } from '$env/dynamic/public';
import { error } from '@sveltejs/kit';

const apiUrl = env.PUBLIC_API_URL;

export async function load({ fetch, params }) {
	const id = params.id;

	const res = await fetch(`https://${apiUrl}/api/products/${id}`);

	if (res.status === 404) {
		throw error(404, 'Nie znaleziono produktu');
	}

	if (!res.ok) {
		throw error(500, 'Wystąpił błąd');
	}

	if (res.status === 206) {
		throw error(503, 'Nie można pobrać produktu. Napotkano zabezpieczenie przeciw robotom.');
	}

	const json = await res.json();

	console.log(res.status);

	return json;
}
