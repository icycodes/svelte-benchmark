import { json, error } from '@sveltejs/kit';
import { posts } from '$lib/server/db';

export async function POST({ params }) {
  const { id } = params;

  // Artificial delay
  await new Promise((resolve) => setTimeout(resolve, 250));

  if (id === 'broken') {
    error(500, 'Internal Server Error');
  }

  const post = posts.get(id);
  if (!post) {
    error(404, 'Not Found');
  }

  post.likes += 1;
  posts.set(id, post);

  return json({ id: post.id, likes: post.likes });
}
