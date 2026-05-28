<script>
	import { enhance } from '$app/forms';
	let { form } = $props();
</script>

<h1>Step 2: Password</h1>

<form method="POST" use:enhance>
	<div>
		<label for="password">Password:</label>
		<input type="password" id="password" name="password" required />
	</div>
	<div>
		<label for="confirmPassword">Confirm Password:</label>
		<input type="password" id="confirmPassword" name="confirmPassword" required />
	</div>
	{#if form?.message}
		<p style="color: red;">{form.message}</p>
	{/if}
	<button type="submit">Next</button>
</form>
