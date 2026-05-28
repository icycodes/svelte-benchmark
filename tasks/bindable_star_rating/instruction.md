# Reusable Star Rating Component with Svelte 5 `$bindable`

## Background
You are building a SvelteKit application that lets visitors rate products. To keep the UI consistent, you need a reusable `StarRating` component implemented with Svelte 5 runes. The component must accept and expose its current rating through two-way binding so that the host page can both read and write the value without resorting to event dispatching.

This task evaluates your ability to design a Svelte 5 component using `$state`, `$props`, and most importantly `$bindable`, then wire it into a SvelteKit route that reflects the bound value reactively.

## Requirements
- Create a SvelteKit application at `/home/user/rating-app` using Svelte 5 runes mode.
- Implement a reusable component at `src/lib/StarRating.svelte` that:
  - Renders exactly five interactive star buttons.
  - Exposes a numeric `value` prop that is bindable (the parent can use `bind:value`).
  - Accepts an optional `max` prop (defaults to `5`).
  - When a star at position `n` (1-indexed) is clicked, the bound value updates to `n`.
  - Visually distinguishes filled stars (value index <= current value) from empty stars so they can be detected from the DOM (e.g. via a stable class name or `data-*` attribute).
- Create a page route at `src/routes/+page.svelte` that:
  - Holds a single rating state initialised to `0`.
  - Uses `bind:value` to connect the `StarRating` component to this state.
  - Displays the current numeric rating in a heading so it can be inspected from the page.
  - Provides a button labelled `Reset` that sets the bound value back to `0` from the parent side, demonstrating that the binding is truly two-way.

## Implementation Hints
- Initialise the project with the official Svelte scaffolder (`npx sv create`) and choose the Svelte 5 / SvelteKit template with the `node` adapter so the app can run with `npm run build && node build`.
- Use the `$bindable()` helper inside `$props()` to declare the bindable `value` prop; remember that an initial value passed to `$bindable()` acts as the default when the parent does not bind.
- Use `$state` only where local component state is genuinely needed; the rating itself should live on the parent and flow into the child via the bindable prop.
- Make the filled/empty state observable from the DOM with a stable hook such as a `filled` class on each star element or a `data-filled` attribute set to `"true"` or `"false"`. The verifier will use a stable selector.
- The display heading should include the exact text `Rating: <n>` (where `<n>` is the current numeric value) so it can be located reliably.
- Configure the adapter so the production build is started with `node build` and listens on port 3000.

## Acceptance Criteria
- Project path: `/home/user/rating-app`
- Start command: `npm run build && PORT=3000 HOST=0.0.0.0 node build`
- Port: `3000`
- Routes:
  - `GET /`: Returns the rating page UI that:
    - Contains a heading whose text matches the pattern `Rating: <n>` reflecting the current rating (initially `0`).
    - Contains exactly 5 interactive star elements, each clickable to set the rating to its 1-indexed position.
    - Marks filled vs. empty stars with a stable, queryable DOM hook (such as a `filled` class on the star element or a `data-filled` attribute) so a test can count how many stars are currently filled.
    - Provides a `Reset` button that sets the rating back to `0` and updates the heading and stars accordingly.
- The `StarRating` component file must exist at `src/lib/StarRating.svelte` and expose a bindable `value` prop using the Svelte 5 `$bindable()` rune so that `<StarRating bind:value={rating} />` works in any consumer.

