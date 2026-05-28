import { O as escape_html, G as attr } from "../../../../chunks/renderer.js";
import "@sveltejs/kit/internal";
import "../../../../chunks/exports.js";
import "../../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../../chunks/root.js";
import "../../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data, form } = $$props;
    let submitting = false;
    $$renderer2.push(`<h1>Review your details</h1> <p class="step-info">Almost done! Please confirm your information.</p> <dl class="summary svelte-1r63m4q"><dt class="svelte-1r63m4q">Email</dt> <dd class="svelte-1r63m4q">${escape_html(data.email)}</dd> <dt class="svelte-1r63m4q">First name</dt> <dd class="svelte-1r63m4q">${escape_html(data.firstName)}</dd> <dt class="svelte-1r63m4q">Last name</dt> <dd class="svelte-1r63m4q">${escape_html(data.lastName)}</dd> <dt class="svelte-1r63m4q">Password</dt> <dd class="svelte-1r63m4q">••••••••</dd></dl> `);
    if (form?.message) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error">${escape_html(form.message)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <form method="POST"><button type="submit"${attr("disabled", submitting, true)}>${escape_html("Submit →")}</button></form>`);
  });
}
export {
  _page as default
};
