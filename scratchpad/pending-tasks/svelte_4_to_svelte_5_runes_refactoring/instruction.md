Migrating older codebases to Svelte 5 requires adopting the new runes-based reactivity system for improved performance and explicit declarations. 

You need to refactor a legacy Svelte 4 component into Svelte 5 by replacing `export let` variable declarations and `$: ` reactive statements with the new runes system in a single `.svelte` file environment. Ensure all reactive dependencies correctly update the DOM.

**Constraints:**
- Do NOT use legacy `$$props`, `<slot>`, or reactive blocks (`$: `).
- Must strictly use the `$props()` and `$derived()` runes.
- The compiled output must successfully pass Svelte 5 syntax validation.