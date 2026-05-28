<script>
    import { enhance } from '$app/forms';

    let { data } = $props();

    // Derived state for remaining todos
    let remainingCount = $derived(data.todos.filter(todo => !todo.completed).length);
</script>

<main>
    <h1>Todo List</h1>

    <form method="POST" action="?/add" use:enhance>
        <input name="text" type="text" placeholder="What needs to be done?" required />
        <button type="submit">Add Todo</button>
    </form>

    <p><strong>{remainingCount}</strong> {remainingCount === 1 ? 'todo' : 'todos'} remaining</p>

    <ul>
        {#each data.todos as todo (todo.id)}
            <li class:completed={todo.completed}>
                <form method="POST" action="?/toggle" use:enhance style="display: inline;">
                    <input type="hidden" name="id" value={todo.id} />
                    <button type="submit" aria-label="Toggle completion">
                        {todo.completed ? '✅' : '⬜️'}
                    </button>
                </form>

                <span class="todo-text">
                    {todo.text}
                </span>

                <form method="POST" action="?/delete" use:enhance style="display: inline;">
                    <input type="hidden" name="id" value={todo.id} />
                    <button type="submit">Delete</button>
                </form>
            </li>
        {/each}
    </ul>
</main>

<style>
    main {
        max-width: 600px;
        margin: 2rem auto;
        padding: 1rem;
        font-family: sans-serif;
    }

    ul {
        list-style: none;
        padding: 0;
    }

    li {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }

    .completed .todo-text {
        text-decoration: line-through;
        color: #888;
    }

    .todo-text {
        flex-grow: 1;
    }

    button {
        cursor: pointer;
    }
</style>
