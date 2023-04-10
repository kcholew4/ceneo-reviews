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
	import { ReviewsFilters, type FilterFunction } from '$lib/helpers/reviewsFilters';
	import type { Review } from '@prisma/client';

	export let data;

	const reviews = data.product.reviews;

	let pageSize = 25;
	let page = 1;

	let modalOpen = false;
	let modalHeading = '';
	let modalContent = '';

	const reviewsToRows = (reviews: Review[]) => {
		return reviews.map((review) => ({
			...review,
			id: review.ceneoReviewId,
			recommendation: review.recommendation ? review.recommendation : 'Brak',
			verified: review.verified ? 'Tak' : 'Nie'
		}));
	};

	const formatDate = (date: Date | null) => {
		if (!date) {
			return '-';
		}

		return new Intl.DateTimeFormat().format(date);
	};

	const reviewsFilters = new ReviewsFilters(reviews);
	const reviewsProperties = new ReviewsProperties(reviews);

	const recommendations = reviewsProperties.recommendations();
	const verifiedOptions = reviewsProperties.verifiedOptions();
	const scores = reviewsProperties.scores();
	const pros = reviewsProperties.pros();
	const cons = reviewsProperties.cons();

	let rows: ReturnType<typeof reviewsToRows>;

	let filters: {
		[index: string]: FilterFunction;
	} = {};

	$: {
		const displayedReviews = reviewsFilters.apply(Object.values(filters));
		rows = reviewsToRows(displayedReviews);
	}
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
				on:select={(event) => {
					const id = event.detail.selectedId;

					if (id < 0) {
						delete filters.recommendation;
						return (filters = filters);
					}

					filters.recommendation = ReviewsFilters.createRecommendationFilter(recommendations[id]);
				}}
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
				on:select={(event) => {
					const id = event.detail.selectedId;

					if (id < 0) {
						delete filters.verified;
						return (filters = filters);
					}

					filters.verified = ReviewsFilters.createVerifiedFilter(verifiedOptions[id]);
				}}
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
				on:select={(event) => {
					if (event.detail.selectedIds.length === 0) {
						delete filters.scores;
						return (filters = filters);
					}

					filters.scores = ReviewsFilters.createScoresFilter(
						event.detail.selected.map((single) => parseFloat(single.text))
					);
				}}
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
				on:select={(event) => {
					if (event.detail.selectedIds.length === 0) {
						delete filters.pros;
						return (filters = filters);
					}

					filters.pros = ReviewsFilters.createProsFilter(
						event.detail.selected.map(({ text }) => text)
					);
				}}
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
				on:select={(event) => {
					if (event.detail.selectedIds.length === 0) {
						delete filters.cons;
						return (filters = filters);
					}

					filters.cons = ReviewsFilters.createConsFilter(
						event.detail.selected.map(({ text }) => text)
					);
				}}
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
