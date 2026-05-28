import { O as escape_html, N as derived } from "../../../../chunks/renderer.js";
import "@sveltejs/kit/internal";
import "../../../../chunks/exports.js";
import "../../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../../chunks/root.js";
import "../../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let { form } = $$props;
    let passwordError = derived(() => form?.field === "password" ? form.message : "");
    let confirmError = derived(() => form?.field === "confirmPassword" ? form.message : "");
    $$renderer2.push(`<h1>Create your account</h1> <p class="step-info">Step 2 of 3 — Choose a password</p> <form method="POST"><div class="field"><label for="password">Password</label> <input type="password" id="password" name="password" autocomplete="new-password" required=""/> `);
    if (passwordError()) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error">${escape_html(passwordError())}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="field"><label for="confirmPassword">Confirm password</label> <input type="password" id="confirmPassword" name="confirmPassword" autocomplete="new-password" required=""/> `);
    if (confirmError()) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<p class="error">${escape_html(confirmError())}</p>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div> <button type="submit">Continue →</button></form>`);
  });
}
export {
  _page as default
};
