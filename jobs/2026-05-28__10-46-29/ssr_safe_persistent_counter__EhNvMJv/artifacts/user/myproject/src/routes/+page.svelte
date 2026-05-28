<script lang="ts">
  const STORAGE_KEY = 'persistent_counter_value';

  let count = $state(0);
  let hydrationStatus = $state('loading');

  $effect(() => {
    // This block only runs in the browser, never on the server.
    // Read the persisted value from localStorage on first run.
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored !== null) {
      const parsed = parseInt(stored, 10);
      if (!isNaN(parsed)) {
        count = parsed;
      }
    }

    // Mark hydration as complete.
    hydrationStatus = 'ready';
  });

  $effect(() => {
    // Write back to localStorage whenever count changes.
    // Runs after the first effect has set the hydrated value,
    // and on every subsequent change keeps localStorage in sync.
    localStorage.setItem(STORAGE_KEY, String(count));
  });

  function increment() {
    count += 1;
  }

  function reset() {
    count = 0;
  }
</script>

<main>
  <h1>Persistent Counter</h1>

  <p data-testid="count">{count}</p>

  <div class="buttons">
    <button data-testid="increment" onclick={increment}>Increment</button>
    <button data-testid="reset" onclick={reset}>Reset</button>
  </div>

  <p data-testid="hydration-status">{hydrationStatus}</p>
</main>

<style>
  main {
    font-family: sans-serif;
    max-width: 400px;
    margin: 4rem auto;
    text-align: center;
  }

  [data-testid="count"] {
    font-size: 3rem;
    font-weight: bold;
    margin: 1rem 0;
  }

  .buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 1rem 0;
  }

  button {
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    border: 2px solid #333;
    border-radius: 4px;
    background: white;
  }

  button:hover {
    background: #f0f0f0;
  }

  [data-testid="hydration-status"] {
    color: #888;
    font-size: 0.875rem;
  }
</style>
