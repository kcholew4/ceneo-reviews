<div class="container">
	<div class="content">
		<h1>Cel aplikacji</h1>
		<p>Otrzymywanie opinii o produkcie i statystyk o nich.</p>
	</div>
	<div class="content">
		<h1>Opis działania aplikacji</h1>
		<p>Nalezy prześć na stronę ekstrakcji, podać id produktu i kliknąć przycisk</p>
	</div>
	<div class="content">
		<h1>Zastosowane biblioteki</h1>
		<p>
			Po stronie backendu zastosowano m.in bibliotekę Flask z Flask RESTful, beautiful soup,
			requests oraz pymongo. Na stronie front end zastosowano metaframework SvelteKi do zbudowanie
			reaktywnej aplikacji SPA oraz Carbon Design Components do stworzenia interfejsu uzytkownika.
		</p>
	</div>
	<div class="content">
		<h1>Zastosowane podejścia</h1>
		<p>
			Zastosowano podejście API first czyli w pythonie stworzone zostało RESTowe API HTTP, które
			jest wykorzystywane w aplikacji stworznej SvelteKit. Dlatego obie częsci aplikacji mozna
			hostować odzielnie.
		</p>
	</div>
</div>

<style lang="scss">
	.container {
		max-width: 1000px;
		margin: 0 auto;
		padding: 0 2em;
	}

	.content {
		padding-top: 0.5em;
		padding-bottom: 0.5em;
	}

	h1 {
		margin-bottom: 0.5em;
	}
</style>
