<script>
	import { Tile, Link, Button } from 'carbon-components-svelte';
	import { saveAs } from 'file-saver';
	import { env } from '$env/dynamic/public';
	import { Parser } from '@json2csv/plainjs';
	import xlsx from 'json-as-xlsx';

	export let data;

	const { list } = data;

	const fetchProduct = async (id) => {
		const res = await fetch(`http://${env.PUBLIC_API_URL}/api/products/${id}`);

		if (!res.ok) {
			console.log('error saving file');
			return null;
		}

		return await res.json();
	};

	const getReviews = async (id) => {
		const product = await fetchProduct(id);

		if (!product) {
			return null;
		}

		return product.reviews;
	};

	const normalizeReviews = (reviews) => {
		return reviews.map((review) => ({
			...review,
			pros: `${review.pros.join(', ')}`,
			cons: `${review.cons.join(', ')}`,
			text: `${review.text.join(', ')}`
		}));
	};

	const downloadJSON = async (id) => {
		const reviews = await getReviews(id);
		const blob = new Blob([JSON.stringify(reviews)], { type: 'application/json' });
		saveAs(blob, 'reviews.json');
	};

	const downloadCSV = async (id) => {
		const reviews = normalizeReviews(await getReviews(id));

		try {
			const parser = new Parser();
			const csv = parser.parse(reviews);
			// console.log(csv);
			const blob = new Blob([csv], { type: 'text/csv' });
			saveAs(blob, 'reviews.csv');
		} catch (error) {
			console.log(error);
		}
	};

	const downloadXLSX = async (id) => {
		const reviews = normalizeReviews(await getReviews(id));

		const columns = Object.keys(reviews[0]).map((key) => ({ label: key, value: key }));

		const data = [
			{
				sheet: 'reviews',
				columns,
				content: reviews
			}
		];

		const result = xlsx(data, { fileName: 'reviews' });

		saveAs(new Blob([result]), 'reviews.xlsx');
	};
</script>

<div class="container">
	<h2>Lista produktów</h2>
	{#each list as single}
		<div class="element">
			<Tile>
				<a href="/products/{single.product_id}"><h3>{single.name}</h3></a>
				<div class="item">Liczba opinii: {single.overview.reviews_count}</div>
				<div class="item">Liczba was: {single.overview.cons_count}</div>
				<div class="item">Liczba zalet: {single.overview.pros_count}</div>
				<h5 style="margin-top: 1.5em;">Pobierz opinie:</h5>
				<div style="padding-top: 1em;">
					<Button kind="ghost" on:click={() => downloadJSON(single.product_id)}>json</Button>
					<Button kind="ghost" on:click={() => downloadCSV(single.product_id)}>csv</Button>
					<Button kind="ghost" on:click={() => downloadXLSX(single.product_id)}>xlsx</Button>
				</div>
			</Tile>
		</div>
	{/each}
</div>

<style>
	.container {
		max-width: 1000px;
		margin: 0 auto;
	}

	h2 {
		margin-bottom: 2em;
	}

	h3 {
		padding-bottom: 0.25em;
	}

	.element + .element {
		margin-top: 2em;
	}

	a {
		display: block;
		text-decoration: none;
		color: inherit;
	}

	.item + .item {
		margin-top: 0.5em;
	}
</style>
