import { json } from '@sveltejs/kit';
import { products } from '$lib/server/products';

export const GET = async () => {
    return json(products);
};
