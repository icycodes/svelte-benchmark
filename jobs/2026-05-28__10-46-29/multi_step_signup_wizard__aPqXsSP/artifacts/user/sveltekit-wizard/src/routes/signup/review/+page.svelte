<script>
  import { enhance } from '$app/forms';

  let { data, form } = $props();

  let submitting = $state(false);
</script>

<h1>Review your details</h1>
<p class="step-info">Almost done! Please confirm your information.</p>

<dl class="summary">
  <dt>Email</dt>
  <dd>{data.email}</dd>

  <dt>First name</dt>
  <dd>{data.firstName}</dd>

  <dt>Last name</dt>
  <dd>{data.lastName}</dd>

  <dt>Password</dt>
  <dd>••••••••</dd>
</dl>

{#if form?.message}
  <p class="error">{form.message}</p>
{/if}

<form
  method="POST"
  use:enhance={() => {
    submitting = true;
    return async ({ update }) => {
      await update();
      submitting = false;
    };
  }}
>
  <button type="submit" disabled={submitting}>
    {submitting ? 'Submitting…' : 'Submit →'}
  </button>
</form>

<style>
  .summary {
    background: #f9f9f9;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
  }

  dt {
    font-weight: 600;
    color: #555;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 0.75rem;
  }

  dt:first-child {
    margin-top: 0;
  }

  dd {
    margin: 0.1rem 0 0;
    font-size: 1rem;
  }
</style>
