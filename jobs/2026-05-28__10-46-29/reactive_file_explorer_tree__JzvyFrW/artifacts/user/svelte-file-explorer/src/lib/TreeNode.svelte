<script>
	import TreeNode from '$lib/TreeNode.svelte';

	const { node, depth = 0 } = $props();

	const isFolder = node.type === 'folder';

	const toggle = () => {
		if (isFolder) {
			node.open = !node.open;
		}
	};
</script>

{#if isFolder}
	<div
		class="row folder"
		style={`padding-left: ${depth * 16}px`}
		data-testid="folder"
		data-folder-name={node.name}
		data-open={node.open ? 'true' : 'false'}
		role="button"
		tabindex="0"
		on:click={toggle}
		on:keydown={(event) => event.key === 'Enter' && toggle()}
	>
		<span class="indicator" aria-hidden="true">{node.open ? '▼' : '▶'}</span>
		<span class="label">{node.name}</span>
	</div>
	{#if node.open}
		<div class="children">
			{#each node.children as child (child.name)}
				<TreeNode node={child} depth={depth + 1} />
			{/each}
		</div>
	{/if}
{:else}
	<div
		class="row file"
		style={`padding-left: ${depth * 16}px`}
		data-testid="file"
		data-file-name={node.name}
	>
		<span class="spacer" aria-hidden="true">•</span>
		<span class="label">{node.name}</span>
	</div>
{/if}

<style>
	.row {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 4px 8px;
		font-family: system-ui, sans-serif;
		font-size: 14px;
	}

	.folder {
		cursor: pointer;
		user-select: none;
	}

	.folder:focus-visible {
		outline: 2px solid #3b82f6;
		outline-offset: 2px;
	}

	.indicator {
		width: 14px;
		text-align: center;
	}

	.spacer {
		width: 14px;
		text-align: center;
		opacity: 0.5;
	}

	.children {
		margin-left: 4px;
	}
</style>
