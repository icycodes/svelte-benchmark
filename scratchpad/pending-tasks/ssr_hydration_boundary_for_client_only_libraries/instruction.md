Integrating non-SSR-friendly libraries (like Leaflet or Canvas APIs) into SvelteKit often causes server-side rendering errors or hydration mismatches because the library expects a `window` object.

You need to implement a Svelte component that acts as an SSR boundary, safely wrapping a mock client-only mapping library. Ensure the wrapper completely bypasses server execution and only initializes the map on the client after the component is mounted in the DOM.

**Constraints:**
- Must use the `$effect` rune to handle the client-only initialization logic.
- Do NOT use the legacy Svelte 4 `onMount` lifecycle hook.
- Ensure a placeholder UI (e.g., a loading spinner) is rendered during the SSR pass.