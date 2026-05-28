<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// Each post entry tracks its own optimistic likes count.
	// We use an overridable $derived (Svelte 5.25+): the value is derived from
	// the server data prop, but we can reassign it locally for optimistic updates.
	// When `data` changes (e.g. after a full page reload / navigation), the derived
	// expression re-runs and the displayed count is reconciled automatically.
	class PostState {
		serverLikes: number;
		likes = $derived(this.serverLikes);

		constructor(initialLikes: number) {
			this.serverLikes = initialLikes;
		}
	}

	// Build a reactive record from the server-loaded posts so Svelte
	// can track individual property accesses reactively.
	let postStates = $state(
		Object.fromEntries(data.posts.map((p) => [p.id, new PostState(p.likes)]))
	);

	async function handleLike(id: string) {
		const state = postStates[id];
		if (!state) return;

		// --- Optimistic update (immediate, before awaiting the network) ---
		state.likes += 1;

		try {
			const res = await fetch(`/api/posts/${id}/like`, { method: 'POST' });

			if (!res.ok) {
				// Server rejected the request — roll back
				state.likes -= 1;
				return;
			}

			const body: { id: string; likes: number } = await res.json();
			// Reconcile with the authoritative server value
			state.likes = body.likes;
		} catch {
			// Network error — roll back
			state.likes -= 1;
		}
	}
</script>

<main>
	<h1>Posts</h1>

	<ul>
		{#each data.posts as post (post.id)}
			{@const state = postStates[post.id]}
			<li data-testid="post-{post.id}">
				<span data-testid="title-{post.id}">{post.title}</span>
				<span data-testid="likes-{post.id}">{state.likes}</span>
				<button data-testid="like-{post.id}" onclick={() => handleLike(post.id)}>
					Like
				</button>
			</li>
		{/each}
	</ul>
</main>

<style>
	main {
		font-family: sans-serif;
		max-width: 600px;
		margin: 2rem auto;
		padding: 0 1rem;
	}

	h1 {
		margin-bottom: 1.5rem;
	}

	ul {
		list-style: none;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	li {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		border: 1px solid #ddd;
		border-radius: 8px;
	}

	span[data-testid^='title'] {
		flex: 1;
		font-weight: 600;
	}

	span[data-testid^='likes'] {
		min-width: 2rem;
		text-align: center;
		font-size: 1.1rem;
		font-weight: 700;
	}

	button {
		padding: 0.4rem 1rem;
		border: none;
		border-radius: 6px;
		background: #e05252;
		color: white;
		cursor: pointer;
		font-size: 0.9rem;
	}

	button:hover {
		background: #c43a3a;
	}
</style>
