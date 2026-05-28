<script>
	import PostItem from '$lib/components/PostItem.svelte';

	const { data } = $props();
</script>

<svelte:head>
	<title>Posts</title>
</svelte:head>

<main>
	<h1>Posts</h1>
	{#each data.posts as post (post.id)}
		<PostItem {post} />
	{/each}
</main>
