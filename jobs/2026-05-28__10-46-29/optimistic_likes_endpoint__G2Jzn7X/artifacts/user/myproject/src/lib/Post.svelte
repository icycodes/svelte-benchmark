<script>
  let { post } = $props();
  let likes = $derived(post.likes);

  async function like() {
    likes += 1;
    try {
      const res = await fetch(`/api/posts/${post.id}/like`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed');
      const data = await res.json();
      likes = data.likes; // Keep authoritative value
    } catch (err) {
      likes -= 1; // Rollback
    }
  }
</script>

<div data-testid="post-{post.id}">
  <h2 data-testid="title-{post.id}">{post.title}</h2>
  <p data-testid="likes-{post.id}">{likes}</p>
  <button data-testid="like-{post.id}" onclick={like}>Like</button>
</div>
