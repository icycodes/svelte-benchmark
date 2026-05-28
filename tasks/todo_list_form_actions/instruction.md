# SvelteKit Todo List with Form Actions

## Background
Build a simple but complete todo list web application using **SvelteKit** and **Svelte 5 runes**. The app must use SvelteKit's filesystem-based routing and **Form Actions** (`+page.server.js`/`.ts`) to read and write data from the server, and it must persist todos in a JSON file so that they survive a server restart. The UI should use Svelte 5's new reactivity primitives (`$state`, `$derived`, `$props`).

## Requirements
- A single-page SvelteKit app served at `/`.
- The page displays:
  - An input form to add a new todo.
  - A list of existing todos. Each list item shows the text, a control to toggle completion, and a delete control.
  - The number of remaining (incomplete) todos.
- Three named **Form Actions** on the root page:
  - `add` — adds a new todo from the submitted `text` field.
  - `toggle` — toggles the `completed` flag of the todo whose `id` was submitted.
  - `delete` — removes the todo whose `id` was submitted.
- Todos must be persisted to a JSON file on disk so that data survives a server restart.
- The forms must work both without JavaScript (native form POSTs) and with progressive enhancement (`use:enhance`).

## Implementation Hints
- Initialize the project with the SvelteKit CLI and pick the Svelte 5 / TypeScript or JavaScript template — either is fine.
- Use the **Node adapter** (`@sveltejs/adapter-node`) so the built app can be served with `node build`.
- Put server-only logic (file reads/writes, action handlers, `load` function) in `src/routes/+page.server.{js,ts}`. Put UI in `src/routes/+page.svelte`.
- Use Svelte 5 runes such as `$props`, `$state`, and `$derived` in the page component (for example, to compute the remaining count).
- Use `<form method="POST" action="?/add">` etc. for the Form Actions, and add `use:enhance` from `$app/forms` for progressive enhancement.
- Use a stable id for each todo (e.g., `crypto.randomUUID()`), and serialize the todos to a JSON file under the project directory.

## Acceptance Criteria
- Project path: /home/user/sveltekit-todos
- Start command: `npm run build && node build` (the Node adapter must be configured and the build must succeed)
- Port: 3000 (the server must listen on port 3000; the `PORT` environment variable is set in the environment)
- Routes:
  - `GET /` — Renders the todo list page. The page must include:
    - An input element to enter new todo text (e.g., `<input name="text">`).
    - For each todo, a visible representation of its text, a control to toggle it complete/incomplete, and a control to delete it.
    - A visible indication of the number of remaining (incomplete) todos.
- Form Actions on `/` (in `+page.server.{js,ts}`):
  - `?/add` — Reads a `text` field from the submitted form data and appends a new todo.
  - `?/toggle` — Reads an `id` field and toggles the matching todo's completion state.
  - `?/delete` — Reads an `id` field and removes the matching todo.
- Persistence: Todos are written to a JSON file inside the project directory and reloaded by the `load` function. Restarting the server must not lose todos.
- Svelte 5: The page component must use Svelte 5 runes (`$props`, `$state`, and/or `$derived`).
- Progressive enhancement: Forms must work as plain HTML POSTs *and* use `use:enhance` for the JS-enhanced experience.

