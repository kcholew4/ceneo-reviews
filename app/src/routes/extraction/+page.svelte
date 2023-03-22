<script>
	import { env } from '$env/dynamic/public';
	import { goto } from '$app/navigation';
	import { TextInput, Button, FormGroup, Form, ToastNotification } from 'carbon-components-svelte';

	let id = null;

	const productExists = async (id) => {
		const url = `https://${env.PUBLIC_API_URL}/api/products/${id}/check`;

		const res = await fetch(url);

		if (res.status == 200) {
			return true;
		}

		return false;
	};

	let showNotFound = false;
</script>

{#if showNotFound}
	<div class="alert">
		<ToastNotification
			lowContrast
			kind="error"
			title="Błąd"
			subtitle="Nie znaleziono produktu o podanym ID."
			on:close={() => {
				showNotFound = false;
			}}
		/>
	</div>
{/if}

<div class="container">
	<h1>Wyszukaj produkt</h1>
	<p>Pobierz opinie o produkcie z portalu ceneo.pl wpisując jego id.</p>
	<Form
		on:submit={async (e) => {
			e.preventDefault();

			if (!(await productExists(id))) {
				console.log('product does not exists');
				showNotFound = true;
				return;
			}

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

	.alert {
		position: fixed;
		right: 0;
	}
</style>
