<script>
  import { enhance } from '$app/forms';

  let { form } = $props();

  let passwordError = $derived(form?.field === 'password' ? form.message : '');
  let confirmError = $derived(form?.field === 'confirmPassword' ? form.message : '');
</script>

<h1>Create your account</h1>
<p class="step-info">Step 2 of 3 — Choose a password</p>

<form method="POST" use:enhance>
  <div class="field">
    <label for="password">Password</label>
    <input
      type="password"
      id="password"
      name="password"
      autocomplete="new-password"
      required
    />
    {#if passwordError}
      <p class="error">{passwordError}</p>
    {/if}
  </div>

  <div class="field">
    <label for="confirmPassword">Confirm password</label>
    <input
      type="password"
      id="confirmPassword"
      name="confirmPassword"
      autocomplete="new-password"
      required
    />
    {#if confirmError}
      <p class="error">{confirmError}</p>
    {/if}
  </div>

  <button type="submit">Continue →</button>
</form>
