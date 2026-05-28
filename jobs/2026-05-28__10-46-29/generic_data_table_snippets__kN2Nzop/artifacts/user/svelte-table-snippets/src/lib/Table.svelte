<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		data: unknown[];
		header: Snippet;
		row: Snippet<[unknown]>;
	}

	const { data, header, row }: Props = $props();
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

<style>
	table {
		width: 100%;
		border-collapse: collapse;
		font-family: sans-serif;
		font-size: 0.95rem;
	}

	:global(thead th) {
		background-color: #1e293b;
		color: #f8fafc;
		padding: 0.6rem 1rem;
		text-align: left;
		letter-spacing: 0.04em;
		font-weight: 600;
	}

	:global(tbody td) {
		padding: 0.55rem 1rem;
		border-bottom: 1px solid #e2e8f0;
		color: #334155;
	}

	:global(tbody tr:last-child td) {
		border-bottom: none;
	}

	:global(tbody tr:hover) {
		background-color: #f1f5f9;
	}
</style>
