<script lang="ts">
	import { enhance } from '$app/forms';

	let { data, form } = $props();
</script>

<h1>Step 1: Email</h1>

<form method="POST" use:enhance>
	<label>
		Email:
		<input type="email" name="email" value={form?.email ?? data.email} required />
	</label>
	
	{#if form?.error}
		<p style="color: red;">{form.error}</p>
	{/if}

	<button type="submit">Next</button>
</form>
