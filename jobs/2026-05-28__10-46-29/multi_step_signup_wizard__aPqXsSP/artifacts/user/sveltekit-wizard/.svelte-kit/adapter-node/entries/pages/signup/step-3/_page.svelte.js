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
    let firstNameValue = derived(() => form?.firstNameValue ?? data.firstName ?? "");
    let lastNameValue = derived(() => form?.lastNameValue ?? data.lastName ?? "");
    $$renderer2.push(`<h1>Create your account</h1> <p class="step-info">Step 3 of 3 — Your name</p> <form method="POST"><div class="field"><label for="firstName">First name</label> <input type="text" id="firstName" name="firstName"${attr("value", firstNameValue())} autocomplete="given-name" required=""/> `);
    if (form?.field === "firstName") {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error">${escape_html(form.message)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="field"><label for="lastName">Last name</label> <input type="text" id="lastName" name="lastName"${attr("value", lastNameValue())} autocomplete="family-name" required=""/> `);
    if (form?.field === "lastName") {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error">${escape_html(form.message)}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> <button type="submit">Review →</button></form>`);
  });
}
export {
  _page as default
};
