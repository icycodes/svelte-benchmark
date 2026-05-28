/**
 * Reactive tree model using Svelte 5 runes.
 *
 * Each FolderNode has an `open` flag tracked with `$state` so that
 * toggling one folder only re-renders its own subtree.
 *
 * The global status counts are exposed via a reactive class so that
 * $derived can live inside the class body (the correct Svelte 5 pattern
 * for sharable reactive computations in .svelte.ts modules).
 */

export type FileNode = {
	kind: 'file';
	name: string;
};

export type FolderNode = {
	kind: 'folder';
	name: string;
	open: boolean;
	children: TreeNodeData[];
};

export type TreeNodeData = FileNode | FolderNode;

/** Create a folder node whose `open` flag is individually reactive. */
function folder(name: string, children: TreeNodeData[]): FolderNode {
	let _open = $state(false);
	return {
		kind: 'folder',
		name,
		get open() { return _open; },
		set open(v: boolean) { _open = v; },
		children,
	};
}

/** Create a plain file leaf. */
function file(name: string): FileNode {
	return { kind: 'file', name };
}

// ---------------------------------------------------------------------------
// Hard-coded demo tree
// ---------------------------------------------------------------------------

export const tree: TreeNodeData[] = [
	folder('src', [
		folder('routes', [
			file('+page.svelte'),
			file('+layout.svelte'),
		]),
		folder('lib', [
			folder('components', [
				file('Button.svelte'),
				file('Modal.svelte'),
				file('Tooltip.svelte'),
			]),
			folder('utils', [
				file('format.ts'),
				file('math.ts'),
			]),
			file('index.ts'),
		]),
		file('app.html'),
		file('app.d.ts'),
	]),
	folder('static', [
		file('favicon.png'),
		file('robots.txt'),
	]),
	folder('tests', [
		folder('unit', [
			file('format.test.ts'),
			file('math.test.ts'),
		]),
		folder('e2e', [
			file('home.spec.ts'),
		]),
	]),
	file('package.json'),
	file('svelte.config.js'),
	file('tsconfig.json'),
	file('vite.config.ts'),
];

// ---------------------------------------------------------------------------
// Derived global counts — wrapped in a class so $derived is valid
// ---------------------------------------------------------------------------

/** Recursively count open folders and visible files within a list of nodes. */
function countNodes(nodes: TreeNodeData[]): { folders: number; files: number } {
	let folders = 0;
	let files = 0;
	for (const node of nodes) {
		if (node.kind === 'file') {
			files++;
		} else {
			if (node.open) {
				folders++;
				const child = countNodes(node.children);
				folders += child.folders;
				files += child.files;
			}
		}
	}
	return { folders, files };
}

class TreeStats {
	openFolderCount = $derived(countNodes(tree).folders);
	visibleFileCount = $derived(countNodes(tree).files);
}

export const treeStats = new TreeStats();
