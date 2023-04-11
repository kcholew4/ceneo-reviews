<script lang="ts">
  import { Grid, Row, Column } from 'carbon-components-svelte';
  import Filters from './Filters.svelte';
  import Table from './Table.svelte';

  export let data;

  let reviews = data.product.reviews;
</script>

<Grid>
  <Row>
    <Column lg={8}>
      <h1>{data.product.name}</h1>
    </Column>
  </Row>
</Grid>

<Filters
  {reviews}
  on:filter={(event) => {
    reviews = event.detail.reviews;
  }}
/>

<div class="table-container">
  <Table {reviews} />
</div>

<style>
  h1 {
    margin-bottom: 2rem;
  }

  .table-container {
    margin-top: 2.5em;
  }
</style>
