<script lang="ts">
	import { enhance } from '$app/forms';

	let { data, form } = $props();
</script>

<h1>Review</h1>

<ul>
	<li>Email: {data.email}</li>
	<li>First Name: {data.firstName}</li>
	<li>Last Name: {data.lastName}</li>
	<li>Password Length: {data.passwordLength}</li>
</ul>

<form method="POST" use:enhance>
	{#if form?.error}
		<p style="color: red;">{form.error}</p>
	{/if}

	<button type="submit">Submit</button>
</form>
