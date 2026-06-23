<script lang="ts">
	import Table from '$lib/Table.svelte';

	type Product = {
		id: number;
		name: string;
		qty: number;
		price: number;
	};

	let products = $state<Product[]>([
		{ id: 1, name: 'Keyboard', qty: 3, price: 45 },
		{ id: 2, name: 'Mouse', qty: 5, price: 18 },
		{ id: 3, name: 'Monitor', qty: 2, price: 220 }
	]);

	let newName = $state('');
	let newQty = $state(1);
	let newPrice = $state(0);

	let grandTotal = $derived(products.reduce((total, product) => total + product.qty * product.price, 0));

	function addProduct(event: SubmitEvent) {
		event.preventDefault();

		const name = newName.trim();
		const qty = Number(newQty);
		const price = Number(newPrice);

		if (!name || !Number.isInteger(qty) || qty < 1 || !Number.isFinite(price) || price < 0) {
			return;
		}

		products = [
			...products,
			{
				id: Date.now(),
				name,
				qty,
				price
			}
		];

		newName = '';
		newQty = 1;
		newPrice = 0;
	}
</script>

<svelte:head>
	<title>Product Inventory</title>
	<meta name="description" content="A generic Svelte 5 snippet-powered product inventory table" />
</svelte:head>

<main>
	<h1>Product Inventory</h1>

	<Table data={products}>
		{#snippet header()}
			<th scope="col">Product</th>
			<th scope="col">Quantity</th>
			<th scope="col">Unit Price</th>
			<th scope="col">Line Total</th>
		{/snippet}

		{#snippet row(product: Product)}
			<td>{product.name}</td>
			<td>{product.qty}</td>
			<td>{product.price}</td>
			<td>{product.qty * product.price}</td>
		{/snippet}
	</Table>

	<p class="total-label">
		Grand total: <strong data-testid="grand-total">{grandTotal}</strong>
	</p>

	<form class="add-product" onsubmit={addProduct} aria-label="Add product">
		<label>
			Product name
			<input data-testid="product-name" type="text" bind:value={newName} required />
		</label>

		<label>
			Quantity
			<input data-testid="product-qty" type="number" min="1" step="1" bind:value={newQty} required />
		</label>

		<label>
			Unit price
			<input data-testid="product-price" type="number" min="0" step="0.01" bind:value={newPrice} required />
		</label>

		<button data-testid="add-product" type="submit">Add product</button>
	</form>
</main>

<style>
	:global(body) {
		margin: 0;
		font-family:
			Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
		background: #f8fafc;
		color: #0f172a;
	}

	main {
		max-width: 56rem;
		margin: 0 auto;
		padding: 3rem 1.5rem;
	}

	h1 {
		margin: 0 0 1.5rem;
		font-size: clamp(2rem, 5vw, 3rem);
	}

	:global(table) {
		width: 100%;
		border-collapse: collapse;
		overflow: hidden;
		border-radius: 0.75rem;
		background: white;
		box-shadow: 0 1rem 2rem rgb(15 23 42 / 0.08);
	}

	:global(th),
	:global(td) {
		padding: 0.875rem 1rem;
		text-align: left;
		border-bottom: 1px solid #e2e8f0;
	}

	:global(th) {
		background: #1e293b;
		color: white;
		font-weight: 700;
	}

	:global(tbody tr:last-child td) {
		border-bottom: 0;
	}

	.total-label {
		margin: 1.5rem 0;
		font-size: 1.25rem;
	}

	.add-product {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 1rem;
		align-items: end;
		padding: 1rem;
		border: 1px solid #e2e8f0;
		border-radius: 0.75rem;
		background: white;
	}

	label {
		display: grid;
		gap: 0.35rem;
		font-weight: 600;
	}

	input,
	button {
		min-height: 2.5rem;
		border-radius: 0.5rem;
		font: inherit;
	}

	input {
		border: 1px solid #cbd5e1;
		padding: 0 0.75rem;
	}

	button {
		border: 0;
		padding: 0 1rem;
		background: #2563eb;
		color: white;
		font-weight: 700;
		cursor: pointer;
	}

	button:hover {
		background: #1d4ed8;
	}

	@media (max-width: 48rem) {
		.add-product {
			grid-template-columns: 1fr;
		}
	}
</style>
