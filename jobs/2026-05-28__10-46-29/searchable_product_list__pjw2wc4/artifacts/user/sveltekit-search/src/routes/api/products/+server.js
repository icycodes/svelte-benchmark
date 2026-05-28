import { json } from '@sveltejs/kit';
import { products } from '$lib/server/products.js';

/** @type {import('./$types').RequestHandler} */
export function GET() {
  return json(products);
}
