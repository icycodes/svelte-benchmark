import { listPosts } from '$lib/server/posts';

export function load() {
	return {
		posts: listPosts()
	};
}
