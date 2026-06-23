<script lang="ts">
	import Table from '$lib/Table.svelte';

	interface Product {
		name: string;
		qty: number;
		price: number;
	}

	// Reactive product list
	let products = $state<Product[]>([
		{ name: 'Apple', qty: 2, price: 5 },
		{ name: 'Banana', qty: 3, price: 10 }
	]);

	// Form input states
	let newName = $state('');
	let newQty = $state<number | ''>('');
	let newPrice = $state<number | ''>('');

	// Derived grand total
	const grandTotal = $derived.by(() => {
		return products.reduce((total, product) => total + (product.qty * product.price), 0);
	});

	function addProduct(event: SubmitEvent) {
		event.preventDefault();
		if (!newName || newQty === '' || newPrice === '') {
			return;
		}

		products = [
			...products,
			{
				name: newName,
				qty: Math.floor(Number(newQty)),
				price: Number(newPrice)
			}
		];

		// Clear inputs
		newName = '';
		newQty = '';
		newPrice = '';
	}
</script>

<h1>Product Inventory</h1>

<Table data={products}>
	{#snippet header()}
		<th>Name</th>
		<th>Quantity</th>
		<th>Price</th>
		<th>Total</th>
	{/snippet}

	{#snippet row(product)}
		<td>{product.name}</td>
		<td>{product.qty}</td>
		<td>{product.price}</td>
		<td>{product.qty * product.price}</td>
	{/snippet}
</Table>

<div>
	<h2>Grand Total: <span data-testid="grand-total">{grandTotal}</span></h2>
</div>

<form onsubmit={addProduct}>
	<div>
		<label for="name">Product Name:</label>
		<input
			id="name"
			type="text"
			data-testid="product-name"
			bind:value={newName}
			required
		/>
	</div>
	<div>
		<label for="qty">Quantity:</label>
		<input
			id="qty"
			type="number"
			step="1"
			data-testid="product-qty"
			bind:value={newQty}
			required
		/>
	</div>
	<div>
		<label for="price">Price:</label>
		<input
			id="price"
			type="number"
			step="any"
			data-testid="product-price"
			bind:value={newPrice}
			required
		/>
	</div>
	<button type="submit" data-testid="add-product">Add Product</button>
</form>
