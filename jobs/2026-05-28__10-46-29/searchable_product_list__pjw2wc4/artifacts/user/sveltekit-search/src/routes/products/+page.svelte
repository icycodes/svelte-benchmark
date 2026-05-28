<script>
  import { goto } from '$app/navigation';

  /** @type {{ data: { q: string, products: Array<{id: number, name: string, price: number}> } }} */
  let { data } = $props();

  // searchValue tracks the live input; initialised from SSR data and kept in sync
  // when data.q changes (e.g. browser back/forward).
  let searchValue = $state(data.q);

  // When the load function produces a new data.q (navigation), sync the input.
  $effect(() => {
    searchValue = data.q;
  });

  // Debounced URL sync: fire 200 ms after the user stops typing.
  $effect(() => {
    const value = searchValue;
    const timer = setTimeout(() => {
      const params = value ? `?q=${encodeURIComponent(value)}` : '';
      goto(`/products${params}`, { replaceState: true, keepFocus: true });
    }, 200);

    return () => clearTimeout(timer);
  });

  let count = $derived(data.products.length);
</script>

<main>
  <h1>Products</h1>

  <form method="get" action="/products">
    <label for="search">Search products</label>
    <input
      id="search"
      type="search"
      name="q"
      data-testid="search-input"
      value={searchValue}
      oninput={(e) => { searchValue = e.currentTarget.value; }}
      placeholder="Type to filter…"
      autocomplete="off"
    />
    <button type="submit">Search</button>
  </form>

  <p>Showing {count} product{count === 1 ? '' : 's'}</p>

  <ul>
    {#each data.products as product (product.id)}
      <li data-testid="product-item">
        <strong>{product.name}</strong> — ${product.price}
      </li>
    {/each}
  </ul>
</main>
