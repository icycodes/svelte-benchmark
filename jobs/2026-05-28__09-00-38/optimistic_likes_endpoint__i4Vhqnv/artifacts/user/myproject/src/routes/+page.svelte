<script>
  import Post from './Post.svelte';
  let { data } = $props();
</script>

<h1>Posts</h1>
<div>
  {#each data.posts as post (post.id)}
    <Post {post} />
  {/each}
</div>
