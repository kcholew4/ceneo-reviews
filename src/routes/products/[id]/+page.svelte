<script lang="ts">
	import {
		Grid,
		Row,
		Column,
		DataTable,
		Pagination,
		Modal,
		Button,
		Dropdown,
		MultiSelect
	} from 'carbon-components-svelte';
	import { ReviewsProperties } from '$lib/helpers/reviewsProperties';

	export let data;

	const reviews = data.product.reviews;

	let pageSize = 25;
	let page = 1;

	let modalOpen = false;
	let modalHeading = '';
	let modalContent = '';

	let rows = reviews.map((review) => ({
		...review,
		id: review.ceneoReviewId,
		recommendation: review.recommendation ? review.recommendation : 'Brak',
		verified: review.verified ? 'Tak' : 'Nie'
	}));

	const formatDate = (date: Date | null) => {
		if (!date) {
			return '-';
		}

		return new Intl.DateTimeFormat().format(date);
	};

	const reviewsProperties = new ReviewsProperties(reviews);

	const recommendations = reviewsProperties.recommendations();
	const verifiedOptions = reviewsProperties.verifiedOptions();
	const scores = reviewsProperties.scores();
	const pros = reviewsProperties.pros();
	const cons = reviewsProperties.cons();
</script>

<Modal bind:open={modalOpen} bind:modalHeading passiveModal>{modalContent}</Modal>

<Grid>
	<Row>
		<Column lg={8}>
			<h1>{data.product.name}</h1>
		</Column>
	</Row>
	<Row padding>
		<Column lg={4}>
			<Dropdown
				titleText="Rekomendacja"
				selectedId={-1}
				items={[
					{ id: -1, text: 'Wszystkie' },
					...recommendations.map((value, index) => ({
						id: index,
						text: value ? value : 'Brak'
					}))
				]}
			/>
		</Column>
		<Column lg={4}>
			<Dropdown
				titleText="Potwierdzona zakupen"
				selectedId={-1}
				items={[
					{ id: -1, text: 'Wszystkie' },
					...verifiedOptions.map((value, index) => ({
						id: index,
						text: value ? 'Tak' : 'Nie'
					}))
				]}
			/>
		</Column>
		<Column lg={4}>
			<MultiSelect
				titleText="Ocena"
				label="Wybierz oceny..."
				items={scores.map((value, index) => ({
					id: index,
					text: value.toString()
				}))}
			/>
		</Column>
	</Row>
	<Row padding>
		<Column lg={6}>
			<MultiSelect
				titleText="Zalety"
				label="Wybierz zalety..."
				items={pros.map((value, index) => ({
					id: index,
					text: value
				}))}
			/>
		</Column>
		<Column lg={6}>
			<MultiSelect
				titleText="Wady"
				label="Wybierz zalety..."
				items={cons.map((value, index) => ({
					id: index,
					text: value
				}))}
			/>
		</Column>
	</Row>
</Grid>

<div class="table-container">
	<Grid>
		<Row>
			<Column>
				<DataTable
					sortable
					headers={[
						{ key: 'author', value: 'Autor' },
						{
							key: 'recommendation',
							value: 'Rekomendacja'
						},
						{ key: 'score', value: 'Ocena' },
						{
							key: 'verified',
							value: 'Potwierdzona zakupem'
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
					{rows}
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
</div>

<style>
	h1 {
		margin-bottom: 2rem;
	}

	.row {
		padding: 1em 0;
	}

	.table-container {
		margin-top: 2.5em;
	}
</style>
