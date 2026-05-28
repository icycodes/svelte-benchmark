export async function load({ url, fetch }) {
	const q = url.searchParams.get('q') || '';
	const response = await fetch('/api/products');
	let products = await response.json();

	if (q) {
		const lowerQ = q.toLowerCase();
		products = products.filter(p => p.name.toLowerCase().includes(lowerQ));
	}

	return { q, products };
}
