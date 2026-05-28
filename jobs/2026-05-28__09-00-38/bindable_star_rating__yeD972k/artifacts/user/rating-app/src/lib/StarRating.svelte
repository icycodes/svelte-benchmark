<script lang="ts">
	let { value = $bindable(0), max = 5 }: { value?: number; max?: number } = $props();

	function setRating(n: number) {
		value = n;
	}
</script>

<div class="star-rating">
	{#each Array.from({ length: max }, (_, i) => i + 1) as n}
		<button
			type="button"
			class="star"
			class:filled={n <= value}
			data-filled={n <= value ? "true" : "false"}
			onclick={() => setRating(n)}
			aria-label="Rate {n} out of {max}"
		>
			★
		</button>
	{/each}
</div>

<style>
	.star {
		font-size: 2rem;
		cursor: pointer;
		background: none;
		border: none;
		color: #ccc;
		padding: 0;
	}

	.star.filled {
		color: gold;
	}
</style>
