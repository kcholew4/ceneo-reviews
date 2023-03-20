<script>
	import { PieChart, BarChartSimple } from '@carbon/charts-svelte';
	import { Grid, Row, Column, Link } from 'carbon-components-svelte';

	export let data;

	const { reviews } = data;

	//console.log(reviews);

	const recommendationStats = reviews.reduce(
		(acc, current) => {
			switch (current.recommendation) {
				case 'Polecam':
					acc.recommended++;
					break;

				case 'Nie polecam':
					acc.not_recommended++;
					break;

				default:
					acc.no_data++;
					break;
			}

			return acc;
		},
		{
			recommended: 0,
			not_recommended: 0,
			no_data: 0
		}
	);

	const createScoreGroups = () => {
		const scoreStats = reviews.reduce((acc, current) => {
			if (current.score_count in acc) {
				acc[current.score_count]++;
			} else {
				acc[current.score_count] = 0;
			}
			return acc;
		}, {});

		return Object.entries(scoreStats)
			.map(([group, value]) => ({ group, value }))
			.sort((a, b) => parseFloat(a.group) - parseFloat(b.group));
	};

	// console.log(createScoreGroups());
</script>

<Grid>
	<Row>
		<Column lg={{ offset: 4 }}>
			<h2 style="margin-bottom: 1em">Statystyki dla {data.name}</h2>
		</Column>
	</Row>
	<Row>
		<Column lg={{ span: 8, offset: 4 }}>
			<div class="chart">
				<PieChart
					theme="g90"
					data={[
						{
							group: 'Polecam',
							value: recommendationStats.recommended
						},
						{
							group: 'Nie polecam',
							value: recommendationStats.not_recommended
						},
						{
							group: 'Brak danych',
							value: recommendationStats.no_data
						}
					]}
					options={{
						title: 'Udział rekomendacji w ogólnej liczbie opinii',
						resizable: true,
						height: '400px',
						legend: {
							alignment: 'center'
						},
						pie: {
							alignment: 'center'
						}
					}}
				/>
			</div>
		</Column>
	</Row>
	<Row>
		<Column lg={{ span: 8, offset: 4 }}>
			<div class="chart">
				<BarChartSimple
					theme="g90"
					data={createScoreGroups()}
					options={{
						title: 'Liczba opinii z poszczególnymi liczbami gwiazdek',
						resizable: true,
						height: '400px',
						axes: {
							left: {
								mapsTo: 'value'
							},
							bottom: {
								mapsTo: 'group',
								scaleType: 'labels'
							}
						}
					}}
				/>
			</div>
		</Column>
	</Row>
	<Row>
		<Column lg={{ offset: 4 }}>
			<Link href="/products/{data.product_id}">Powrót do produktu</Link>
		</Column>
	</Row>
</Grid>

<style>
	.chart {
		margin-bottom: 2em;
	}
</style>
