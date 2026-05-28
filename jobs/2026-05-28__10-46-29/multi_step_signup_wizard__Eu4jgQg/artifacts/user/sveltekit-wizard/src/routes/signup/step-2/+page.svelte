<script lang="ts">
	import { enhance } from '$app/forms';

	let { form } = $props();
</script>

<h1>Step 2: Password</h1>

<form method="POST" use:enhance>
	<label>
		Password:
		<input type="password" name="password" required />
	</label>
	
	<label>
		Confirm Password:
		<input type="password" name="confirmPassword" required />
	</label>
	
	{#if form?.error}
		<p style="color: red;">{form.error}</p>
	{/if}

	<button type="submit">Next</button>
</form>
