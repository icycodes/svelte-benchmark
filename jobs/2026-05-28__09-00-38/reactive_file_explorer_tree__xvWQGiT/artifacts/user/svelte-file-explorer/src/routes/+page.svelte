<script>
	import TreeNode from '$lib/TreeNode.svelte';

	let tree = $state({
		name: 'project',
		type: 'folder',
		isOpen: false,
		children: [
			{
				name: 'src',
				type: 'folder',
				isOpen: false,
				children: [
					{
						name: 'lib',
						type: 'folder',
						isOpen: false,
						children: [
							{ name: 'TreeNode.svelte', type: 'file' },
							{ name: 'utils.js', type: 'file' }
						]
					},
					{
						name: 'routes',
						type: 'folder',
						isOpen: false,
						children: [
							{ name: '+page.svelte', type: 'file' },
							{ name: '+layout.svelte', type: 'file' }
						]
					},
					{ name: 'app.d.ts', type: 'file' }
				]
			},
			{
				name: 'static',
				type: 'folder',
				isOpen: false,
				children: [
					{ name: 'favicon.png', type: 'file' },
					{ name: 'robots.txt', type: 'file' }
				]
			},
			{ name: 'package.json', type: 'file' },
			{ name: 'svelte.config.js', type: 'file' }
		]
	});

	const openFolderCount = $derived.by(() => {
		let count = 0;
		function walk(n) {
			if (n.type === 'folder') {
				if (n.isOpen) {
					count++;
					n.children.forEach(walk);
				}
			}
		}
		walk(tree);
		return count;
	});

	const visibleFileCount = $derived.by(() => {
		let count = 0;
		function walk(n) {
			if (n.type === 'folder') {
				if (n.isOpen) {
					n.children.forEach(child => {
						if (child.type === 'file') {
							count++;
						} else {
							walk(child);
						}
					});
				}
			}
		}
		walk(tree);
		return count;
	});
</script>

<div style="padding: 20px; font-family: sans-serif;">
	<div style="background: #f0f0f0; padding: 10px; margin-bottom: 20px; border-radius: 4px;">
		<strong>Status Bar:</strong>
		<span style="margin-left: 20px;">
			Open Folders: <span data-testid="open-folder-count">{openFolderCount}</span>
		</span>
		<span style="margin-left: 20px;">
			Visible Files: <span data-testid="visible-file-count">{visibleFileCount}</span>
		</span>
	</div>

	<TreeNode node={tree} />
</div>
