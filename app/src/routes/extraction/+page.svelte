<script>
	import { goto } from '$app/navigation';
	import { TextInput, Button, FormGroup, Form } from 'carbon-components-svelte';

	let id = null;
</script>

<div class="container">
	<h1>Wyszukaj produkt</h1>
	<p>Pobierz opinie o produkcie z portalu ceneo.pl wpisując jego id.</p>
	<Form
		on:submit={(e) => {
			e.preventDefault();
			goto(`/products/${id}`);
		}}
	>
		<FormGroup>
			<TextInput labelText="ID produktu" placeholder="Wpisz ID produktu..." bind:value={id} />
		</FormGroup>
		<Button type="submit">Wyślij</Button>
	</Form>
</div>

<style>
	.container {
		max-width: 1000px;
		margin: 0 auto;
	}

	h1 {
		margin-bottom: 0.5em;
	}

	p {
		margin-bottom: 1em;
	}
</style>
