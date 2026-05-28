<script>
  import StarRating from '$lib/StarRating.svelte';

  let rating = $state(0);
</script>

<h1>Rating: {rating}</h1>

<StarRating bind:value={rating} />

<button type="button" on:click={() => (rating = 0)}>
  Reset
</button>
