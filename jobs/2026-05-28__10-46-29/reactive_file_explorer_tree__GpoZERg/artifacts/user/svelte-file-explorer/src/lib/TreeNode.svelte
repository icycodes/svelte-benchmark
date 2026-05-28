<script lang="ts">
	import TreeNode from './TreeNode.svelte';

	let { node } = $props();

	function toggle(e: Event) {
		if (node.type === 'folder') {
			node.open = !node.open;
            e.stopPropagation();
		}
	}
</script>

{#if node.type === 'folder'}
	<div 
        data-testid="folder" 
        data-folder-name={node.name} 
        data-open={String(!!node.open)} 
        onclick={toggle}
        style="cursor: pointer;"
    >
		{node.open ? '▼' : '▶'} {node.name}
	</div>
	{#if node.open && node.children}
		<div style="padding-left: 20px;">
			{#each node.children as child}
				<TreeNode node={child} />
			{/each}
		</div>
	{/if}
{:else}
	<div data-testid="file" data-file-name={node.name}>
		{node.name}
	</div>
{/if}
