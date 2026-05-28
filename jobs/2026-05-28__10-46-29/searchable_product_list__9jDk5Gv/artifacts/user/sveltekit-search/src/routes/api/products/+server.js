import { json } from '@sveltejs/kit';
import { products } from '$lib/server/data.js';

export function GET() {
	return json(products);
}
