<script>
	let count = $state(0);
	let hydrationStatus = $state('loading');
	let initialized = false;

	$effect(() => {
		if (!initialized) {
			initialized = true;
			const storedValue = localStorage.getItem('persistent_counter_value');
			if (storedValue !== null) {
				const parsed = JSON.parse(storedValue);
				if (typeof parsed === 'number' && !Number.isNaN(parsed)) {
					count = parsed;
				}
			}
			hydrationStatus = 'ready';
		}

		localStorage.setItem('persistent_counter_value', JSON.stringify(count));
	});
</script>

<main>
	<h1>Persistent Counter</h1>
	<p data-testid="hydration-status">{hydrationStatus}</p>
	<p data-testid="count">{count}</p>
	<div>
		<button data-testid="increment" type="button" on:click={() => count += 1}>
			Increment
		</button>
		<button data-testid="reset" type="button" on:click={() => count = 0}>
			Reset
		</button>
	</div>
</main>
