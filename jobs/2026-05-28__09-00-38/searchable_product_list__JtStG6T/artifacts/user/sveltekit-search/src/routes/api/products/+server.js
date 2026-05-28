import { json } from '@sveltejs/kit';
import { products } from '$lib/server/products';

export function GET() {
    return json(products);
}
