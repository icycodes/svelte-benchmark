<script lang="ts">
	import Table from '$lib/Table.svelte';

	// Datasets
	const products = [
		{ id: 1, name: 'Widget', price: 9.99, quantity: 150 },
		{ id: 2, name: 'Gadget', price: 19.50, quantity: 85 },
		{ id: 3, name: 'Doohickey', price: 4.25, quantity: 300 },
		{ id: 4, name: 'Thingamabob', price: 12.00, quantity: 42 },
		{ id: 5, name: 'Sprocket', price: 2.99, quantity: 500 }
	];

	const users = [
		{ id: 101, name: 'Alice Smith', email: 'alice@example.com', role: 'Admin' },
		{ id: 102, name: 'Bob Johnson', email: 'bob@example.com', role: 'User' },
		{ id: 103, name: 'Charlie Brown', email: 'charlie@example.com', role: 'Editor' }
	];

	// State and Derived for Products table
	let productFilter = $state('');
	
	let filteredProducts = $derived(
		products.filter(p => p.name.toLowerCase().includes(productFilter.toLowerCase()))
	);
	
	let inventoryTotal = $derived(
		filteredProducts.reduce((sum, p) => sum + (p.price * p.quantity), 0)
	);
</script>

<h1>Svelte 5 Snippets Table Demo</h1>

<h2>Products</h2>
<div class="filter-container">
	<label for="product-filter">Filter products by name:</label>
	<input id="product-filter" type="text" bind:value={productFilter} placeholder="Type to filter..." />
</div>

<p class="summary">
	Total inventory value: <strong>${inventoryTotal.toFixed(2)}</strong>
</p>

<Table data={filteredProducts}>
	{#snippet header()}
		<tr>
			<th>Name</th>
			<th>Unit Price</th>
			<th>Quantity</th>
			<th>Line Total</th>
		</tr>
	{/snippet}
	{#snippet row(item)}
		<td>{item.name}</td>
		<td>${item.price.toFixed(2)}</td>
		<td>{item.quantity}</td>
		<td>${(item.price * item.quantity).toFixed(2)}</td>
	{/snippet}
</Table>

<h2>Users</h2>

<Table data={users}>
	{#snippet header()}
		<tr>
			<th>Name</th>
			<th>Email</th>
			<th>Role</th>
		</tr>
	{/snippet}
	{#snippet row(item)}
		<td>{item.name}</td>
		<td>{item.email}</td>
		<td>{item.role}</td>
	{/snippet}
</Table>

<style>
	:global(body) {
		font-family: system-ui, -apple-system, sans-serif;
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
	}
	.filter-container {
		margin-bottom: 1rem;
	}
	input {
		padding: 0.5rem;
		font-size: 1rem;
		border: 1px solid #ccc;
		border-radius: 4px;
	}
	.summary {
		font-size: 1.2rem;
		margin-bottom: 1rem;
		padding: 1rem;
		background-color: #e9ecef;
		border-radius: 4px;
	}
</style>
