<script>
  let { data } = $props();

  let displayEmail = $derived(data.email || 'your email address');
</script>

<div class="success">
  <div class="icon">✓</div>
  <h1>Account created!</h1>
  <p>
    Welcome aboard! We've registered your account for
    <strong>{displayEmail}</strong>.
  </p>
  <a href="/signup/step-1">Start over</a>
</div>

<style>
  .success {
    text-align: center;
  }

  .icon {
    font-size: 3rem;
    color: #22c55e;
    margin-bottom: 0.5rem;
    line-height: 1;
  }

  h1 {
    margin-bottom: 0.5rem;
  }

  p {
    color: #444;
  }

  a {
    display: inline-block;
    margin-top: 1rem;
    color: #0070f3;
    text-decoration: none;
    font-size: 0.9rem;
  }

  a:hover {
    text-decoration: underline;
  }
</style>
