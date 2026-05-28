import { posts } from '$lib/server/db.js';

export function load() {
  return {
    posts: Array.from(posts.values())
  };
}
