<script lang="ts">
	import {
		Grid,
		Row,
		Column,
		Form,
		TextInput,
		Button,
		InlineNotification
	} from 'carbon-components-svelte';
	import { goto } from '$app/navigation';

	export let form;

	let formErrorMessage = '';

	if (form?.ok === false) {
		if (form.doesNotExist) {
			formErrorMessage = 'Produkt o podanym id nie istnieje.';
		} else if (form.invalidId) {
			formErrorMessage = 'Podane id jest nieprawidłowe.';
		}
	}

	if (form?.ok === true) {
		const { productId } = form;

		goto(`/product/${productId}`).catch(() => {
			formErrorMessage = 'Wystąpił nieoczekiwany błąd, spróbuj ponownie pózniej.';
		});
	}
</script>

<Grid>
	<Row>
		<Column lg={8}>
			<h1>Pobierz opinie z portalu Ceneo.pl</h1>
			<p>
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Explicabo aliquid ab, laudantium
				sequi nulla corrupti quasi esse officiis non provident molestias praesentium in maiores
				vitae distinctio autem nisi quod harum.
			</p>
		</Column>
	</Row>
	<Row>
		<Column lg={8}>
			{#if formErrorMessage}
				<div class="notification-container">
					<InlineNotification lowContrast title="Błąd" subtitle={formErrorMessage} />
				</div>
			{/if}
			<div class="form-container">
				<Form method="POST" action="?/search">
					<TextInput name="productId" labelText="ID produktu" placeholder="Podaj ID produktu..." />
					<div class="submit-button">
						<Button class="submit-button" type="submit">Wyszukaj produkt</Button>
					</div>
				</Form>
			</div>
		</Column>
	</Row>
</Grid>

<style>
	h1 {
		margin-bottom: 0.5em;
	}

	.form-container {
		margin-top: 2.5em;
	}

	.notification-container {
		margin-top: 2.5em;
		margin-bottom: -1em;
	}

	.submit-button {
		margin-top: 1.25em;
	}
</style>
