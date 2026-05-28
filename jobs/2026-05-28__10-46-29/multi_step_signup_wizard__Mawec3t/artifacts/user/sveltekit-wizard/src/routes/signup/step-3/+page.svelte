<script>
  import { enhance } from '$app/forms';

  const { data, form } = $props();
  const values = $derived(() => form?.values ?? data?.values ?? {});
  const error = $derived(() => form?.error ?? '');
</script>

<h1>Step 3: Your Name</h1>

<form method="POST" use:enhance>
  <label for="firstName">First name</label>
  <input id="firstName" name="firstName" value={values.firstName ?? ''} required />

  <label for="lastName">Last name</label>
  <input id="lastName" name="lastName" value={values.lastName ?? ''} required />

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <button type="submit">Continue</button>
</form>
