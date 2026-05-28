<script>
	let { value = $bindable(0), max = 5 } = $props();
</script>

<div class="star-rating">
	{#each Array(max) as _, i}
		<button
			class="star"
			class:filled={i < value}
			data-filled={i < value ? 'true' : 'false'}
			onclick={() => (value = i + 1)}
		>
			★
		</button>
	{/each}
</div>

<style>
	.star {
		background: none;
		border: none;
		font-size: 2rem;
		cursor: pointer;
		color: #ccc;
	}
	.star.filled {
		color: gold;
	}
</style>
