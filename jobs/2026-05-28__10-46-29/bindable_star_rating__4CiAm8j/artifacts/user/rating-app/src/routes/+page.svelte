<script lang="ts">
	import StarRating from '$lib/StarRating.svelte';

	let rating = $state(0);
</script>

<main>
	<h1>Product Rating</h1>

	<h2>Rating: {rating}</h2>

	<StarRating bind:value={rating} />

	<div class="controls">
		<button type="button" onclick={() => (rating = 0)}>Reset</button>
	</div>
</main>

<style>
	main {
		font-family: system-ui, sans-serif;
		max-width: 480px;
		margin: 4rem auto;
		padding: 2rem;
		text-align: center;
	}

	h1 {
		font-size: 2rem;
		margin-bottom: 0.5rem;
	}

	h2 {
		font-size: 1.25rem;
		color: #555;
		margin-bottom: 1.5rem;
	}

	.controls {
		margin-top: 1.5rem;
	}

	button {
		padding: 0.5rem 1.5rem;
		font-size: 1rem;
		cursor: pointer;
		border: 1px solid #999;
		border-radius: 4px;
		background: #f0f0f0;
	}

	button:hover {
		background: #e0e0e0;
	}
</style>
