<script>
  import Post from '$lib/Post.svelte';
  let { data } = $props();
</script>

<h1>Posts</h1>
{#each data.posts as post}
  <Post {post} />
{/each}
