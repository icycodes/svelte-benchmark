import { G as attr, O as escape_html, N as derived } from "../../../../chunks/renderer.js";
import "@sveltejs/kit/internal";
import "../../../../chunks/exports.js";
import "../../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../../chunks/root.js";
import "../../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { data, form } = $$props;
    let emailValue = derived(() => form?.value ?? data.email ?? "");
    $$renderer2.push(`<h1>Create your account</h1> <p class="step-info">Step 1 of 3 — Enter your email</p> <form method="POST"><div class="field"><label for="email">Email address</label> <input type="email" id="email" name="email"${attr("value", emailValue())} autocomplete="email" required=""/> `);
    if (form?.field === "email") {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error">${escape_html(form.message)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> <button type="submit">Continue →</button></form>`);
  });
}
export {
  _page as default
};
