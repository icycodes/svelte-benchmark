<script>
  import { enhance } from '$app/forms';

  let { data, form } = $props();

  // Use $derived so emailValue re-computes when props change
  let emailValue = $derived(form?.value ?? data.email ?? '');
</script>

<h1>Create your account</h1>
<p class="step-info">Step 1 of 3 — Enter your email</p>

<form method="POST" use:enhance>
  <div class="field">
    <label for="email">Email address</label>
    <input
      type="email"
      id="email"
      name="email"
      value={emailValue}
      autocomplete="email"
      required
    />
    {#if form?.field === 'email'}
      <p class="error">{form.message}</p>
    {/if}
  </div>

  <button type="submit">Continue →</button>
</form>
