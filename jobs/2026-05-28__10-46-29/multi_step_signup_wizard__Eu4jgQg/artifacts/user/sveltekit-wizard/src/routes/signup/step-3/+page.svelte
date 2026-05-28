<script lang="ts">
	import { enhance } from '$app/forms';

	let { data, form } = $props();
</script>

<h1>Step 3: Name</h1>

<form method="POST" use:enhance>
	<label>
		First Name:
		<input type="text" name="firstName" value={form?.firstName ?? data.firstName} required />
	</label>
	
	<label>
		Last Name:
		<input type="text" name="lastName" value={form?.lastName ?? data.lastName} required />
	</label>
	
	{#if form?.error}
		<p style="color: red;">{form.error}</p>
	{/if}

	<button type="submit">Next</button>
</form>
