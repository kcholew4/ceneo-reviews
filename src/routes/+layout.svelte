<script>
	import 'carbon-components-svelte/css/g90.css';
	import {
		Content,
		Header,
		HeaderNav,
		HeaderNavItem,
		SideNav,
		SideNavItems,
		SideNavLink
	} from 'carbon-components-svelte';

	let isSideNavOpen = false;
</script>

<Header platformName="ceneo-reviews" expandedByDefault={false} bind:isSideNavOpen>
	<HeaderNav>
		<HeaderNavItem text="Szukaj" />
		<HeaderNavItem text="Lista produktów" />
	</HeaderNav>
</Header>

<SideNav bind:isOpen={isSideNavOpen}>
	<SideNavItems>
		<SideNavLink text="Szukaj" />
		<SideNavLink text="Lista produktów" />
	</SideNavItems>
</SideNav>

<Content>
	<slot />
</Content>
