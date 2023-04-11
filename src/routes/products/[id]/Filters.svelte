<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { writable } from 'svelte/store';
  import { Grid, Row, Column, Dropdown, MultiSelect, Button } from 'carbon-components-svelte';
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

  const defaultSelected = () => {
    return {
      recommendation: -1,
      verified: -1,
      scores: [],
      pros: [],
      cons: []
    };
  };

  let selected = defaultSelected();

  const filters = writable<{
    [index: string]: FilterFunction;
  }>({});

  const removeFilter = (filterName: string) => {
    filters.update((value) => {
      delete value[filterName];
      return value;
    });
  };

  const addFilter = (filterName: string, filterFunction: FilterFunction) => {
    filters.update((value) => {
      value[filterName] = filterFunction;
      return value;
    });
  };

  const dispatch = createEventDispatcher();

  filters.subscribe((value) => {
    dispatch('filter', {
      reviews: reviewsFilters.apply(Object.values(value))
    });
  });

  // For some reason this cannot be in on:select in Dropdows

  const recommendationSelect = (index: number) => {
    if (index < 0) {
      return removeFilter('recommendation');
    }

    addFilter('recommendation', ReviewsFilters.createRecommendationFilter(recommendations[index]));
  };

  const verifiedSelect = (index: number) => {
    if (index < 0) {
      return removeFilter('verified');
    }

    addFilter('verified', ReviewsFilters.createVerifiedFilter(verifiedOptions[index]));
  };

  $: recommendationSelect(selected.recommendation);
  $: verifiedSelect(selected.verified);
</script>

<Grid>
  <Row padding>
    <Column lg={4}>
      <Dropdown
        titleText="Rekomendacja"
        bind:selectedId={selected.recommendation}
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
        bind:selectedId={selected.verified}
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
        bind:selectedIds={selected.scores}
        items={scores.map((value, index) => ({
          id: index,
          text: value.toString()
        }))}
        on:select={(event) => {
          console.log('asdfsadf');
          if (event.detail.selectedIds.length === 0) {
            return removeFilter('scores');
          }

          addFilter(
            'scores',
            ReviewsFilters.createScoresFilter(
              event.detail.selected.map((single) => parseFloat(single.text))
            )
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
        bind:selectedIds={selected.pros}
        items={pros.map((value, index) => ({
          id: index,
          text: value
        }))}
        on:select={(event) => {
          if (event.detail.selectedIds.length === 0) {
            return removeFilter('pros');
          }

          addFilter(
            'pros',
            ReviewsFilters.createProsFilter(event.detail.selected.map(({ text }) => text))
          );
        }}
      />
    </Column>
    <Column lg={6}>
      <MultiSelect
        titleText="Wady"
        label="Wybierz zalety..."
        bind:selectedIds={selected.cons}
        items={cons.map((value, index) => ({
          id: index,
          text: value
        }))}
        on:select={(event) => {
          if (event.detail.selectedIds.length === 0) {
            return removeFilter('cons');
          }

          addFilter(
            'cons',
            ReviewsFilters.createConsFilter(event.detail.selected.map(({ text }) => text))
          );
        }}
      />
    </Column>
  </Row>
  <Row padding>
    <Column>
      <Button
        kind="tertiary"
        on:click={(event) => {
          event.preventDefault();
          selected = defaultSelected();
        }}>Wyczyść filtry</Button
      >
    </Column>
  </Row>
</Grid>
