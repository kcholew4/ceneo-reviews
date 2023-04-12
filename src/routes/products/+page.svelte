<script lang="ts">
  import { Grid, Row, Column, Tile, Link } from 'carbon-components-svelte';

  export let data;
</script>

<Grid>
  <Row>
    <Column>
      <h1>Lista zapisanych produktów</h1>
    </Column>
  </Row>
  <Row>
    <Column>
      <div class="product-cards">
        {#each data.products as product}
          <Tile class="product">
            <div class="product-image">
              {#if product.imageUrl}
                <img src="https:{product.imageUrl}" alt="image of {product.name}" />
              {/if}
            </div>
            <div class="product-title">
              <Link href="/products/{product.ceneoProductId}">
                <h4>{product.name}</h4>
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
      </div>
    </Column>
  </Row>
</Grid>

<style>
  h1 {
    margin-bottom: 1.5em;
  }

  .product-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2em;
  }

  .product-title {
    margin-bottom: 1.5em;
  }

  .product-image {
    display: flex;
    justify-content: center;
    margin: -1em;
    padding: 1em;
    margin-bottom: 1em;
    height: 160px;
    background-color: rgb(235, 235, 235);
  }

  .product-image img {
    height: 100%;
    object-fit: contain;
    mix-blend-mode: multiply;
  }

  .stats > * + * {
    margin-top: 0.75em;
  }
</style>
