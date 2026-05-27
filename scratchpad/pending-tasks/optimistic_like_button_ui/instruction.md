Modern interactive applications utilize Optimistic UI to provide instantaneous feedback to the user before the server explicitly confirms the state change, dropping virtual DOM overhead.

You need to implement an optimistic "Like" button in Svelte 5 that immediately increments a local like counter using `$state` when clicked, while simultaneously dispatching a mock asynchronous `fetch` request to the server. 

**Constraints:**
- If the simulated server request fails, the local like counter must accurately revert to its previous state.
- Do NOT block the UI thread waiting for the server response before updating the visual count.
- Local state management must only use Svelte 5 runes, avoiding external state stores like Redux or native Svelte `writable`.