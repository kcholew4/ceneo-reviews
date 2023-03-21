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
		Column,
		MultiSelect,
		FormGroup
	} from 'carbon-components-svelte';
	import _ from 'lodash';

	export let data;

	const dateTimeFormat = new Intl.DateTimeFormat('default', {
		year: 'numeric',
		month: 'numeric',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
		second: 'numeric',
		hour12: false
	});

	const rows = data.reviews.map((review, index) => ({
		...review,
		id: index,
		review_id: review.id,
		recommendation: review.recommendation ?? 'Brak',
		verified: review.verified ? 'Tak' : 'Nie',
		published_date: new Date(review.published_date).valueOf() ?? 0,
		bought_date: new Date(review.bought_date).valueOf() ?? 0
	}));

	let displayedRows = rows;
	let pageSize = 20;
	let page = 1;
	let filteredRowIds = [];

	const availableScores = rows.reduce((acc, current) => {
		const score = current.score_count;
		if (acc.includes(score)) {
			return acc;
		}

		return [...acc, score];
	}, []);

	const prosList = rows.reduce((acc, current) => {
		current.pros.forEach((single) => {
			if (!acc.includes(single)) {
				acc.push(single);
			}
		});

		return acc;
	}, []);

	const consList = rows.reduce((acc, current) => {
		current.cons.forEach((single) => {
			if (!acc.includes(single)) {
				acc.push(single);
			}
		});

		return acc;
	}, []);

	// console.log(prosList, consList);

	const createRecommendationFilter = (recommendation) => (rows) => {
		if (recommendation === 'default') {
			return rows;
		}

		return rows.filter((row) => row.recommendation === recommendation);
	};

	const createScoreFilter = (scores) => (rows) => {
		if (scores.length === 0) {
			return rows;
		}

		return rows.filter((row) => scores.includes(row.score_count.toString()));
	};

	const createVerifiedFilter = (verified) => (rows) => {
		if (verified === 'default') {
			return rows;
		}

		return rows.filter((row) => verified.includes(row.verified));
	};

	const createProsFilter = (pros) => (rows) => {
		if (pros.length === 0) {
			return rows;
		}

		return rows.filter((row) => row.pros.some((value) => pros.includes(value)));
	};

	const createConsFilter = (cons) => (rows) => {
		if (cons.length === 0) {
			return rows;
		}

		return rows.filter((row) => row.cons.some((value) => cons.includes(value)));
	};

	let filters = {};

	const addFilter = (name, filter) => (filters[name] = filter);

	const applyFilters = (filters) => {
		let result = rows;

		Object.values(filters).forEach((filter) => {
			result = filter(result);
		});

		return result;
	};

	$: displayedRows = applyFilters(filters);

	let recommendationSelect = undefined;
	let verfiedSelect = undefined;
	let scoreSelectedIds = [];
	let prosSelectedIds = [];
	let consSelectedIds = [];

	const resetFilters = () => {
		recommendationSelect = undefined;
		verfiedSelect = undefined;
		scoreSelectedIds = [];
		prosSelectedIds = [];
		consSelectedIds = [];

		filters = {};
	};
</script>

<div class="container">
	<h2>{data.name}</h2>
	<Button on:click={() => goto(`/products/${data.product_id}/statistics`)}>Idź do wykresów</Button>
</div>
<div class="filters container">
	<Grid>
		<Row padding>
			<Column lg={{ span: 4 }}>
				<Select
					labelText="Rekomendacja"
					bind:selected={recommendationSelect}
					on:change={(e) => addFilter('recommendation', createRecommendationFilter(e.target.value))}
				>
					<SelectItem value="default" text="Wszystkie" />
					<SelectItem value="Polecam" text="Polecam" />
					<SelectItem value="Nie polecam" text="Nie polecam" />
					<SelectItem value="Brak" text="Brak" />
				</Select>
			</Column>
			<Column lg={{ span: 4 }}>
				<Select
					labelText="Potwierdzona zakupem"
					bind:selected={verfiedSelect}
					on:change={(e) => addFilter('verfied', createVerifiedFilter(e.target.value))}
				>
					<SelectItem value="default" text="Wszystkie" />
					<SelectItem value="Tak" text="Tak" />
					<SelectItem value="Nie" text="Nie" />
				</Select>
			</Column>
			<Column lg={{ span: 8 }}>
				<MultiSelect
					titleText="Ocena"
					bind:selectedIds={scoreSelectedIds}
					label="Wybierz ocene..."
					items={availableScores.map((single, index) => ({ id: index, text: single.toString() }))}
					on:select={({ detail }) => {
						addFilter('score', createScoreFilter(detail.selected.map(({ text }) => text)));
					}}
				/>
			</Column>
		</Row>
		<Row padding>
			<Column lg={{ span: 8 }}>
				<MultiSelect
					titleText="Zalety"
					bind:selectedIds={prosSelectedIds}
					label="Wybierz zalety..."
					items={prosList.map((single, index) => ({ id: index, text: single }))}
					on:select={({ detail }) => {
						addFilter('pros', createProsFilter(detail.selected.map(({ text }) => text)));
					}}
				/>
			</Column>
			<Column lg={{ span: 8 }}>
				<MultiSelect
					titleText="Wady"
					bind:selectedIds={consSelectedIds}
					label="Wybierz wady..."
					items={consList.map((single, index) => ({ id: index, text: single }))}
					on:select={({ detail }) => {
						addFilter('pros', createConsFilter(detail.selected.map(({ text }) => text)));
					}}
				/>
			</Column>
		</Row>
		<Row padding>
			<Column style="display: flex; justify-content: end;">
				<Button kind="tertiary" on:click={() => resetFilters()}>Wyczyść filtry</Button>
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
			{
				key: 'published_date',
				value: 'Data opublikowania',
				display: (value) =>
					value ? dateTimeFormat.format(new Date(parseInt(value))) : 'Brak danych'
			},
			{
				key: 'bought_date',
				value: 'Data zakupu',
				display: (value) =>
					value ? dateTimeFormat.format(new Date(parseInt(value))) : 'Brak danych'
			},
			{ key: 'votes_yes', value: 'Głosy za' },
			{ key: 'votes_no', value: 'Głosy przeciw' },
			// { key: 'text', value: 'Treść' },
			{ key: 'pros', value: 'Zalety', display: (pros) => pros.join(', ') },
			{ key: 'cons', value: 'Wady', display: (cons) => cons.join(', ') }
		]}
		rows={displayedRows}
		{pageSize}
		{page}
	>
		<Toolbar>
			<ToolbarContent>
				<ToolbarSearch
					persistent
					shouldFilterRows={(row, value) => {
						const filterableRow = {
							...row,
							pros: row.pros.join(', '),
							cons: row.cons.join(', ')
						};

						return Object.values(filterableRow).some((cell) =>
							String(cell).toLowerCase().includes(value.toLowerCase())
						);
					}}
					bind:filteredRowIds
					placeholder="Szukaj..."
				/>
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
