<script>
	import { enhance } from '$app/forms';
	let { data, form } = $props();
</script>

<h1>Step 3: Personal Information</h1>

<form method="POST" use:enhance>
	<div>
		<label for="firstName">First Name:</label>
		<input type="text" id="firstName" name="firstName" value={form?.firstName ?? data.firstName} required />
	</div>
	<div>
		<label for="lastName">Last Name:</label>
		<input type="text" id="lastName" name="lastName" value={form?.lastName ?? data.lastName} required />
	</div>
	{#if form?.message}
		<p style="color: red;">{form.message}</p>
	{/if}
	<button type="submit">Review</button>
</form>
