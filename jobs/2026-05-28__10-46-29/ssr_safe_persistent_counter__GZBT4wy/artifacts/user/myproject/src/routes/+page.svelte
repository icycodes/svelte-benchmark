<script lang="ts">
	let count = $state(0);
	let status = $state("loading");

	$effect(() => {
		const stored = localStorage.getItem("persistent_counter_value");
		if (stored !== null) {
			count = JSON.parse(stored);
		}
		status = "ready";
	});

	$effect(() => {
		if (status === "ready") {
			localStorage.setItem("persistent_counter_value", JSON.stringify(count));
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
<div data-testid="count">{count}</div>
<button data-testid="increment" onclick={increment}>Increment</button>
<button data-testid="reset" onclick={reset}>Reset</button>
<div data-testid="hydration-status">{status}</div>
