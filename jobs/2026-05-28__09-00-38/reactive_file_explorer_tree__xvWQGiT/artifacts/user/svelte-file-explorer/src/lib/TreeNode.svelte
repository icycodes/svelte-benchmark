<script>
	import TreeNode from './TreeNode.svelte';
	let { node } = $props();

	function toggle() {
		if (node.type === 'folder') {
			node.isOpen = !node.isOpen;
		}
	}
</script>

{#if node.type === 'folder'}
	<div
		data-testid="folder"
		data-folder-name={node.name}
		data-open={node.isOpen ? "true" : "false"}
		onclick={toggle}
		style="cursor: pointer; user-select: none;"
	>
		<span>{node.isOpen ? '▼' : '▶'}</span>
		{node.name}
	</div>
	{#if node.isOpen}
		<div style="margin-left: 20px;">
			{#each node.children as child}
				<TreeNode node={child} />
			{/each}
		</div>
	{/if}
{:else}
	<div
		data-testid="file"
		data-file-name={node.name}
		style="margin-left: 20px;"
	>
		{node.name}
	</div>
{/if}
