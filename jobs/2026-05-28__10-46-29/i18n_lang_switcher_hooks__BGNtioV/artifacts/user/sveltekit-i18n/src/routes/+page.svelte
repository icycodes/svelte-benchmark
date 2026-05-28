<script>
  import { enhance } from '$app/forms';
  import { greetings, LOCALES } from '$lib/i18n';

  /** @type {{ data: import('./$types').PageData }} */
  let { data } = $props();

  let locale = $derived(data.locale);
  let greeting = $derived(greetings[locale]);
</script>

<main>
  <h1>{greeting}</h1>

  <p>Current locale: <span data-testid="current-locale">{locale}</span></p>

  <form method="POST" use:enhance>
    {#each LOCALES as code}
      <button
        type="submit"
        name="locale"
        value={code}
        data-testid="locale-btn-{code}"
        aria-current={locale === code ? 'true' : undefined}
      >
        {code.toUpperCase()}
      </button>
    {/each}
  </form>
</main>

<style>
  main {
    font-family: sans-serif;
    max-width: 480px;
    margin: 4rem auto;
    text-align: center;
  }

  form {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    margin-top: 1.5rem;
  }

  button {
    padding: 0.5rem 1.25rem;
    font-size: 1rem;
    cursor: pointer;
    border: 2px solid #555;
    border-radius: 4px;
    background: #fff;
  }

  button[aria-current='true'] {
    background: #333;
    color: #fff;
    border-color: #333;
  }
</style>
