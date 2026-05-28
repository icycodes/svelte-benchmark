<script>
  let { post } = $props();
  
  // Overridable derived value (Svelte 5.25+)
  let likes = $derived(post.likes);

  async function likePost() {
    // 1. Update the displayed count immediately (optimistic)
    likes += 1;

    try {
      // 2. Send POST /api/posts/[id]/like to the server
      const response = await fetch(`/api/posts/${post.id}/like`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error('Failed to like post');
      }

      const result = await response.json();
      // 3. On success, keep the new count (the server's authoritative value)
      // Since 'post' is a prop from the parent, if we wanted to be truly authoritative 
      // we might need the parent to update the data, but the prompt says 
      // "reconciled with the value returned by the server".
      // If we assign the server value back to the overridable derived, it works.
      likes = result.likes;
    } catch (err) {
      // 4. On failure, revert the displayed count to its previous value
      likes -= 1;
    }
  }
</script>

<div data-testid="post-{post.id}">
  <h2 data-testid="title-{post.id}">{post.title}</h2>
  <p data-testid="likes-{post.id}">{likes}</p>
  <button data-testid="like-{post.id}" onclick={likePost}>
    Like
  </button>
</div>
