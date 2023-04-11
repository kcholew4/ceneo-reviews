<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Grid, Row, Column, Dropdown, MultiSelect } from 'carbon-components-svelte';
  import { ReviewsProperties } from '$lib/helpers/reviewsProperties';
  import { ReviewsFilters, type FilterFunction } from '$lib/helpers/reviewsFilters';
  import type { Review } from '@prisma/client';

  export let reviews: Review[];

  const reviewsFilters = new ReviewsFilters(reviews);
  const reviewsProperties = new ReviewsProperties(reviews);

  const recommendations = reviewsProperties.recommendations();
  const verifiedOptions = reviewsProperties.verifiedOptions();
  const scores = reviewsProperties.scores();
  const pros = reviewsProperties.pros();
  const cons = reviewsProperties.cons();

  let filters: {
    [index: string]: FilterFunction;
  } = {};

  const dispatch = createEventDispatcher();

  $: dispatch('filter', {
    reviews: reviewsFilters.apply(Object.values(filters))
  });
</script>

<Grid>
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
