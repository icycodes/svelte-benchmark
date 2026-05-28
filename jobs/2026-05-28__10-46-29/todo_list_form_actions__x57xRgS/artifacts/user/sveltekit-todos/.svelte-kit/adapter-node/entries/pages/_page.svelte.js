import { c as escape_html, e as ensure_array_like, b as attr_style, a as attr, d as derived } from "../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data } = $$props;
    let todos = derived(() => data.todos);
    let remaining = derived(() => todos().filter((t) => !t.completed).length);
    $$renderer2.push(`<h1>Todo List</h1> <p>${escape_html(remaining())} remaining</p> <form method="POST" action="?/add"><input name="text" type="text" placeholder="Add a new todo" required=""/> <button type="submit">Add</button></form> <ul><!--[-->`);
    const each_array = ensure_array_like(todos());
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let todo = each_array[$$index];
      $$renderer2.push(`<li><span${attr_style(`text-decoration: ${todo.completed ? "line-through" : "none"};`)}>${escape_html(todo.text)}</span> <form method="POST" action="?/toggle" style="display:inline;"><input type="hidden" name="id"${attr("value", todo.id)}/> <button type="submit">${escape_html(todo.completed ? "Mark Incomplete" : "Mark Complete")}</button></form> <form method="POST" action="?/delete" style="display:inline;"><input type="hidden" name="id"${attr("value", todo.id)}/> <button type="submit">Delete</button></form></li>`);
    }
    $$renderer2.push(`<!--]--></ul>`);
  });
}
export {
  _page as default
};
