<script>
  import { enhance } from '$app/forms';

  const { form } = $props();
  const error = $derived(() => form?.error ?? '');
</script>

<h1>Step 2: Choose a Password</h1>

<form method="POST" use:enhance>
  <label for="password">Password</label>
  <input id="password" name="password" type="password" required minlength="8" />

  <label for="confirmPassword">Confirm password</label>
  <input id="confirmPassword" name="confirmPassword" type="password" required minlength="8" />

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <button type="submit">Continue</button>
</form>
