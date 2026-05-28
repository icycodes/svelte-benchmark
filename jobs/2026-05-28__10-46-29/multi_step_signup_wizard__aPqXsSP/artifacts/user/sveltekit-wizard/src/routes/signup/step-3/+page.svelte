<script>
  import { enhance } from '$app/forms';

  let { data, form } = $props();

  let firstNameValue = $derived(form?.firstNameValue ?? data.firstName ?? '');
  let lastNameValue = $derived(form?.lastNameValue ?? data.lastName ?? '');
</script>

<h1>Create your account</h1>
<p class="step-info">Step 3 of 3 — Your name</p>

<form method="POST" use:enhance>
  <div class="field">
    <label for="firstName">First name</label>
    <input
      type="text"
      id="firstName"
      name="firstName"
      value={firstNameValue}
      autocomplete="given-name"
      required
    />
    {#if form?.field === 'firstName'}
      <p class="error">{form.message}</p>
    {/if}
  </div>

  <div class="field">
    <label for="lastName">Last name</label>
    <input
      type="text"
      id="lastName"
      name="lastName"
      value={lastNameValue}
      autocomplete="family-name"
      required
    />
    {#if form?.field === 'lastName'}
      <p class="error">{form.message}</p>
    {/if}
  </div>

  <button type="submit">Review →</button>
</form>
