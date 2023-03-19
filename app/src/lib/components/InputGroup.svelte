<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let id = null;
</script>

<div class="group">
	<input type="text" placeholder="id produktu" bind:value={id} />
	<button on:click={() => dispatch('send', { id })} disabled={id === null}>Szukaj</button>
</div>

<style lang="scss">
	input {
		font-family: inherit;
		outline: none;
		padding: 0.5em 1em;
		font-size: 1em;
		border-radius: 0.5em;
		border: 1px solid #b0b0b0;

		&::placeholder {
			color: rgb(200, 200, 200);
		}
	}

	.group {
		display: flex;
		gap: 0.5em;
		font-size: 1.125em;
	}

	button {
		font-family: inherit;
		outline: none;
		font-size: 1em;
		border: none;
		color: white;
		padding: 0.5em 1em;
		border-radius: 0.5em;
		background-color: #29405a;

		&:hover {
			background-color: #1a293a;
			cursor: pointer;
		}

		&:disabled {
			background-color: #29405a;
			cursor: not-allowed;
		}
	}
</style>
