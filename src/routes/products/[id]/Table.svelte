<script lang="ts">
  import {
    Grid,
    Row,
    Column,
    DataTable,
    Pagination,
    Modal,
    Button
  } from 'carbon-components-svelte';
  import type { Review } from '@prisma/client';

  export let reviews: Review[];

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

  let rows: ReturnType<typeof reviewsToRows>;

  $: rows = reviewsToRows(reviews);
</script>

<Modal bind:open={modalOpen} bind:modalHeading passiveModal>{modalContent}</Modal>

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

<style>
  .row {
    padding: 1em 0;
  }
</style>
