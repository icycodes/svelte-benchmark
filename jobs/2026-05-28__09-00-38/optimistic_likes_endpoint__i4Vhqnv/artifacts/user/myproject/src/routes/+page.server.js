import { posts } from '$lib/server/db';

export function load() {
  return {
    posts: Array.from(posts.values())
  };
}
