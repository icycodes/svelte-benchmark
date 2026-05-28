import { h as head, a as attr, c as escape_html, e as ensure_array_like, b as attr_class, d as derived } from "../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data, form } = $$props;
    let todos = derived(() => data.todos);
    let remaining = derived(() => todos().filter((t) => !t.completed).length);
    let newText = "";
    head("1uha8ag", $$renderer2, ($$renderer3) => {
      $$renderer3.title(($$renderer4) => {
        $$renderer4.push(`<title>SvelteKit Todos</title>`);
      });
    });
    $$renderer2.push(`<main class="svelte-1uha8ag"><h1 class="svelte-1uha8ag">Todo List</h1> <form method="POST" action="?/add"><div class="add-row svelte-1uha8ag"><input name="text" type="text" placeholder="What needs to be done?"${attr("value", newText)} required="" aria-label="New todo text" class="svelte-1uha8ag"/> <button type="submit" class="svelte-1uha8ag">Add</button></div> `);
    if (form?.error) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error svelte-1uha8ag" role="alert">${escape_html(form.error)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></form> <p class="remaining svelte-1uha8ag"><strong>${escape_html(remaining())}</strong> ${escape_html(remaining() === 1 ? "item" : "items")} remaining</p> `);
    if (todos().length === 0) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="empty svelte-1uha8ag">No todos yet — add one above!</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
      $$renderer2.push(`<ul class="todo-list svelte-1uha8ag"><!--[-->`);
      const each_array = ensure_array_like(todos());
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        let todo = each_array[$$index];
        $$renderer2.push(`<li${attr_class("svelte-1uha8ag", void 0, { "completed": todo.completed })}><form method="POST" action="?/toggle"><input type="hidden" name="id"${attr("value", todo.id)}/> <button type="submit" class="toggle svelte-1uha8ag"${attr("aria-label", todo.completed ? "Mark incomplete" : "Mark complete")}${attr("title", todo.completed ? "Mark incomplete" : "Mark complete")}>`);
        if (todo.completed) {
          $$renderer2.push("<!--[0-->");
          $$renderer2.push(`✅`);
        } else {
          $$renderer2.push("<!--[-1-->");
          $$renderer2.push(`⬜`);
        }
        $$renderer2.push(`<!--]--></button></form> <span class="todo-text svelte-1uha8ag">${escape_html(todo.text)}</span> <form method="POST" action="?/delete"><input type="hidden" name="id"${attr("value", todo.id)}/> <button type="submit" class="delete svelte-1uha8ag" aria-label="Delete todo" title="Delete">🗑️</button></form></li>`);
      }
      $$renderer2.push(`<!--]--></ul>`);
    }
    $$renderer2.push(`<!--]--></main>`);
  });
}
export {
  _page as default
};
