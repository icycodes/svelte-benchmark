import { c as escape_html, e as ensure_array_like, b as attr_class, a as attr, d as derived } from "../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data } = $$props;
    let remainingCount = derived(() => data.todos.filter((todo) => !todo.completed).length);
    $$renderer2.push(`<main class="svelte-1uha8ag"><h1>Todo List</h1> <form method="POST" action="?/add"><input name="text" type="text" placeholder="What needs to be done?" required=""/> <button type="submit" class="svelte-1uha8ag">Add Todo</button></form> <p><strong>${escape_html(remainingCount())}</strong> ${escape_html(remainingCount() === 1 ? "todo" : "todos")} remaining</p> <ul class="svelte-1uha8ag"><!--[-->`);
    const each_array = ensure_array_like(data.todos);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let todo = each_array[$$index];
      $$renderer2.push(`<li${attr_class("svelte-1uha8ag", void 0, { "completed": todo.completed })}><form method="POST" action="?/toggle" style="display: inline;"><input type="hidden" name="id"${attr("value", todo.id)}/> <button type="submit" aria-label="Toggle completion" class="svelte-1uha8ag">${escape_html(todo.completed ? "✅" : "⬜️")}</button></form> <span class="todo-text svelte-1uha8ag">${escape_html(todo.text)}</span> <form method="POST" action="?/delete" style="display: inline;"><input type="hidden" name="id"${attr("value", todo.id)}/> <button type="submit" class="svelte-1uha8ag">Delete</button></form></li>`);
    }
    $$renderer2.push(`<!--]--></ul></main>`);
  });
}
export {
  _page as default
};
