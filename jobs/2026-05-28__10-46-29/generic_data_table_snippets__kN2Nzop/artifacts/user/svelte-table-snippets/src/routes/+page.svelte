<script lang="ts">
	import Table from '$lib/Table.svelte';

	// ── Datasets ─────────────────────────────────────────────────────────────

	interface Product {
		name: string;
		price: number;
		quantity: number;
	}

	interface User {
		name: string;
		email: string;
		role: string;
	}

	const products: Product[] = [
		{ name: 'Wireless Keyboard', price: 49.99, quantity: 120 },
		{ name: 'USB-C Hub',         price: 34.99, quantity: 85  },
		{ name: 'Mechanical Mouse',  price: 59.99, quantity: 60  },
		{ name: 'Monitor Stand',     price: 29.99, quantity: 200 },
		{ name: 'Webcam HD 1080p',   price: 79.99, quantity: 45  },
		{ name: 'Laptop Sleeve',     price: 19.99, quantity: 310 },
	];

	const users: User[] = [
		{ name: 'Alice Martin',  email: 'alice@example.com',  role: 'Admin'    },
		{ name: 'Bob Nguyen',    email: 'bob@example.com',    role: 'Editor'   },
		{ name: 'Carol Smith',   email: 'carol@example.com',  role: 'Viewer'   },
		{ name: 'David Lee',     email: 'david@example.com',  role: 'Editor'   },
		{ name: 'Eva Rossi',     email: 'eva@example.com',    role: 'Admin'    },
	];

	// ── Reactive state (Svelte 5 runes) ──────────────────────────────────────

	let filter = $state('');

	const filteredProducts = $derived(
		products.filter((p) =>
			p.name.toLowerCase().includes(filter.toLowerCase())
		)
	);

	const inventoryTotal = $derived(
		filteredProducts.reduce((sum, p) => sum + p.price * p.quantity, 0)
	);
</script>

<main>
	<h1>Generic Data Table — Svelte 5 Snippets Demo</h1>

	<!-- ── Products Table ─────────────────────────────────────────────────── -->

	<section>
		<h2>Products</h2>

		<div class="controls">
			<label for="product-filter">Filter by name:</label>
			<input
				id="product-filter"
				type="text"
				placeholder="e.g. keyboard"
				bind:value={filter}
			/>
		</div>

		<Table data={filteredProducts}>
			{#snippet header()}
				<th>Name</th>
				<th>Unit Price</th>
				<th>Quantity</th>
				<th>Line Total</th>
			{/snippet}

			{#snippet row(item)}
				{@const p = item as { name: string; price: number; quantity: number }}
				<td>{p.name}</td>
				<td>${p.price.toFixed(2)}</td>
				<td>{p.quantity}</td>
				<td>${(p.price * p.quantity).toFixed(2)}</td>
			{/snippet}
		</Table>

		<p class="summary">
			Total inventory value:
			<strong class="total">${inventoryTotal.toFixed(2)}</strong>
		</p>
	</section>

	<!-- ── Users Table ────────────────────────────────────────────────────── -->

	<section>
		<h2>Users</h2>

		<Table data={users}>
			{#snippet header()}
				<th>Name</th>
				<th>Email</th>
				<th>Role</th>
			{/snippet}

			{#snippet row(item)}
				{@const u = item as { name: string; email: string; role: string }}
				<td>{u.name}</td>
				<td>{u.email}</td>
				<td><span class="badge">{u.role}</span></td>
			{/snippet}
		</Table>
	</section>
</main>

<style>
	:global(*, *::before, *::after) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}

	:global(body) {
		background: #f8fafc;
		color: #0f172a;
	}

	main {
		max-width: 860px;
		margin: 2.5rem auto;
		padding: 0 1.25rem;
		font-family: system-ui, sans-serif;
	}

	h1 {
		font-size: 1.6rem;
		font-weight: 700;
		margin-bottom: 2rem;
		color: #0f172a;
	}

	section {
		background: #ffffff;
		border-radius: 0.75rem;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
		padding: 1.5rem;
		margin-bottom: 2rem;
		overflow: hidden;
	}

	h2 {
		font-size: 1.15rem;
		font-weight: 600;
		margin-bottom: 1rem;
		color: #1e293b;
	}

	.controls {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	label {
		font-size: 0.9rem;
		color: #475569;
		white-space: nowrap;
	}

	input[type='text'] {
		flex: 1;
		max-width: 280px;
		padding: 0.4rem 0.75rem;
		border: 1px solid #cbd5e1;
		border-radius: 0.375rem;
		font-size: 0.9rem;
		outline: none;
		transition: border-color 0.15s;
	}

	input[type='text']:focus {
		border-color: #6366f1;
		box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
	}

	.summary {
		margin-top: 1rem;
		font-size: 0.95rem;
		color: #475569;
	}

	.total {
		color: #16a34a;
		font-size: 1.05rem;
	}

	.badge {
		display: inline-block;
		padding: 0.15rem 0.55rem;
		border-radius: 9999px;
		font-size: 0.8rem;
		font-weight: 600;
		background: #e0e7ff;
		color: #3730a3;
	}
</style>
