<script>
	import { enhance } from '$app/forms';
	let { data, form } = $props();
</script>

<h1>Review Your Information</h1>

<dl>
	<dt>Email:</dt>
	<dd>{data.email}</dd>
	
	<dt>First Name:</dt>
	<dd>{data.firstName}</dd>
	
	<dt>Last Name:</dt>
	<dd>{data.lastName}</dd>
</dl>

<form method="POST" use:enhance>
	{#if form?.message}
		<p style="color: red;">{form.message}</p>
	{/if}
	<button type="submit">Submit</button>
</form>

<p><a href="/signup/step-1">Edit Step 1</a> | <a href="/signup/step-2">Edit Step 2</a> | <a href="/signup/step-3">Edit Step 3</a></p>
