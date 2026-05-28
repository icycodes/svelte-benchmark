<script>
	import TreeNode from '$lib/TreeNode.svelte';

	const file = (name) => ({ type: 'file', name });
	const folder = (name, children) => ({ type: 'folder', name, open: $state(false), children });

	const tree = [
		folder('src', [
			folder('routes', [file('+page.svelte'), file('+layout.svelte')]),
			folder('lib', [file('TreeNode.svelte'), file('utils.js')])
		]),
		folder('static', [file('logo.png'), file('favicon.png')]),
		folder('tests', [file('tree.spec.js'), file('runes.spec.js')]),
		file('package.json'),
		file('svelte.config.js')
	];

	const openFolderCount = $derived.by(() => countOpenFolders(tree));
	const visibleFileCount = $derived.by(() => countVisibleFiles(tree));

	const countOpenFolders = (nodes) =>
		nodes.reduce((total, node) => {
			if (node.type !== 'folder') return total;
			return total + (node.open ? 1 : 0) + countOpenFolders(node.children);
		}, 0);

	const countVisibleFiles = (nodes, ancestorsOpen = true) =>
		nodes.reduce((total, node) => {
			if (!ancestorsOpen) return total;
			if (node.type === 'file') return total + 1;
			if (!node.open) return total;
			return total + countVisibleFiles(node.children, node.open);
		}, 0);
</script>

<div class="page">
	<header class="status-bar">
		<div class="status-item">
			<span class="label">Open folders</span>
			<span data-testid="open-folder-count" class="count">{openFolderCount}</span>
		</div>
		<div class="status-item">
			<span class="label">Visible files</span>
			<span data-testid="visible-file-count" class="count">{visibleFileCount}</span>
		</div>
	</header>

	<main class="tree">
		{#each tree as node (node.name)}
			<TreeNode node={node} />
		{/each}
	</main>
</div>

<style>
	.page {
		min-height: 100vh;
		background: #f8fafc;
		color: #0f172a;
	}

	.status-bar {
		position: sticky;
		top: 0;
		z-index: 10;
		display: flex;
		gap: 24px;
		align-items: center;
		padding: 12px 16px;
		background: #0f172a;
		color: #e2e8f0;
		font-family: system-ui, sans-serif;
		font-size: 14px;
	}

	.status-item {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.label {
		text-transform: uppercase;
		letter-spacing: 0.08em;
		font-size: 11px;
		opacity: 0.8;
	}

	.count {
		font-size: 18px;
		font-weight: 600;
	}

	.tree {
		padding: 16px;
	}
</style>
