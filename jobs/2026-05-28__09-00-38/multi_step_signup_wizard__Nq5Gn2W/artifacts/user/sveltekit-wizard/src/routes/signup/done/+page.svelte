<script>
	import { page } from '$app/state';
	const email = $derived(page.url.searchParams.get('email'));
</script>

<h1>Signup Complete!</h1>

<p>Thank you for signing up, <strong>{email}</strong>.</p>
<p>Your account has been successfully created.</p>
<a href="/signup/step-1">Start over</a>
