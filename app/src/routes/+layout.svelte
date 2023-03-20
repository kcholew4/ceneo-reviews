<script>
	import { setContext } from 'svelte';
	import { writable } from 'svelte/store';
	import NavBar from '$lib/components/NavBar.svelte';

	import '@carbon/styles/css/styles.css';
	import '@carbon/charts/styles.css';
	import 'carbon-components-svelte/css/g90.css';
	import { Content, Theme } from 'carbon-components-svelte';

	export const ssr = false;

	const product = writable({ id: 'asdf' });
	setContext('product', product);
</script>

<!-- <Theme theme="g90" /> -->
<NavBar />
<Content>
	<slot />
</Content>
