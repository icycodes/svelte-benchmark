<script>
  import { enhance } from '$app/forms';

  const { data, form } = $props();
  const values = $derived(() => data?.values ?? {});
  const error = $derived(() => form?.error ?? '');
</script>

<h1>Review your details</h1>

<dl>
  <dt>Email</dt>
  <dd>{values.email}</dd>

  <dt>First name</dt>
  <dd>{values.firstName}</dd>

  <dt>Last name</dt>
  <dd>{values.lastName}</dd>

  <dt>Password</dt>
  <dd>(hidden)</dd>
</dl>

<form method="POST" use:enhance>
  {#if error}
    <p class="error">{error}</p>
  {/if}
  <button type="submit">Submit signup</button>
</form>
