import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
const DATA_PATH = path.resolve("todos.json");
function readTodos() {
  if (!fs.existsSync(DATA_PATH)) {
    return [];
  }
  try {
    const data = fs.readFileSync(DATA_PATH, "utf-8");
    return JSON.parse(data);
  } catch (e) {
    return [];
  }
}
function writeTodos(todos) {
  fs.writeFileSync(DATA_PATH, JSON.stringify(todos, null, 2));
}
const load = async () => {
  return {
    todos: readTodos()
  };
};
const actions = {
  add: async ({ request }) => {
    const data = await request.formData();
    const text = data.get("text");
    if (typeof text !== "string" || text.length === 0) {
      return { success: false };
    }
    const todos = readTodos();
    todos.push({
      id: crypto.randomUUID(),
      text,
      completed: false
    });
    writeTodos(todos);
    return { success: true };
  },
  toggle: async ({ request }) => {
    const data = await request.formData();
    const id = data.get("id");
    const todos = readTodos();
    const todo = todos.find((t) => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
      writeTodos(todos);
    }
    return { success: true };
  },
  delete: async ({ request }) => {
    const data = await request.formData();
    const id = data.get("id");
    const todos = readTodos();
    const newTodos = todos.filter((t) => t.id !== id);
    writeTodos(newTodos);
    return { success: true };
  }
};
export {
  actions,
  load
};
