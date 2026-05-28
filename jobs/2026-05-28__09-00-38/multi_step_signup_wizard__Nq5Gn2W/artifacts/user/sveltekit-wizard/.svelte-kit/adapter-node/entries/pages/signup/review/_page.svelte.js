import { e as escape_html } from "../../../../chunks/root.js";
import "clsx";
import "@sveltejs/kit/internal";
import "../../../../chunks/exports.js";
import "../../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data, form } = $$props;
    $$renderer2.push(`<h1>Review Your Information</h1> <dl><dt>Email:</dt> <dd>${escape_html(data.email)}</dd> <dt>First Name:</dt> <dd>${escape_html(data.firstName)}</dd> <dt>Last Name:</dt> <dd>${escape_html(data.lastName)}</dd></dl> <form method="POST">`);
    if (form?.message) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p style="color: red;">${escape_html(form.message)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <button type="submit">Submit</button></form> <p><a href="/signup/step-1">Edit Step 1</a> | <a href="/signup/step-2">Edit Step 2</a> | <a href="/signup/step-3">Edit Step 3</a></p>`);
  });
}
export {
  _page as default
};
