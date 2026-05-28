<script>
	import { enhance } from '$app/forms';

	// Svelte 5: receive server data via $props()
	let { data, form } = $props();

	// Svelte 5: derived — always reflects the latest server data after actions
	let todos = $derived(data.todos);

	// Svelte 5: derived value — count of incomplete todos
	let remaining = $derived(todos.filter((t) => !t.completed).length);

	// Controlled input value for the new-todo text field
	let newText = $state('');
</script>

<svelte:head>
	<title>SvelteKit Todos</title>
</svelte:head>

<main>
	<h1>Todo List</h1>

	<!-- ── Add todo form ──────────────────────────────────────────── -->
	<form
		method="POST"
		action="?/add"
		use:enhance={() => {
			return ({ update }) => {
				newText = '';
				update();
			};
		}}
	>
		<div class="add-row">
			<input
				name="text"
				type="text"
				placeholder="What needs to be done?"
				bind:value={newText}
				required
				aria-label="New todo text"
			/>
			<button type="submit">Add</button>
		</div>

		{#if form?.error}
			<p class="error" role="alert">{form.error}</p>
		{/if}
	</form>

	<!-- ── Remaining count ───────────────────────────────────────── -->
	<p class="remaining">
		<strong>{remaining}</strong>
		{remaining === 1 ? 'item' : 'items'} remaining
	</p>

	<!-- ── Todo list ─────────────────────────────────────────────── -->
	{#if todos.length === 0}
		<p class="empty">No todos yet — add one above!</p>
	{:else}
		<ul class="todo-list">
			{#each todos as todo (todo.id)}
				<li class:completed={todo.completed}>
					<!-- Toggle form -->
					<form method="POST" action="?/toggle" use:enhance>
						<input type="hidden" name="id" value={todo.id} />
						<button
							type="submit"
							class="toggle"
							aria-label={todo.completed ? 'Mark incomplete' : 'Mark complete'}
							title={todo.completed ? 'Mark incomplete' : 'Mark complete'}
						>
							{#if todo.completed}
								✅
							{:else}
								⬜
							{/if}
						</button>
					</form>

					<!-- Todo text -->
					<span class="todo-text">{todo.text}</span>

					<!-- Delete form -->
					<form method="POST" action="?/delete" use:enhance>
						<input type="hidden" name="id" value={todo.id} />
						<button type="submit" class="delete" aria-label="Delete todo" title="Delete">
							🗑️
						</button>
					</form>
				</li>
			{/each}
		</ul>
	{/if}
</main>

<style>
	:global(*, *::before, *::after) {
		box-sizing: border-box;
	}

	:global(body) {
		margin: 0;
		font-family: system-ui, -apple-system, sans-serif;
		background: #f5f5f5;
		color: #1a1a1a;
	}

	main {
		max-width: 560px;
		margin: 3rem auto;
		padding: 0 1rem;
	}

	h1 {
		font-size: 2rem;
		margin-bottom: 1.25rem;
		text-align: center;
	}

	/* ── Add form ── */
	.add-row {
		display: flex;
		gap: 0.5rem;
	}

	input[type='text'] {
		flex: 1;
		padding: 0.6rem 0.8rem;
		font-size: 1rem;
		border: 2px solid #ccc;
		border-radius: 6px;
		outline: none;
		transition: border-color 0.2s;
	}

	input[type='text']:focus {
		border-color: #4a90e2;
	}

	button[type='submit']:not(.toggle):not(.delete) {
		padding: 0.6rem 1.2rem;
		font-size: 1rem;
		background: #4a90e2;
		color: #fff;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		transition: background 0.2s;
	}

	button[type='submit']:not(.toggle):not(.delete):hover {
		background: #357abd;
	}

	.error {
		color: #c0392b;
		margin-top: 0.4rem;
		font-size: 0.9rem;
	}

	/* ── Remaining count ── */
	.remaining {
		text-align: center;
		margin: 1rem 0 0.5rem;
		font-size: 0.95rem;
		color: #555;
	}

	/* ── List ── */
	.todo-list {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	li {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background: #fff;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		padding: 0.6rem 0.8rem;
		margin-bottom: 0.5rem;
		transition: opacity 0.2s;
	}

	li.completed .todo-text {
		text-decoration: line-through;
		color: #999;
	}

	.todo-text {
		flex: 1;
		font-size: 1rem;
		word-break: break-word;
	}

	/* ── Icon buttons ── */
	.toggle,
	.delete {
		background: none;
		border: none;
		cursor: pointer;
		font-size: 1.2rem;
		line-height: 1;
		padding: 0.1rem 0.2rem;
		border-radius: 4px;
		transition: background 0.15s;
	}

	.toggle:hover,
	.delete:hover {
		background: #f0f0f0;
	}

	.empty {
		text-align: center;
		color: #999;
		margin-top: 1.5rem;
	}
</style>
