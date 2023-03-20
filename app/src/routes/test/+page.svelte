<script>
	import { env } from '$env/dynamic/public';
	import { onMount } from 'svelte';

	const getUrl = (id) => `http://${env.PUBLIC_API_URL}/api/products/${id}/check`;

	const check = async (id) => {
		const url = getUrl(id);

		console.log(url);

		const res = await fetch(getUrl(id));

		if (res.status == 200) {
			return true;
		}

		return false;
	};

	onMount(async () => {
		console.log(await check('1234'));
	});
</script>
