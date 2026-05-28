/** @type {import('./$types').PageLoad} */
export async function load({ url, fetch }) {
  const q = url.searchParams.get('q') ?? '';

  const response = await fetch('/api/products');
  /** @type {Array<{id: number, name: string, price: number}>} */
  const allProducts = await response.json();

  const products = q
    ? allProducts.filter((p) => p.name.toLowerCase().includes(q.toLowerCase()))
    : allProducts;

  return { q, products };
}
