Svelte 5's `$state` rune provides deep reactivity out of the box, making it highly efficient for complex nested data structures like trees and file systems.

You need to create a nested file explorer component representing a directory structure. The component must consume a deeply nested object of files and folders, using `$state` so that toggling a folder's open/closed boolean immediately and efficiently updates the view.

**Constraints:**
- Must declare the initial nested state utilizing the `$state` rune.
- Must handle infinite nesting depth via either recursive component rendering or recursive Svelte snippets.
- Toggling a folder must mutate the state directly rather than forcing a full re-assignment of the tree root.