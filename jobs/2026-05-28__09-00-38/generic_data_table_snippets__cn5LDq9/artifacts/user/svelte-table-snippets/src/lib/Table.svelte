<script>
	/**
	 * @typedef {Object} Props
	 * @property {any[]} data
	 * @property {import('svelte').Snippet} header
	 * @property {import('svelte').Snippet<[any]>} row
	 */

	/** @type {Props} */
	let { data, header, row } = $props();
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
		border: 1px solid #ccc;
		padding: 0.5rem;
		text-align: left;
	}
	:global(th) {
		background-color: #f4f4f4;
	}
</style>
