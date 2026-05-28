<script lang="ts">
	import TreeNode from '$lib/TreeNode.svelte';

	type Node = {
		name: string;
		type: 'folder' | 'file';
		children?: Node[];
		open?: boolean;
	};

	let tree: Node[] = $state([
		{
			name: 'src',
			type: 'folder',
			open: false,
			children: [
				{
					name: 'lib',
					type: 'folder',
					open: false,
					children: [
						{ name: 'TreeNode.svelte', type: 'file' },
						{ name: 'utils.ts', type: 'file' }
					]
				},
				{
					name: 'routes',
					type: 'folder',
					open: false,
					children: [
						{ name: '+page.svelte', type: 'file' },
						{ name: '+layout.svelte', type: 'file' }
					]
				}
			]
		},
		{
			name: 'static',
			type: 'folder',
			open: false,
			children: [
				{ name: 'favicon.png', type: 'file' }
			]
		},
		{ name: 'package.json', type: 'file' },
		{ name: 'svelte.config.js', type: 'file' }
	]);

	function getStats(nodes: Node[], visible: boolean) {
		let openFolders = 0;
		let visibleFiles = 0;

		for (const node of nodes) {
			if (node.type === 'folder') {
				if (node.open) openFolders++;
				const childStats = getStats(node.children || [], visible && !!node.open);
				openFolders += childStats.openFolders;
				visibleFiles += childStats.visibleFiles;
			} else if (node.type === 'file') {
				if (visible) visibleFiles++;
			}
		}

		return { openFolders, visibleFiles };
	}

	let stats = $derived(getStats(tree, true));
</script>

<div class="status-bar" style="padding: 10px; background: #eee; border-bottom: 1px solid #ccc; margin-bottom: 20px;">
	Open folders: <span data-testid="open-folder-count">{stats.openFolders}</span> |
	Visible files: <span data-testid="visible-file-count">{stats.visibleFiles}</span>
</div>

<div class="tree">
	{#each tree as node}
		<TreeNode {node} />
	{/each}
</div>
