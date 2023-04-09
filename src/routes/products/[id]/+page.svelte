<script lang="ts">
	import {
		Grid,
		Row,
		Column,
		DataTable,
		Pagination,
		Link,
		Modal,
		Button,
		Tag
	} from 'carbon-components-svelte';

	export let data;

	const reviews = data.product.reviews;

	const formatDate = (date: Date | null) => {
		if (!date) {
			return '-';
		}

		return new Intl.DateTimeFormat().format(date);
	};

	let pageSize = 25;
	let page = 1;

	let modalOpen = false;
	let modalHeading = '';
	let modalContent = '';
</script>

<Modal bind:open={modalOpen} bind:modalHeading passiveModal>{modalContent}</Modal>

<Grid>
	<Row>
		<Column lg={8}>
			<h1>{data.product.name}</h1>
		</Column>
	</Row>
	<Row>
		<Column>
			<DataTable
				sortable
				headers={[
					{ key: 'author', value: 'Autor' },
					{
						key: 'recommendation',
						value: 'Rekomendacja',
						display: (value) => (value ? value : '-')
					},
					{ key: 'score', value: 'Ocena' },
					{
						key: 'verified',
						value: 'Potwierdzona zakupem',
						sort: (a, b) => {
							const diff = Number(a) - Number(b);

							if (diff < 0) {
								return -1;
							} else if (diff > 0) {
								return 1;
							} else {
								return 0;
							}
						},
						display: (value) => (value ? 'Tak' : 'Nie')
					},
					{
						key: 'published',
						value: 'Data publikacji',
						display: (value) => formatDate(value)
					},
					{ key: 'bought', value: 'Data zakupu', display: (value) => formatDate(value) },
					{ key: 'votesYes', value: 'Za' },
					{ key: 'votesNo', value: 'Przeciw' },
					{ key: 'text', value: 'Treść' },
					{
						key: 'pros',
						value: 'Zalety',
						display: (value) => value.join(', ')
					},
					{ key: 'cons', value: 'Wady', display: (value) => value.join(', ') }
				]}
				{pageSize}
				{page}
				rows={reviews.map((single) => ({ ...single, id: single.ceneoReviewId }))}
			>
				<svelte:fragment slot="cell" let:cell let:row>
					<div class="row">
						{#if cell.key === 'text'}
							<Button
								kind="ghost"
								size="small"
								on:click={(e) => {
									e.preventDefault();

									if (modalOpen) {
										return;
									}

									modalContent = cell.value;
									modalOpen = true;
									modalHeading = row.author;
								}}>Otwórz</Button
							>
						{:else if cell.display}
							{cell.display(cell.value)}
						{:else}
							{cell.value}
						{/if}
					</div>
				</svelte:fragment>
			</DataTable>
			<Pagination bind:pageSize bind:page totalItems={reviews.length} pageSizeInputDisabled />
		</Column>
	</Row>
</Grid>

<style>
	h1 {
		margin-bottom: 1.5em;
	}

	.row {
		padding: 1em 0;
	}
</style>
