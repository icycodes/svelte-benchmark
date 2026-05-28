import { json, error } from '@sveltejs/kit';
import { posts } from '$lib/server/posts';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ params }) => {
	const { id } = params;

	// Artificial delay so the optimistic update is observable in the browser
	await new Promise((resolve) => setTimeout(resolve, 300));

	// The "broken" post always fails
	if (id === 'broken') {
		throw error(500, 'This post is broken and cannot be liked.');
	}

	const post = posts.get(id);

	if (!post) {
		throw error(404, `Post "${id}" not found.`);
	}

	post.likes += 1;

	return json({ id: post.id, likes: post.likes });
};
