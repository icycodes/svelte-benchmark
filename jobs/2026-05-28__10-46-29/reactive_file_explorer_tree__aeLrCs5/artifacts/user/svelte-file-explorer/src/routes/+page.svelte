<script lang="ts">
	import TreeNode from '$lib/TreeNode.svelte';
	import { tree, treeStats } from '$lib/tree.svelte.js';
</script>

<svelte:head>
	<title>Svelte 5 File Explorer</title>
</svelte:head>

<!-- ── Status bar ─────────────────────────────────────────────────────── -->
<header class="status-bar">
	<span class="status-item">
		<span class="status-label">Open folders</span>
		<span class="status-badge" data-testid="open-folder-count">{treeStats.openFolderCount}</span>
	</span>
	<span class="divider" aria-hidden="true">│</span>
	<span class="status-item">
		<span class="status-label">Visible files</span>
		<span class="status-badge" data-testid="visible-file-count">{treeStats.visibleFileCount}</span>
	</span>
</header>

<!-- ── File explorer ──────────────────────────────────────────────────── -->
<main class="explorer">
	<h1 class="explorer-title">📂 File Explorer</h1>
	<div class="tree">
		{#each tree as node (node.name)}
			<TreeNode {node} />
		{/each}
	</div>
</main>

<style>
	:global(*, *::before, *::after) {
		box-sizing: border-box;
	}

	:global(body) {
		margin: 0;
		font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
		background: #f8fafc;
		color: #1e293b;
	}

	/* ── Status bar ── */
	.status-bar {
		position: sticky;
		top: 0;
		z-index: 100;
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.6rem 1.5rem;
		background: #1e293b;
		color: #f1f5f9;
		font-size: 0.875rem;
		font-weight: 500;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
	}

	.status-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.status-label {
		color: #94a3b8;
	}

	.status-badge {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 1.5rem;
		padding: 0.05rem 0.45rem;
		background: #6366f1;
		color: #fff;
		border-radius: 999px;
		font-size: 0.8rem;
		font-variant-numeric: tabular-nums;
		font-weight: 700;
	}

	.divider {
		color: #475569;
	}

	/* ── Explorer panel ── */
	.explorer {
		max-width: 640px;
		margin: 2rem auto;
		padding: 0 1rem;
	}

	.explorer-title {
		font-size: 1.25rem;
		font-weight: 700;
		margin: 0 0 1rem 0;
		color: #1e293b;
	}

	.tree {
		background: #fff;
		border: 1px solid #e2e8f0;
		border-radius: 8px;
		padding: 0.5rem 0.25rem;
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
	}
</style>
