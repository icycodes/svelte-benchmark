<script>
    import { goto } from '$app/navigation';
    import { browser } from '$app/environment';

    let { data } = $props();

    let searchQuery = $state(data.q);

    // Sync state with data.q only when data.q changes from outside (e.g. navigation)
    // We use a separate variable to track the last known data.q to avoid overwriting user input
    let lastDataQ = data.q;
    $effect(() => {
        if (data.q !== lastDataQ) {
            searchQuery = data.q;
            lastDataQ = data.q;
        }
    });

    $effect(() => {
        if (!browser) return;

        const timeoutId = setTimeout(() => {
            if (searchQuery !== data.q) {
                const url = new URL(window.location.href);
                if (searchQuery) {
                    url.searchParams.set('q', searchQuery);
                } else {
                    url.searchParams.delete('q');
                }
                lastDataQ = searchQuery; // Anticipate the change to avoid overwrite
                goto(url.pathname + url.search, {
                    replaceState: true,
                    keepFocus: true,
                    noScroll: true
                });
            }
        }, 200);

        return () => clearTimeout(timeoutId);
    });
</script>

<h1>Products</h1>

<form method="get" action="/products">
    <input
        type="text"
        name="q"
        bind:value={searchQuery}
        placeholder="Search products..."
        data-testid="search-input"
    />
    <button type="submit" class="sr-only">Search</button>
</form>

<p>Showing {data.products.length} products</p>

<ul>
    {#each data.products as product (product.id)}
        <li data-testid="product-item">
            {product.name} - ${product.price}
        </li>
    {/each}
</ul>

<style>
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
    }
</style>
