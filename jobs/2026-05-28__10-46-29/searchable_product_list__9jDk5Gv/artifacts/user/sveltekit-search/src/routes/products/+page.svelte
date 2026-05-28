<script>
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';

	let { data } = $props();
	
	let initialQ = data.q;
	let q = $state(initialQ);
	
	// Keep the local state in sync if data.q changes (e.g. via back button)
	$effect(() => {
		if (q !== data.q) {
			q = data.q;
		}
	});

	let timeout;

	$effect(() => {
		if (!browser) return;
		
		// Skip navigating if the query is exactly what we started with in the URL
		if (q === data.q) return;

		clearTimeout(timeout);
		timeout = setTimeout(() => {
			const url = new URL(window.location.href);
			if (q) {
				url.searchParams.set('q', q);
			} else {
				url.searchParams.delete('q');
			}
			goto(url.pathname + url.search, { replaceState: true, keepFocus: true });
		}, 300);
		
		return () => clearTimeout(timeout);
	});
</script>

<h1>Products</h1>

<form method="get" action="/products">
	<input 
		type="text" 
		name="q" 
		data-testid="search-input" 
		bind:value={q} 
		placeholder="Search products..." 
	/>
	<button type="submit">Search</button>
</form>

<p>Showing {data.products.length} product(s)</p>

<ul>
	{#each data.products as product (product.id)}
		<li data-testid="product-item">
			{product.name} - ${product.price}
		</li>
	{/each}
</ul>
