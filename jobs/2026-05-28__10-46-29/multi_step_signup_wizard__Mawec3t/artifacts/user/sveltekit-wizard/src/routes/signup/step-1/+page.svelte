<script>
  import { enhance } from '$app/forms';

  const { data, form } = $props();
  const values = $derived(() => form?.values ?? data?.values ?? {});
  const error = $derived(() => form?.error ?? '');
</script>

<h1>Step 1: Account Email</h1>

<form method="POST" use:enhance>
  <label for="email">Email</label>
  <input
    id="email"
    name="email"
    type="email"
    value={values.email ?? ''}
    required
  />
  {#if error}
    <p class="error">{error}</p>
  {/if}
  <button type="submit">Continue</button>
</form>
