<script>
	import { enhance } from '$app/forms';

	let { data } = $props();
	let newText = $state('');

	const todos = $derived(() => data.todos ?? []);
	const remaining = $derived(() => todos.filter((todo) => !todo.completed).length);
</script>

<main class="page">
	<section class="card">
		<header class="header">
			<h1>Todo List</h1>
			<p>{remaining} remaining</p>
		</header>

		<form method="POST" action="?/add" use:enhance class="add-form">
			<label class="field">
				<span class="label">New todo</span>
				<input
					name="text"
					required
					placeholder="What needs doing?"
					bind:value={newText}
				/>
			</label>
			<button type="submit">Add</button>
		</form>

		{#if todos.length === 0}
			<p class="empty">Nothing here yet.</p>
		{:else}
			<ul class="list">
				{#each todos as todo (todo.id)}
					<li class:completed={todo.completed}>
						<span class="text">{todo.text}</span>
						<div class="actions">
							<form method="POST" action="?/toggle" use:enhance>
								<input type="hidden" name="id" value={todo.id} />
								<button type="submit">
									{todo.completed ? 'Undo' : 'Complete'}
								</button>
							</form>
							<form method="POST" action="?/delete" use:enhance>
								<input type="hidden" name="id" value={todo.id} />
								<button type="submit" class="danger">Delete</button>
							</form>
						</div>
					</li>
				{/each}
			</ul>
		{/if}
	</section>
</main>

<style>
	:global(body) {
		margin: 0;
		font-family: system-ui, sans-serif;
		background: #f4f6fb;
		color: #1f2933;
	}

	.page {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 2rem;
	}

	.card {
		width: min(720px, 100%);
		background: white;
		padding: 2rem;
		border-radius: 16px;
		box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
		display: grid;
		gap: 1.5rem;
	}

	.header {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
	}

	.add-form {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 1rem;
		align-items: end;
	}

	.field {
		display: grid;
		gap: 0.5rem;
	}

	.label {
		font-size: 0.9rem;
		color: #52606d;
	}

	input {
		padding: 0.65rem 0.75rem;
		border-radius: 8px;
		border: 1px solid #cbd2d9;
		font-size: 1rem;
	}

	button {
		padding: 0.6rem 1rem;
		border-radius: 8px;
		border: none;
		background: #2563eb;
		color: white;
		cursor: pointer;
		font-weight: 600;
	}

	button.danger {
		background: #dc2626;
	}

	.list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 1rem;
	}

	li {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.75rem 1rem;
		border-radius: 12px;
		background: #f8fafc;
	}

	li.completed .text {
		text-decoration: line-through;
		color: #94a3b8;
	}

	.actions {
		display: flex;
		gap: 0.5rem;
	}

	.actions form {
		margin: 0;
	}

	.empty {
		color: #7b8794;
	}

	@media (max-width: 600px) {
		.add-form {
			grid-template-columns: 1fr;
		}

		.header {
			flex-direction: column;
			gap: 0.5rem;
		}

		li {
			flex-direction: column;
			align-items: flex-start;
			gap: 0.75rem;
		}

		.actions {
			width: 100%;
			justify-content: flex-start;
			flex-wrap: wrap;
		}
	}
</style>
