# Reactive Nested File Explorer with Svelte 5 Runes

## Background
Build a small **SvelteKit** application that demonstrates **Svelte 5 fine-grained reactivity** by implementing an interactive, nested file-explorer tree. Toggling a folder must update only the affected subtree (the rest of the tree stays mounted), and an always-visible status bar at the top of the page must recompute, in real time, how many folders are currently open and how many total files are visible in the expanded portions of the tree.

The component must be **recursive** (folders contain folders), driven by the new **runes** (`$state`, `$derived`, `$props`), and rendered through a single reusable component.

## Requirements
- A single page served at `/` that renders one **recursive** file-explorer component for a hard-coded tree of folders and files.
- A reusable component must render a node. When the node is a folder, the component must render itself recursively for each child. Folders must start **collapsed** by default.
- Clicking a folder must toggle that folder open/closed. Toggling one folder must **not** collapse other open folders.
- Files (leaf nodes) must be rendered as plain rows that are not clickable as folders.
- An always-visible status bar at the top of the page must display the live counts of:
  - the number of folders currently open, and
  - the total number of files visible (i.e. files inside open folders, recursively; files inside collapsed folders do not count).
  These counts must update reactively as folders are toggled, using `$state` for the open/closed state and `$derived` for the counts.
- Each rendered folder row must include a small indicator showing whether it is open or closed (e.g. a `▶` for closed and `▼` for open). The indicator must update immediately when the folder is toggled.

## Implementation Hints
- Initialize the project with the SvelteKit CLI (`npx sv create`) using the minimal template (JavaScript or TypeScript is acceptable).
- Use the **Node adapter** (`@sveltejs/adapter-node`) so the built app can be served with `node build` and the server listens on the `PORT` environment variable.
- Put the recursive component at `src/lib/TreeNode.svelte` and have `src/routes/+page.svelte` render it with the top-level tree.
- The recursive component must accept its props with `$props()` and import/render itself by name to traverse children.
- Model the tree as plain JavaScript data and wrap the per-folder `open` flag in `$state` so toggles are fine-grained — collapsing one folder must not re-mount sibling subtrees.
- Compute the status-bar counts with `$derived` (or `$derived.by`) based on the shared reactive tree, not by manually wiring callbacks from each child.
- You are free to style the page minimally; only the observable DOM behavior described in the acceptance criteria is verified.

## Acceptance Criteria
- Project path: /home/user/svelte-file-explorer
- Start command: `npm run build && node build`
- Port: 3000 (the server must listen on the port given in the `PORT` environment variable)
- Routes:
  - `GET /` — Renders the demo page. The page must contain:
    - An always-visible status bar with two reactive counters: the number of currently open folders and the number of currently visible files. The counters must be machine-readable: the open-folders counter must have `data-testid="open-folder-count"` and the visible-files counter must have `data-testid="visible-file-count"`, and the text content of each element must be the current integer count (e.g. `0`, `3`).
    - A recursive folder/file tree. Every folder row must:
      - have `data-testid="folder"` and a `data-folder-name` attribute equal to the folder's name,
      - have a `data-open` attribute whose value is `"true"` when the folder is open and `"false"` when closed,
      - act as a click target that toggles the folder open/closed (clicking the folder row, or a button/icon inside it, must flip the state),
      - show a textual indicator that contains `▼` when open and `▶` when closed.
    - Every file row must have `data-testid="file"` and a `data-file-name` attribute equal to the file's name. File rows for files inside a closed folder must not be present in the DOM (i.e. they are only rendered when their parent chain is fully open).
- Recursive component:
  - There must be a single reusable component at `src/lib/TreeNode.svelte` that is used recursively to render both folders and files.
  - `TreeNode.svelte` must declare its props using `$props(` and must reference itself by name (e.g. `<TreeNode ... />`) inside its template to recurse on children.
- Svelte 5 runes:
  - The source files of the page and the component, taken together, must use at least one `$state(` and at least one `$derived(` (or `$derived.by(`) call.
- SvelteKit Node adapter:
  - `svelte.config.js` (or `.ts`) must import `adapter` from `@sveltejs/adapter-node` and use it as the kit adapter.
  - The build output `/home/user/svelte-file-explorer/build/index.js` must exist after running `npm run build`.

