import { existsSync, readFileSync, writeFileSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import { fail } from "@sveltejs/kit";
const __dirname$1 = dirname(fileURLToPath(import.meta.url));
const DATA_FILE = join(__dirname$1, "..", "..", "todos.json");
function readTodos() {
  if (!existsSync(DATA_FILE)) return [];
  try {
    return JSON.parse(readFileSync(DATA_FILE, "utf-8"));
  } catch {
    return [];
  }
}
function writeTodos(todos) {
  writeFileSync(DATA_FILE, JSON.stringify(todos, null, 2), "utf-8");
}
function load() {
  const todos = readTodos();
  return { todos };
}
const actions = {
  /** Add a new todo from the `text` form field. */
  add: async ({ request }) => {
    const data = await request.formData();
    const text = (data.get("text") ?? "").toString().trim();
    if (!text) {
      return fail(400, { error: "Todo text cannot be empty." });
    }
    const todos = readTodos();
    todos.push({ id: crypto.randomUUID(), text, completed: false });
    writeTodos(todos);
  },
  /** Toggle the `completed` flag for the todo whose `id` was submitted. */
  toggle: async ({ request }) => {
    const data = await request.formData();
    const id = (data.get("id") ?? "").toString();
    const todos = readTodos();
    const todo = todos.find((t) => t.id === id);
    if (!todo) return fail(404, { error: "Todo not found." });
    todo.completed = !todo.completed;
    writeTodos(todos);
  },
  /** Remove the todo whose `id` was submitted. */
  delete: async ({ request }) => {
    const data = await request.formData();
    const id = (data.get("id") ?? "").toString();
    const todos = readTodos();
    const filtered = todos.filter((t) => t.id !== id);
    writeTodos(filtered);
  }
};
export {
  actions,
  load
};
