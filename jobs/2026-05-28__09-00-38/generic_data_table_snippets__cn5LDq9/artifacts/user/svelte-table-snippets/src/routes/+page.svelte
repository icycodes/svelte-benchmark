<script>
	import Table from '$lib/Table.svelte';

	const products = [
		{ id: 1, name: 'Laptop', price: 999.99, quantity: 5 },
		{ id: 2, name: 'Mouse', price: 25.50, quantity: 10 },
		{ id: 3, name: 'Keyboard', price: 59.99, quantity: 3 },
		{ id: 4, name: 'Monitor', price: 199.99, quantity: 2 },
		{ id: 5, name: 'Headphones', price: 89.00, quantity: 7 }
	];

	const users = [
		{ id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'Admin' },
		{ id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'User' },
		{ id: 3, name: 'Charlie Brown', email: 'charlie@example.com', role: 'Editor' }
	];

	let filterText = $state('');

	const filteredProducts = $derived(
		products.filter(p => p.name.toLowerCase().includes(filterText.toLowerCase()))
	);

	const totalInventoryValue = $derived(
		filteredProducts.reduce((sum, p) => sum + p.price * p.quantity, 0)
	);
</script>

<h1>Svelte 5 Snippets & Runes Demo</h1>

<section>
	<h2>Products</h2>
	<div class="filter-container">
		<label for="product-filter">Filter by name:</label>
		<input
			id="product-filter"
			type="text"
			bind:value={filterText}
			placeholder="Search products..."
		/>
	</div>

	<Table data={filteredProducts}>
		{#snippet header()}
			<tr>
				<th>Name</th>
				<th>Unit Price</th>
				<th>Quantity</th>
				<th>Line Total</th>
			</tr>
		{/snippet}
		{#snippet row(product)}
			<td>{product.name}</td>
			<td>${product.price.toFixed(2)}</td>
			<td>{product.quantity}</td>
			<td>${(product.price * product.quantity).toFixed(2)}</td>
		{/snippet}
	</Table>

	<p class="inventory-total">
		Total inventory value: <strong>${totalInventoryValue.toFixed(2)}</strong>
	</p>
</section>

<section>
	<h2>Users</h2>
	<Table data={users}>
		{#snippet header()}
			<tr>
				<th>Name</th>
				<th>Email</th>
				<th>Role</th>
			</tr>
		{/snippet}
		{#snippet row(user)}
			<td>{user.name}</td>
			<td>{user.email}</td>
			<td>{user.role}</td>
		{/snippet}
	</Table>
</section>

<style>
	:global(body) {
		font-family: sans-serif;
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
		line-height: 1.5;
	}
	.filter-container {
		margin-bottom: 1rem;
	}
	input {
		padding: 0.4rem;
		font-size: 1rem;
	}
	.inventory-total {
		font-size: 1.2rem;
		text-align: right;
		margin-top: -1rem;
		margin-bottom: 2rem;
	}
	h2 {
		border-bottom: 2px solid #eee;
		padding-bottom: 0.5rem;
	}
</style>
