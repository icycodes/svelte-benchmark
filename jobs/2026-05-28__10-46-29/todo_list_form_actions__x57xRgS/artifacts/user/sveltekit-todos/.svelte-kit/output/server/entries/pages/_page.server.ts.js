import { fail } from "@sveltejs/kit";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
const dataFile = path.resolve("todos.json");
function getTodos() {
  if (!fs.existsSync(dataFile)) {
    return [];
  }
  try {
    const data = fs.readFileSync(dataFile, "utf-8");
    return JSON.parse(data);
  } catch (e) {
    return [];
  }
}
function saveTodos(todos) {
  fs.writeFileSync(dataFile, JSON.stringify(todos, null, 2));
}
const load = () => {
  const todos = getTodos();
  return { todos };
};
const actions = {
  add: async ({ request }) => {
    const data = await request.formData();
    const text = data.get("text")?.toString();
    if (!text) {
      return fail(400, { text, missing: true });
    }
    const todos = getTodos();
    todos.push({
      id: crypto.randomUUID(),
      text,
      completed: false
    });
    saveTodos(todos);
    return { success: true };
  },
  toggle: async ({ request }) => {
    const data = await request.formData();
    const id = data.get("id")?.toString();
    if (!id) {
      return fail(400, { id, missing: true });
    }
    const todos = getTodos();
    const todo = todos.find((t) => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
      saveTodos(todos);
    }
    return { success: true };
  },
  delete: async ({ request }) => {
    const data = await request.formData();
    const id = data.get("id")?.toString();
    if (!id) {
      return fail(400, { id, missing: true });
    }
    const todos = getTodos();
    const newTodos = todos.filter((t) => t.id !== id);
    saveTodos(newTodos);
    return { success: true };
  }
};
export {
  actions,
  load
};
