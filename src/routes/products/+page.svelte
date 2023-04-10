<script lang="ts">
  import { Grid, Row, Column, Tile, Link } from 'carbon-components-svelte';

  export let data;
</script>

<Grid>
  <Row>
    <Column lg={{ offset: 4, span: 8 }}>
      <h1>Lista zapisanych produktów</h1>
    </Column>
  </Row>
  <Row>
    <Column lg={{ offset: 4, span: 8 }}>
      {#each data.products as product}
        <Tile class="product">
          <div class="product-title">
            <Link href="/products/{product.ceneoProductId}">
              <h3>{product.name}</h3>
            </Link>
          </div>
          <div class="stats">
            <div>Liczba opinii: <strong>{product.overview.reviewsCount}</strong></div>
            <div>Zalety: <strong>{product.overview.prosCount}</strong></div>
            <div>Wady: <strong>{product.overview.consCount}</strong></div>
            <div>Średnia ocena: <strong>{product.overview.averageScore.toFixed(2)}</strong></div>
          </div>
        </Tile>
      {/each}
    </Column>
  </Row>
</Grid>

<style>
  h1 {
    margin-bottom: 1.5em;
  }

  .product-title {
    margin-bottom: 1.5em;
  }

  .stats > * + * {
    margin-top: 0.75em;
  }

  :global(.product + .product) {
    margin-top: 2em;
  }
</style>
