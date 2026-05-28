<script lang="ts">
	let {
		value = $bindable(0),
		max = 5
	}: {
		value?: number;
		max?: number;
	} = $props();
</script>

<div class="star-rating" role="group" aria-label="Star rating">
	{#each { length: max } as _, i}
		{@const position = i + 1}
		{@const filled = position <= value}
		<button
			type="button"
			class="star"
			class:filled
			data-filled={filled ? 'true' : 'false'}
			aria-label="Rate {position} out of {max}"
			aria-pressed={position === value}
			onclick={() => (value = position)}
		>
			{filled ? '★' : '☆'}
		</button>
	{/each}
</div>

<style>
	.star-rating {
		display: inline-flex;
		gap: 0.25rem;
	}

	.star {
		background: none;
		border: none;
		cursor: pointer;
		font-size: 2rem;
		line-height: 1;
		padding: 0.25rem;
		color: #ccc;
		transition: color 0.15s ease;
	}

	.star.filled {
		color: #f5a623;
	}

	.star:hover {
		color: #f5a623;
	}

	.star:focus-visible {
		outline: 2px solid #f5a623;
		outline-offset: 2px;
		border-radius: 4px;
	}
</style>
