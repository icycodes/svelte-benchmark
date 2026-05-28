<script lang="ts">
  import Table from '$lib/Table.svelte';

  type Product = {
    name: string;
    price: number;
    quantity: number;
  };

  type User = {
    name: string;
    email: string;
    role: string;
  };

  const products: Product[] = [
    { name: 'Svelte Starter Kit', price: 49.99, quantity: 12 },
    { name: 'Svelte T-Shirt', price: 24.5, quantity: 48 },
    { name: 'Sticker Pack', price: 6.75, quantity: 120 },
    { name: 'Desk Mat', price: 34.25, quantity: 15 },
    { name: 'Coffee Mug', price: 14.99, quantity: 36 }
  ];

  const users: User[] = [
    { name: 'Ada Lovelace', email: 'ada@example.com', role: 'Administrator' },
    { name: 'Grace Hopper', email: 'grace@example.com', role: 'Editor' },
    { name: 'Linus Torvalds', email: 'linus@example.com', role: 'Viewer' },
    { name: 'Margaret Hamilton', email: 'margaret@example.com', role: 'Editor' }
  ];

  let productFilter = $state('');

  const filteredProducts = $derived(() => {
    const normalized = productFilter.trim().toLowerCase();
    if (!normalized) {
      return products;
    }

    return products.filter((product) => product.name.toLowerCase().includes(normalized));
  });

  const totalInventoryValue = $derived(() =>
    filteredProducts.reduce((sum, product) => sum + product.price * product.quantity, 0)
  );
</script>

<main>
  <section>
    <h1>Inventory Overview</h1>
    <div>
      <label for="product-filter">Filter products</label>
      <input
        id="product-filter"
        type="text"
        placeholder="Type a product name"
        bind:value={productFilter}
      />
    </div>
    <p>Filtered inventory total: {"$" + totalInventoryValue.toFixed(2)}</p>

    <Table data={filteredProducts}>
      {#snippet header()}
        <th>Product</th>
        <th>Unit price</th>
        <th>Quantity</th>
        <th>Line total</th>
      {/snippet}

      {#snippet row(product)}
        <td>{product.name}</td>
        <td>{"$" + product.price.toFixed(2)}</td>
        <td>{product.quantity}</td>
        <td>{"$" + (product.price * product.quantity).toFixed(2)}</td>
      {/snippet}
    </Table>
  </section>

  <section>
    <h2>Team Directory</h2>
    <Table data={users}>
      {#snippet header()}
        <th>Name</th>
        <th>Email</th>
        <th>Role</th>
      {/snippet}

      {#snippet row(user)}
        <td>{user.name}</td>
        <td>{user.email}</td>
        <td>{user.role}</td>
      {/snippet}
    </Table>
  </section>
</main>

<style>
  main {
    font-family: system-ui, sans-serif;
    margin: 2rem auto;
    max-width: 960px;
    padding: 0 1.5rem 3rem;
  }

  section {
    margin-bottom: 3rem;
  }

  h1,
  h2 {
    margin-bottom: 0.75rem;
  }

  label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  input {
    border: 1px solid #cbd5f5;
    border-radius: 0.5rem;
    padding: 0.5rem 0.75rem;
    width: min(320px, 100%);
  }

  table {
    border-collapse: collapse;
    margin-top: 1rem;
    width: 100%;
  }

  th,
  td {
    border-bottom: 1px solid #e2e8f0;
    padding: 0.5rem 0.75rem;
    text-align: left;
  }

  thead th {
    background: #f8fafc;
    font-size: 0.9rem;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }
</style>
