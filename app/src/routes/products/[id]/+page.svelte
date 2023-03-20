<script>
	import { goto } from '$app/navigation';
	import {
		DataTable,
		Tag,
		Pagination,
		Toolbar,
		ToolbarContent,
		ToolbarSearch,
		Button,
		Select,
		SelectItem,
		Grid,
		Row,
		Column
	} from 'carbon-components-svelte';

	export let data;

	const og_rows = data.reviews.map((review, index) => ({
		...review,
		id: index,
		review_id: review.id,
		recommendation: review.recommendation ?? 'Brak',
		verified: review.verified ? 'Tak' : 'Nie',
		pros: review.pros.join(', '),
		cons: review.cons.join(', ')
	}));

	let rows = [...og_rows];

	console.log(rows);

	let pageSize = 20;
	let page = 1;
	let filteredRowIds = [];

	const filterRecommendation = (text) => {
		if (text === 'default') {
			return (rows = [...og_rows]);
		}

		rows = og_rows.filter((row) => row.recommendation === text);
		console.log(filteredRowIds);
	};

	$: console.log(filteredRowIds);
</script>

<div class="container">
	<h2>{data.name}</h2>
	<Button on:click={() => goto(`/products/${data.product_id}/statistics`)}>Idź do wykresów</Button>
</div>
<div class="filters container">
	<Grid>
		<Row>
			<Column lg={{ span: 4 }}>
				<Select labelText="Rekomendacja" on:change={(e) => filterRecommendation(e.target.value)}>
					<SelectItem value="default" text="Domyślnie" />
					<SelectItem value="Polecam" text="Polecam" />
					<SelectItem value="Nie polecam" text="Nie polecam" />
					<SelectItem value="Brak" text="Brak" />
				</Select>
			</Column>
		</Row>
	</Grid>
</div>
<div class="table-container">
	<DataTable
		sortable
		expandable
		headers={[
			{ key: 'review_id', value: 'ID' },
			{ key: 'author', value: 'Autor' },
			{ key: 'recommendation', value: 'Rekomendacja' },
			{ key: 'score_count', value: 'Ocena' },
			{
				key: 'verified',
				value: 'Potwierdzona zakupem'
			},
			{ key: 'published_date', value: 'Data opublikowania' },
			{ key: 'bought_date', value: 'Data zakupu' },
			{ key: 'votes_yes', value: 'Głosy za' },
			{ key: 'votes_no', value: 'Głosy przeciw' },
			// { key: 'text', value: 'Treść' },
			{ key: 'pros', value: 'Zalety' },
			{ key: 'cons', value: 'Wady' }
		]}
		{rows}
		{pageSize}
		{page}
	>
		<Toolbar>
			<ToolbarContent>
				<ToolbarSearch persistent shouldFilterRows bind:filteredRowIds placeholder="Szukaj..." />
			</ToolbarContent>
		</Toolbar>
		<svelte:fragment slot="expanded-row" let:row>
			<div style="max-width: 640px;">{row.text}</div>
		</svelte:fragment>
	</DataTable>
	<Pagination bind:pageSize bind:page totalItems={filteredRowIds.length} pageSizeInputDisabled />
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

		margin-bottom: 2.5em;
	}

	.table-container {
		max-width: 1924px;
		margin: 0 auto;
	}
</style>
