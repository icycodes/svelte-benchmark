<script lang="ts">
	import { enhance } from '$app/forms';

	let { data } = $props();

	let todos = $derived(data.todos);
	let remaining = $derived(todos.filter((t: any) => !t.completed).length);
</script>

<h1>Todo List</h1>

<p>{remaining} remaining</p>

<form method="POST" action="?/add" use:enhance>
	<input name="text" type="text" placeholder="Add a new todo" required />
	<button type="submit">Add</button>
</form>

<ul>
	{#each todos as todo (todo.id)}
		<li>
			<span style="text-decoration: {todo.completed ? 'line-through' : 'none'};">
				{todo.text}
			</span>

			<form method="POST" action="?/toggle" use:enhance style="display:inline;">
				<input type="hidden" name="id" value={todo.id} />
				<button type="submit">
					{todo.completed ? 'Mark Incomplete' : 'Mark Complete'}
				</button>
			</form>

			<form method="POST" action="?/delete" use:enhance style="display:inline;">
				<input type="hidden" name="id" value={todo.id} />
				<button type="submit">Delete</button>
			</form>
		</li>
	{/each}
</ul>
