# Generic Data Table with Svelte 5 Snippets in SvelteKit

## Background
Svelte 5 introduces a brand-new way of composing reusable markup blocks called **snippets** (`{#snippet ...}` / `{@render ...}`), which replace the old slot mechanism. Combined with Svelte 5 runes (`$state`, `$derived`, `$props`), they enable you to build truly generic, type-safe, highly composable UI components.

In this task you will build a small SvelteKit application that renders a generic, reusable `Table` component for a product inventory page. The same `Table` component must be flexible enough to be reused for any tabular data by letting callers pass in their own header and row snippets.

## Requirements
- Initialize a SvelteKit (Svelte 5) project at `/home/user/myproject` using the official Svelte CLI.
- Implement a reusable component at `src/lib/Table.svelte` that:
  - Accepts a `data` prop (an array of items).
  - Accepts a `header` snippet prop describing the table's `<th>` cells.
  - Accepts a `row` snippet prop that receives a single data item and describes its `<td>` cells.
  - Renders a real HTML `<table>` element with a `<thead>` (containing the `header` snippet) and a `<tbody>` (rendering the `row` snippet once per item).
- Implement the home page at `src/routes/+page.svelte` that uses the `Table` component to render a product inventory.
  - The product list MUST be declared with `$state` so it is reactive.
  - The grand total (sum of `qty * price` across all products) MUST be displayed and MUST be computed with `$derived` (or `$derived.by`).
  - The page MUST allow adding a new product through three input fields and a button. Adding a product MUST update the table and the grand total immediately (no full-page reload).

## Implementation Hints
- Create the project non-interactively with `npx sv create` using the minimal template and a package manager of your choice.
- Use Svelte 5 snippet syntax with `{#snippet name(args)}...{/snippet}` and `{@render name(args)}` instead of legacy `<slot>` elements.
- Pass snippets to the `Table` component using the implicit-prop form: declare the snippets inside the `<Table>...</Table>` tags.
- Bind the three input fields to local `$state` values with `bind:value` and clear them after a successful add.
- The grand total must react automatically when the products array changes — use `$derived` so you don't have to recompute it manually.
- For production verification use the SvelteKit preview server (a static-ish local production server) rather than the dev server.

## Acceptance Criteria
- Project path: `/home/user/myproject`
- Start command: `npm run build && npm run preview -- --host 0.0.0.0 --port 4173`
- Port: `4173`
- Routes & UI:
  - `GET /` returns an HTML page that renders a single `<table>` element produced by `src/lib/Table.svelte`.
  - The table MUST have a `<thead>` row of `<th>` cells produced from the `header` snippet and a `<tbody>` whose `<tr>` rows are produced from the `row` snippet (one row per product).
  - The page MUST display the current grand total of `qty * price` across all products. The total MUST appear inside an element with the attribute `data-testid="grand-total"` and its text content MUST be the numeric total (e.g. `30`).
  - The add-product form MUST expose three input fields and a button with the following stable selectors:
    - `input[data-testid="product-name"]` – product name (text)
    - `input[data-testid="product-qty"]` – product quantity (integer)
    - `input[data-testid="product-price"]` – product unit price (number)
    - `button[data-testid="add-product"]` – submits the new product
  - Clicking the add button MUST append a new `<tr>` for the product to the table's `<tbody>` and update the value inside `data-testid="grand-total"` — both without a full page reload.
- The `Table` component MUST live at `src/lib/Table.svelte` and MUST use Svelte 5 snippets (`{@render ...}`). It MUST NOT use the legacy `<slot>` element.
- The home page MUST live at `src/routes/+page.svelte` and MUST declare its product list with `$state` and its grand total with `$derived` (or `$derived.by`).

