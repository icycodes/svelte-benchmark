/** @type {import('./$types').PageLoad} */
export async function load({ url, fetch }) {
    const q = url.searchParams.get('q') || '';
    const res = await fetch('/api/products');
    const allProducts = await res.json();

    const filteredProducts = q 
        ? allProducts.filter(p => p.name.toLowerCase().includes(q.toLowerCase()))
        : allProducts;

    return {
        q,
        products: filteredProducts
    };
}
