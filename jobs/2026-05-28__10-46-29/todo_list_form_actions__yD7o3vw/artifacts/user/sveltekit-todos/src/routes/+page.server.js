import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { fail } from '@sveltejs/kit';

// Resolve an absolute path to the JSON file next to this source file.
// Using import.meta.url keeps it stable regardless of the CWD at runtime.
const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_FILE = join(__dirname, '..', '..', 'todos.json');

/** @returns {Array<{id: string, text: string, completed: boolean}>} */
function readTodos() {
	if (!existsSync(DATA_FILE)) return [];
	try {
		return JSON.parse(readFileSync(DATA_FILE, 'utf-8'));
	} catch {
		return [];
	}
}

/** @param {Array<{id: string, text: string, completed: boolean}>} todos */
function writeTodos(todos) {
	writeFileSync(DATA_FILE, JSON.stringify(todos, null, 2), 'utf-8');
}

/** @type {import('./$types').PageServerLoad} */
export function load() {
	const todos = readTodos();
	return { todos };
}

/** @type {import('./$types').Actions} */
export const actions = {
	/** Add a new todo from the `text` form field. */
	add: async ({ request }) => {
		const data = await request.formData();
		const text = (data.get('text') ?? '').toString().trim();

		if (!text) {
			return fail(400, { error: 'Todo text cannot be empty.' });
		}

		const todos = readTodos();
		todos.push({ id: crypto.randomUUID(), text, completed: false });
		writeTodos(todos);
	},

	/** Toggle the `completed` flag for the todo whose `id` was submitted. */
	toggle: async ({ request }) => {
		const data = await request.formData();
		const id = (data.get('id') ?? '').toString();

		const todos = readTodos();
		const todo = todos.find((t) => t.id === id);
		if (!todo) return fail(404, { error: 'Todo not found.' });

		todo.completed = !todo.completed;
		writeTodos(todos);
	},

	/** Remove the todo whose `id` was submitted. */
	delete: async ({ request }) => {
		const data = await request.formData();
		const id = (data.get('id') ?? '').toString();

		const todos = readTodos();
		const filtered = todos.filter((t) => t.id !== id);
		writeTodos(filtered);
	}
};
