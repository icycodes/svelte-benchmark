<script lang="ts">
	let count = $state(0);
	let status = $state('loading');
	const STORAGE_KEY = 'persistent_counter_value';

	$effect(() => {
		// On mount, load from localStorage
		const stored = localStorage.getItem(STORAGE_KEY);
		if (stored !== null) {
			count = JSON.parse(stored);
		}
		status = 'ready';

		// Return a cleanup function if needed, but here we just want to sync back
		// Actually, we can use a separate effect for syncing or just do it in the same one
		// if we want it to react to 'count' changes.
	});

	$effect(() => {
		// This effect runs whenever 'count' changes (after the first run)
		// It's safe to use localStorage here because $effect only runs on the client.
		if (status === 'ready') {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(count));
		}
	});

	function increment() {
		count += 1;
	}

	function reset() {
		count = 0;
	}
</script>

<h1>Persistent Counter</h1>

<div>
	Count: <span data-testid="count">{count}</span>
</div>

<button data-testid="increment" onclick={increment}>Increment</button>
<button data-testid="reset" onclick={reset}>Reset</button>

<p>Status: <span data-testid="hydration-status">{status}</span></p>
