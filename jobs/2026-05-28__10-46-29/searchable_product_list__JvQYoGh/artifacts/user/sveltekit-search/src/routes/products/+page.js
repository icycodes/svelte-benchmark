export const load = async ({ url, fetch }) => {
    const q = url.searchParams.get('q') ?? '';
    const response = await fetch('/api/products');
    const products = await response.json();
    const normalizedQuery = q.toLowerCase();

    const filteredProducts = normalizedQuery
        ? products.filter((product) => product.name.toLowerCase().includes(normalizedQuery))
        : products;

    return {
        q,
        products: filteredProducts
    };
};
