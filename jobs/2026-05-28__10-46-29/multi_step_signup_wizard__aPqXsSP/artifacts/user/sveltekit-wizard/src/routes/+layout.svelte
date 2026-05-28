<script>
  let { children } = $props();
</script>

<svelte:head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sign Up Wizard</title>
</svelte:head>

<main>
  {@render children()}
</main>

<style>
  :global(body) {
    font-family: system-ui, sans-serif;
    margin: 0;
    padding: 0;
    background: #f5f5f5;
  }

  main {
    max-width: 480px;
    margin: 3rem auto;
    background: #fff;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  :global(h1) {
    margin-top: 0;
    font-size: 1.5rem;
  }

  :global(.field) {
    margin-bottom: 1rem;
  }

  :global(label) {
    display: block;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  :global(input[type="text"]),
  :global(input[type="email"]),
  :global(input[type="password"]) {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
  }

  :global(.error) {
    color: #c00;
    font-size: 0.875rem;
    margin-top: 0.25rem;
  }

  :global(button[type="submit"]) {
    padding: 0.6rem 1.5rem;
    background: #0070f3;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
  }

  :global(button[type="submit"]:hover) {
    background: #005bb5;
  }

  :global(.step-info) {
    color: #666;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
  }
</style>
