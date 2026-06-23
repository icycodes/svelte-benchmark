<script lang="ts" generics="T">
	import type { Snippet } from 'svelte';

	let {
		data,
		header,
		row
	}: {
		data: T[];
		header: Snippet;
		row: Snippet<[T]>;
	} = $props();
</script>

<table>
	<thead>
		<tr>
			{@render header()}
		</tr>
	</thead>
	<tbody>
		{#each data as item}
			<tr>
				{@render row(item)}
			</tr>
		{/each}
	</tbody>
</table>
