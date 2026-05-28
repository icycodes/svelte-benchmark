import { error, json } from '@sveltejs/kit';
import { incrementLike } from '$lib/server/posts';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export async function POST({ params }) {
	await delay(250);

	if (params.id === 'broken') {
		throw error(500, 'Broken post failed to like.');
	}

	const likes = incrementLike(params.id);

	if (likes === null) {
		throw error(404, 'Post not found.');
	}

	return json({ id: params.id, likes });
}
