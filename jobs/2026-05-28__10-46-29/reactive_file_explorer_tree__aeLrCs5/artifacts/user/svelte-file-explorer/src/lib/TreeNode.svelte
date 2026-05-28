<script lang="ts">
	import type { TreeNodeData } from './tree.svelte.js';
	import TreeNode from './TreeNode.svelte';

	const { node, depth = 0 }: { node: TreeNodeData; depth?: number } = $props();

	function toggle() {
		if (node.kind === 'folder') {
			node.open = !node.open;
		}
	}
</script>

{#if node.kind === 'folder'}
	<!-- Folder row -->
	<div
		class="row folder-row"
		style="padding-left: {depth * 1.25}rem"
		role="button"
		tabindex="0"
		data-testid="folder"
		data-folder-name={node.name}
		data-open={node.open ? 'true' : 'false'}
		onclick={toggle}
		onkeydown={(e) => (e.key === 'Enter' || e.key === ' ') && toggle()}
	>
		<span class="indicator" aria-hidden="true">{node.open ? '▼' : '▶'}</span>
		<span class="icon" aria-hidden="true">📁</span>
		<span class="name">{node.name}</span>
	</div>

	<!-- Children — only mounted when folder is open -->
	{#if node.open}
		{#each node.children as child (child.name)}
			<TreeNode node={child} depth={depth + 1} />
		{/each}
	{/if}
{:else}
	<!-- File row -->
	<div
		class="row file-row"
		style="padding-left: {depth * 1.25}rem"
		data-testid="file"
		data-file-name={node.name}
	>
		<span class="icon" aria-hidden="true">📄</span>
		<span class="name">{node.name}</span>
	</div>
{/if}

<style>
	.row {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		padding-top: 0.2rem;
		padding-bottom: 0.2rem;
		padding-right: 0.5rem;
		font-size: 0.9rem;
		line-height: 1.4;
		border-radius: 4px;
		cursor: default;
		user-select: none;
	}

	.folder-row {
		cursor: pointer;
		font-weight: 500;
	}

	.folder-row:hover {
		background: rgba(99, 102, 241, 0.08);
	}

	.folder-row:focus-visible {
		outline: 2px solid #6366f1;
		outline-offset: -2px;
	}

	.indicator {
		width: 0.8rem;
		text-align: center;
		font-size: 0.65rem;
		color: #9ca3af;
		flex-shrink: 0;
	}

	.icon {
		font-size: 0.85rem;
		flex-shrink: 0;
	}

	.name {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.file-row {
		color: #4b5563;
	}
</style>
