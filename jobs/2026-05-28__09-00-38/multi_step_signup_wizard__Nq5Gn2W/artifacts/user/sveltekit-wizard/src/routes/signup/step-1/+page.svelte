<script>
	import { enhance } from '$app/forms';
	let { data, form } = $props();
</script>

<h1>Step 1: Email</h1>

<form method="POST" use:enhance>
	<div>
		<label for="email">Email:</label>
		<input type="email" id="email" name="email" value={form?.email ?? data.email} required />
	</div>
	{#if form?.message}
		<p style="color: red;">{form.message}</p>
	{/if}
	<button type="submit">Next</button>
</form>
