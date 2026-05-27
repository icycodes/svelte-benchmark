Creating highly reusable and customizable UI components in Svelte 5 is achieved by leveraging the new Snippets feature, which replaces older slot-based composition.

You need to implement a generic `Table.svelte` component that accepts an array of arbitrary data objects and utilizes Svelte 5 `{#snippet}` blocks to allow parent components to define custom cell rendering templates for different columns. 

**Constraints:**
- Must use `{#snippet}` and `{@render}` tags for column definitions.
- Do NOT use the deprecated `<slot>` element.
- Must provide a default snippet fallback if the parent does not supply a custom column template.