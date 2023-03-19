<script>
	import { DataTable } from 'carbon-components-svelte';

	export let data;

	console.log(data.reviews);
</script>

<div class="container">
	<h2>{data.name}</h2>
</div>
<div class="table-container">
	<DataTable
		sortable
		headers={[
			{ key: 'id', value: 'ID' },
			{ key: 'author', value: 'Autor' },
			{ key: 'recommendation', value: 'Rekomendacja' },
			{ key: 'score_count', value: 'Ocena' },
			{ key: 'verified', value: 'Potwierdzona zakupem' },
			{ key: 'published_date', value: 'Data opublikowania' },
			{ key: 'bought_date', value: 'Data zakupu' },
			{ key: 'votes_yes', value: 'Głosy za' },
			{ key: 'votes_no', value: 'Głosy przeciw' },
			{ key: 'text', value: 'Treść' },
			{ key: 'pros', value: 'Zalety' },
			{ key: 'cons', value: 'Wady' }
		]}
		rows={data.reviews}
	/>
</div>

<style lang="scss">
	.container {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 2em;

		h2 {
			margin-top: 1em;
			margin-bottom: 1em;
		}
	}

	.table-container {
		max-width: 1924px;
		margin: 0 auto;
	}
</style>
