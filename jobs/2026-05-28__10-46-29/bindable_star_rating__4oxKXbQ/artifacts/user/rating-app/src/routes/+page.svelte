<script>
	import StarRating from '$lib/StarRating.svelte';

	let rating = $state(0);

	function resetRating() {
		rating = 0;
	}
</script>

<h1>Rating: {rating}</h1>

<StarRating bind:value={rating} />

<button onclick={resetRating}>Reset</button>
