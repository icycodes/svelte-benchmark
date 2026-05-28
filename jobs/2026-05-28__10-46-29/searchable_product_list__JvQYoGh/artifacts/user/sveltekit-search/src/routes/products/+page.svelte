<script>
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';

    const { data } = $props();

    let query = $state(data.q ?? '');
    const count = $derived(data.products.length);

    $effect(() => {
        query = data.q ?? '';
    });

    $effect(() => {
        if (!browser) {
            return;
        }

        const currentQuery = query;
        const serverQuery = data.q ?? '';

        if (currentQuery === serverQuery) {
            return;
        }

        const timeout = setTimeout(() => {
            const target = currentQuery
                ? `/products?q=${encodeURIComponent(currentQuery)}`
                : '/products';

            goto(target, {
                replaceState: true,
                keepFocus: true
            });
        }, 200);

        return () => clearTimeout(timeout);
    });
</script>

<svelte:head>
    <title>Products</title>
</svelte:head>

<h1>Products</h1>

<form method="get" action="/products">
    <label>
        Search
        <input
            type="search"
            name="q"
            data-testid="search-input"
            bind:value={query}
            autocomplete="off"
        />
    </label>
</form>

<p>{count} products shown</p>

<ul>
    {#each data.products as product}
        <li data-testid="product-item">
            <strong>{product.name}</strong> — ${product.price}
        </li>
    {/each}
</ul>
