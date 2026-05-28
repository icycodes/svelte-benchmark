<script>
	const { post } = $props();

	let likes = $derived(post.likes);

	const handleLike = async () => {
		const previousLikes = likes;
		likes += 1;

		try {
			const response = await fetch(`/api/posts/${post.id}/like`, {
				method: 'POST'
			});

			if (!response.ok) {
				throw new Error('Failed to like.');
			}

			const data = await response.json();
			likes = data.likes;
		} catch (error) {
			likes = previousLikes;
		}
	};
</script>

<div data-testid={`post-${post.id}`}>
	<h2 data-testid={`title-${post.id}`}>{post.title}</h2>
	<p data-testid={`likes-${post.id}`}>{likes}</p>
	<button type="button" data-testid={`like-${post.id}`} on:click={handleLike}>
		Like
	</button>
</div>
