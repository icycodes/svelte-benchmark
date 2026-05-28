const posts = new Map([
	['1', { id: '1', title: 'First Post', likes: 0 }],
	['2', { id: '2', title: 'Second Post', likes: 5 }],
	['3', { id: '3', title: 'Third Post', likes: 10 }],
	['broken', { id: 'broken', title: 'Broken Post', likes: 0 }]
]);

export function listPosts() {
	return Array.from(posts.values(), (post) => ({ ...post }));
}

export function incrementLike(id) {
	const post = posts.get(id);
	if (!post) {
		return null;
	}

	post.likes += 1;
	return post.likes;
}
