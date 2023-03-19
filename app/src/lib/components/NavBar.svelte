<script>
	import {
		Header,
		HeaderNav,
		HeaderNavItem,
		SkipToContent,
		SideNav,
		SideNavItems,
		SideNavLink
	} from 'carbon-components-svelte';

	let isSideNavOpen = false;
</script>

<Header platformName="Ceneo Reviews" bind:isSideNavOpen expandedByDefault={false}>
	<svelte:fragment slot="skip-to-content">
		<SkipToContent />
	</svelte:fragment>
	<HeaderNav>
		<HeaderNavItem href="/" text="Strona główna" />
		<HeaderNavItem href="/extraction" text="Ekstrakcja opinii" />
		<HeaderNavItem href="/products" text="Lista produktów" />
		<HeaderNavItem href="/about-me" text="O autorze" />
	</HeaderNav>
</Header>

<SideNav bind:isOpen={isSideNavOpen}>
	<SideNavItems>
		<SideNavLink href="/" text="Strona główna" />
		<SideNavLink href="/extraction" text="Ekstrakcja opinii" />
		<SideNavLink href="/products" text="Lista produktów" />
		<SideNavLink href="/about-me" text="O autorze" />
	</SideNavItems>
</SideNav>
