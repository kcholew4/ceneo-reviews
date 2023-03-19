<script>
	import { setContext } from 'svelte';
	import { writable } from 'svelte/store';
	import NavBar from '$lib/components/NavBar.svelte';

	import 'carbon-components-svelte/css/g90.css';
	import { Content } from 'carbon-components-svelte';

	export const ssr = false;

	const product = writable({ id: 'asdf' });
	setContext('product', product);
</script>

<NavBar />
<Content>
	<slot />
</Content>
