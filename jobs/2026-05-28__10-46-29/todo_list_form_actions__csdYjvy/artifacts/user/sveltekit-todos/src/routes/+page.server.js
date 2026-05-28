import { fail } from '@sveltejs/kit';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const dataFilePath = path.resolve('data', 'todos.json');

async function ensureDataFile() {
	await mkdir(path.dirname(dataFilePath), { recursive: true });
	try {
		await readFile(dataFilePath, 'utf-8');
	} catch (error) {
		if (error.code === 'ENOENT') {
			await writeFile(dataFilePath, JSON.stringify([], null, 2));
			return;
		}
		throw error;
	}
}

async function readTodos() {
	await ensureDataFile();
	const raw = await readFile(dataFilePath, 'utf-8');
	return JSON.parse(raw);
}

async function writeTodos(todos) {
	await ensureDataFile();
	await writeFile(dataFilePath, JSON.stringify(todos, null, 2));
}

export const load = async () => {
	const todos = await readTodos();
	return { todos };
};

export const actions = {
	add: async ({ request }) => {
		const formData = await request.formData();
		const text = String(formData.get('text') ?? '').trim();

		if (!text) {
			return fail(400, { message: 'Todo text is required.' });
		}

		const todos = await readTodos();
		todos.push({
			id: crypto.randomUUID(),
			text,
			completed: false
		});
		await writeTodos(todos);

		return { success: true };
	},
	toggle: async ({ request }) => {
		const formData = await request.formData();
		const id = String(formData.get('id') ?? '');

		if (!id) {
			return fail(400, { message: 'Todo id is required.' });
		}

		const todos = await readTodos();
		const todo = todos.find((item) => item.id === id);

		if (!todo) {
			return fail(404, { message: 'Todo not found.' });
		}

		todo.completed = !todo.completed;
		await writeTodos(todos);

		return { success: true };
	},
	delete: async ({ request }) => {
		const formData = await request.formData();
		const id = String(formData.get('id') ?? '');

		if (!id) {
			return fail(400, { message: 'Todo id is required.' });
		}

		const todos = await readTodos();
		const nextTodos = todos.filter((item) => item.id !== id);

		if (nextTodos.length === todos.length) {
			return fail(404, { message: 'Todo not found.' });
		}

		await writeTodos(nextTodos);

		return { success: true };
	}
};
