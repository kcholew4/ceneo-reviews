<script>
	import { Tile, Link } from 'carbon-components-svelte';

	export let data;

	const { list } = data;
</script>

<div class="container">
	<h2>Lista produktów</h2>
	{#each list as single}
		<div class="element">
			<a href="/products/{single.product_id}">
				<Tile>
					<h3>{single.name}</h3>
					<div class="item">Liczba opinii: {single.overview.reviews_count}</div>
					<div class="item">Liczba was: {single.overview.cons_count}</div>
					<div class="item">Liczba zalet: {single.overview.pros_count}</div>
				</Tile>
			</a>
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
