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
    <HeaderNavItem text="Szukaj" href="/" />
    <HeaderNavItem text="Lista produktów" href="/products" />
  </HeaderNav>
</Header>

<SideNav bind:isOpen={isSideNavOpen}>
  <SideNavItems>
    <SideNavLink text="Szukaj" href="/" />
    <SideNavLink text="Lista produktów" />
  </SideNavItems>
</SideNav>

<Content>
  <slot />
</Content>
