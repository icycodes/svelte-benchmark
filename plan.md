### 1. Library Overview

*   **Description**: Svelte is a compiler-based UI framework that converts declarative components into highly optimized vanilla JavaScript. SvelteKit is its official application framework, providing filesystem-based routing, server-side rendering (SSR), and data fetching.
*   **Ecosystem Role**: Positioned as a "transitional" framework that bridges the gap between traditional multi-page apps and modern single-page apps. It competes with Next.js (React) and Nuxt (Vue).
*   **Project Setup**:
    1.  Initialize: `npx sv create my-app`
    2.  Navigate: `cd my-app`
    3.  Install: `npm install`
    4.  Dev Server: `npm run dev`
    5.  Check: `npx sv check` (for TypeScript/Linting)

### 2. Core Primitives & APIs

#### Svelte 5 Runes (Reactivity)
*   **$state**: Declares reactive state. Deeply reactive for objects/arrays.
    ```svelte
    <script>
      let count = $state(0);
      let user = $state({ name: 'Alice' });
    </script>
    <button onclick={() => count++}>{count}</button>
    ```
*   **$derived**: Declares state derived from other reactive values.
    ```js
    let doubled = $derived(count * 2);
    let fullName = $derived.by(() => `${user.firstName} ${user.lastName}`);
    ```
*   **$effect**: Runs side effects when dependencies change. Replaces lifecycle hooks like `onMount`.
    ```js
    $effect(() => {
      console.log('Count changed to:', count);
      return () => console.log('Cleanup');
    });
    ```
*   **$props & $bindable**: Receives inputs and marks them as two-way bindable.
    ```js
    let { value = $bindable(), name } = $props();
    ```

#### Snippets & Rendering
*   **Snippets**: Reusable template blocks within a component.
    ```svelte
    {#snippet item(text)}
      <li>{text}</li>
    {/snippet}
    <ul>
      {@render item('First')}
      {@render item('Second')}
    </ul>
    ```

#### SvelteKit Routing & Data
*   **Routing**: Defined by `src/routes/` directory structure.
    *   `+page.svelte`: The UI for a route.
    *   `+page.server.js`: Server-only data loading (`load`) and actions.
    *   `+layout.svelte`: Shared UI across sub-routes.
*   **Form Actions**: Handle POST requests from HTML forms.
    ```js
    // +page.server.js
    export const actions = {
      default: async ({ request }) => {
        const data = await request.formData();
        // process data
      }
    };
    ```

*   **Documentation Links**:
    *   [Svelte Runes](https://svelte.dev/docs/svelte/runes)
    *   [SvelteKit Routing](https://svelte.dev/docs/kit/routing)
    *   [SvelteKit Load Functions](https://svelte.dev/docs/kit/load)

### 3. Real-World Use Cases & Templates

*   **SaaS Boilerplates**: SvelteKit is widely used for SaaS due to its excellent SEO (SSR) and fast interaction.
*   **Interactive Dashboards**: Leveraging Svelte 5's fine-grained reactivity (signals) for real-time data updates without virtual DOM overhead.
*   **Official Demo**: The "SvelteKit Demo App" (a word-guessing game) available via `npx sv create`.
*   **Integration Patterns**:
    *   **Auth**: Usually handled in `hooks.server.js` to protect routes.
    *   **DB**: Direct access in `+page.server.js` using Prisma or Drizzle.

### 4. Developer Friction Points

*   **Hydration Timing**: Tests (e.g., Playwright) often click buttons before hydration is finished, leading to "silent" failures where the click doesn't trigger the Svelte handler. [Issue Discussion](https://github.com/sveltejs/kit/discussions/13455)
*   **i18n & app.html**: Controlling global attributes like `<html lang="...">` dynamically is tricky and often requires complex `transformPageChunk` logic in hooks. [Issue Discussion](https://github.com/sveltejs/kit/discussions/12001)
*   **Editor "Tab Overload"**: Having multiple `+page.svelte` files open makes it hard to distinguish between routes in the IDE tab bar.

### 5. Evaluation Ideas

*   **Runes Refactor**: Refactor a Svelte 4 component using `export let` and `$: doubled = ...` to Svelte 5 `$props` and `$derived`.
*   **Generic Data Table**: Implement a `Table` component using Snippets to allow users to define custom cell rendering for different columns.
*   **Multi-Step Form**: Build a multi-step wizard using SvelteKit Form Actions and `$app/forms` to handle validation and state persistence across steps.
*   **Reactive Tree Structure**: Create a nested file explorer where toggling a folder's state (`$state`) updates the entire view efficiently.
*   **SSR Hydration Boundary**: Implement a component that wraps a non-SSR-friendly library (like Leaflet) and ensure it only initializes on the client using `$effect`.
*   **Optimistic UI**: Use Svelte 5.25's "overridable deriveds" to implement an optimistic "Like" button that updates immediately while the server request is pending.

### 6. Sources

1. [Svelte Official Documentation (llms.txt)](https://svelte.dev/llms.txt) - Central hub for LLM-friendly documentation.
2. [Svelte 5 Runes Reference](https://svelte.dev/docs/svelte/runes) - Detailed guide on the new reactivity system.
3. [SvelteKit Routing Guide](https://svelte.dev/docs/kit/routing) - Core filesystem-based routing documentation.
4. [Svelte CLI Documentation](https://svelte.dev/docs/cli/overview) - Details on the `sv` tool.
5. [GitHub Discussion #13455](https://github.com/sveltejs/kit/discussions/13455) - Scale issues and friction points in large SvelteKit projects.
6. [Svelte 5 Snippets Tutorial](https://svelte.dev/tutorial/svelte/snippets-and-render-tags) - Interactive guide to snippets.