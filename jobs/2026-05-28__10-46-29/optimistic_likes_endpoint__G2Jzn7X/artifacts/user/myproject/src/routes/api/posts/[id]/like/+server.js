import { json, error } from '@sveltejs/kit';
import { posts } from '$lib/server/db.js';

export async function POST({ params }) {
  const { id } = params;
  
  // Artificial delay of 250ms
  await new Promise(resolve => setTimeout(resolve, 250));

  if (id === 'broken') {
    throw error(500, 'Broken post');
  }

  const post = posts.get(id);
  if (!post) {
    throw error(404, 'Post not found');
  }

  post.likes += 1;
  posts.set(id, post);

  return json({ id: post.id, likes: post.likes });
}
