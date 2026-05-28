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
		{@render header()}
	</thead>
	<tbody>
		{#each data as item}
			<tr>
				{@render row(item)}
			</tr>
		{/each}
	</tbody>
</table>

<style>
	table {
		width: 100%;
		border-collapse: collapse;
		margin-bottom: 2rem;
	}
	:global(th), :global(td) {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: left;
	}
	:global(th) {
		background-color: #f2f2f2;
	}
</style>
