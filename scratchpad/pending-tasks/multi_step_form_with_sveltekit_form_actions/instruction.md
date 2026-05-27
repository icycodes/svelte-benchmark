SvelteKit handles data mutations robustly through server-side Form Actions, providing excellent progressive enhancement and avoiding heavy client-side form libraries.

You need to build a two-step wizard using SvelteKit Form Actions in `+page.server.js` and standard HTML `<form>` elements enhanced with `$app/forms` (like `use:enhance`) in `+page.svelte`. The server action must validate step 1 data, persist it, and transition to step 2.

**Constraints:**
- Must implement the `actions` export object strictly in `+page.server.js`.
- Form data extraction must use `await request.formData()`.
- Do NOT use a third-party form library (e.g., Superforms) for state management.